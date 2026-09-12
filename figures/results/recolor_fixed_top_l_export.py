"""Recolor an existing diagnostic export when raw results are unavailable.

Only the three raster cell fills change; vector labels/geometry remain intact.
The normal source is fig_fixed_top_l_diagnostics.py. Requires PyMuPDF and NumPy.
"""
from pathlib import Path
import pymupdf as fitz
import numpy as np
import shutil
root=Path(__file__).resolve().parents[2]
p=root/'figures/results/fig_fixed_top_l_diagnostics.pdf'
doc=fitz.open(p); before=doc[0].get_text()
# Existing 3-class matrix image only. Vector text, numbers, positions stay byte-identical.
mapping={(238,241,243):(244,244,244),(215,240,233):(214,238,235),(244,216,210):(247,222,216)}
for info in doc[0].get_images():
 pix=fitz.Pixmap(doc,info[0]);arr=np.frombuffer(pix.samples,dtype=np.uint8).reshape(-1,3).copy()
 assert set(map(tuple,arr)).issubset(set(mapping) | set(mapping.values()))
 original=arr.copy()
 for a,b in mapping.items(): arr[(original==a).all(axis=1)]=b
 pix2=fitz.Pixmap(fitz.csRGB,pix.width,pix.height,arr.tobytes(),False)
 doc[0].replace_image(info[0],pixmap=pix2)
out=p.with_name(p.stem+'-recolored.pdf');doc.save(out,garbage=4,deflate=True);doc.close();out.replace(p)
with fitz.open(p) as new:
 assert new[0].get_text()==before
 new[0].get_pixmap(matrix=fitz.Matrix(450/72,450/72)).save(p.with_suffix('.png'))
 p.with_suffix('.svg').write_text(new[0].get_svg_image(text_as_path=True))
shutil.copy2(p,root/'paper/acl2027/figures'/p.name)
print('Recolored only 3 matrix cell fills; all text and numbers unchanged')
