# There is a lot to do...

## Urgent

* Rewrite ELM pattern searches (formerly ELM website requests)
* Fix PDB analysis (surface/core, residue distance to phosphosites)

## Misc
&#10005; Card to show more data if requested. Such as sequence.

&#10005; Idea. Train on known variants. How do I parse verbose human text? Keyword mining?

## Moving to Protein()

&#10005; Do something about Go and Tissue (vide infra)

&#10005; Deactivate manual data? This ought to be session specific not global.

## Extra data

&#10005; coservation... this is tricky. I think the best bet is to use Uniprot's Uniprot-50 or -80 and do a blast beforehand.
&#10005; phosphorylation... Phosphosite downloaded. Just needs retrieval.


## Preallocate

&#10005; Make models? See models.


## Models

Make threaded models of very close homologues and fix the numbering?

The code to do it by altering the residues and letting Rosetta Score fix it does not work if there are too many changes.

Make phosphorylated versions? Very straightforward.

It is worth revisit the idea of getting I-Tasser to run locally and pre-making a bunch of somewhat close and easy models of protein with high pLI.
I-Tasser submits Slurm jobs, but I got to switch to Qsub, but I never went ahead as I was not sure about Rescomp charges.

There is also the possibility of scraping I-TASSER queue and ModelBase or whatever it is called.

## GO and Tissue
These two have been removed. The former is rather useful in combination with the binding partners, their diseases and their pLI. Nothing much has come from this. Maybe a table?

See depracted methods folder for the mssing methods.

## Tour
Reactivate/rewrite tour once complete.
