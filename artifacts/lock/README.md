# Experiment provenance

`pre-heldout-v1.json` records the original experiment at commit
`ec605a35a22693b65ca98f7448ca2954ea6bcfed`. `protocol-snapshot.zip` preserves its
protocol documents byte-for-byte. `maintenance.json` records approved documentation
and reporting changes separately from the original lock.

Later commits added comparison methods and extended fusion code. The original
lock therefore does not describe every file in the current checkout. Full lock
verification requires the matching source revision and original datasets, models,
and ranking stores. `make tables` independently verifies the released numerical
results from included per-query records.
