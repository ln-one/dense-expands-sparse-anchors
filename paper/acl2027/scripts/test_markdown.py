"""Focused regression tests for the manuscript conversion boundary."""

import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("builder", ROOT / "scripts/build_markdown.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)
CONFIG = json.loads((ROOT / "manuscript.json").read_text())


class MarkdownBuildTests(unittest.TestCase):
    def test_reading_link_resolves_publication_reference(self):
        config = dict(CONFIG, references={"../preview/example.svg": {"kind": "ref", "label": "fig:test"}})
        latex = builder.compile_markdown("See [1](../preview/example.svg).", config)
        self.assertIn(r"\ref{fig:test}", latex)

    def test_layout_boundaries_are_checked(self):
        with self.assertRaisesRegex(ValueError, "Layout boundary"):
            builder.compile_markdown("Text.", CONFIG, {"layout_insertions": [{"before": "Missing", "latex": r"\FloatBarrier"}]})

    def test_no_publication_commands_in_markdown(self):
        for path in (ROOT / "markdown").glob("*.md"):
            for marker in ("<!-- latex", "<!-- anchor:", r"\FloatBarrier", '"ref:', '"eqref:'):
                self.assertNotIn(marker, path.read_text())

    def test_hidden_anchor_preserves_label(self):
        config = dict(CONFIG, anchors={"sec-test": "sec:test"})
        latex = builder.compile_markdown("# Test\n\n<!-- anchor: sec-test -->\n", config)
        self.assertEqual(latex.count(r"\label{sec:test}"), 1)
        self.assertNotIn("<!--", latex)

    def test_edit_changes_compiled_text(self):
        before = builder.compile_markdown("A manuscript sentence.", CONFIG)
        after = builder.compile_markdown("A revised manuscript sentence.", CONFIG)
        self.assertNotEqual(before, after)
        self.assertIn("revised", after)

    def test_numbered_math_has_no_nested_display(self):
        source = r"$$\begin{equation}x=1\label{eq:test}\end{equation}$$"
        latex = builder.compile_markdown(source, CONFIG)
        self.assertIn(r"\begin{equation}", latex)
        self.assertNotIn(r"\[", latex)
        self.assertIn(r"\label{eq:test}", latex)

    def test_equation_reference_is_dynamic(self):
        config = dict(CONFIG, labels={"eq:test": "method"})
        latex = builder.compile_markdown('[99](method.md "eqref:eq:test")', config)
        self.assertIn(r"\eqref{eq:test}", latex)
        self.assertNotIn("99", latex)

    def test_preview_label_comment_is_restored_for_tex(self):
        text = "$$\\begin{equation}x=1\n% label: eq:test\n\\end{equation}$$"
        latex = builder.compile_markdown(text, CONFIG)
        self.assertIn(r"\label{eq:test}", latex)
        self.assertNotIn("% label:", latex)

    def test_heading_anchor_does_not_duplicate_label(self):
        config = dict(CONFIG, anchors={"sec-test": "sec:test"})
        latex = builder.compile_markdown("# Test\n\n^sec-test\n", config)
        self.assertEqual(latex.count(r"\label{"), 1)
        self.assertIn(r"\label{sec:test}", latex)

    def test_unnumbered_heading(self):
        latex = builder.compile_markdown("# Limitations\n\nScope remains unchanged.\n", CONFIG, {"unnumbered": True})
        self.assertIn(r"\section*{Limitations}", latex)

    def test_heading_numbered_by_default(self):
        for section in (None, {"unnumbered": False}):
            latex = builder.compile_markdown("# Example\n\nBody text.\n", CONFIG, section)
            self.assertIn(r"\section{Example}", latex)

    def test_limitations_layout_is_external(self):
        section = next(s for s in CONFIG["sections"] if s["markdown"] == "markdown/08.limitations.md")
        text = (builder.ROOT / section["markdown"]).read_text()
        self.assertFalse(text.startswith("---"))
        self.assertIn(r"\section*{Limitations}", builder.compile_markdown(text, CONFIG, section))

    def test_citations_preserve_keys(self):
        latex = builder.compile_markdown("Evidence [@first; @second].", CONFIG)
        self.assertIn("first", latex)
        self.assertIn("second", latex)
        self.assertIn(r"\cite{" if CONFIG.get("numeric_citations") else r"\citep{", latex)

    def test_unknown_asset_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unregistered image"):
            builder.compile_markdown("![Missing](../preview/missing.png)", CONFIG)

    def test_figure_caption_is_editable_in_markdown(self):
        path = next(p for p, a in CONFIG["assets"].items() if a["kind"] == "figure")
        latex = builder.compile_markdown("![Revised caption with $x$.](" + path + ")", CONFIG)
        self.assertIn(r"\caption{Revised caption", latex)
        self.assertIn(r"\includegraphics", latex)
        self.assertNotIn("@@CAPTION@@", latex)

    def test_manuscript_assets_and_links_exist(self):
        for section in CONFIG["sections"]:
            file = ROOT / section["markdown"]
            ast = json.loads(builder.pandoc(file.read_text(), "markdown-implicit_figures", "json"))

            def visit(node):
                if isinstance(node, list):
                    for child in node:
                        visit(child)
                elif isinstance(node, dict):
                    if node.get("t") in ("Link", "Image"):
                        target = node["c"][2][0]
                        if "://" not in target:
                            path, _, anchor = target.partition("#")
                            destination = file.parent / path
                            self.assertTrue(destination.is_file(), target)
                            if anchor.startswith("^"):
                                self.assertIn(anchor, destination.read_text())
                    for value in node.values():
                        visit(value)
            visit(ast)

    def test_all_generated_sections_are_current(self):
        builder.build(check=True)


if __name__ == "__main__":
    unittest.main()
