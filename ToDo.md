# There is a lot to do...

## Get a basic site up
&#10003; Input and output

&#10003; concurrent Progress ajax. Implemented incorrectly: currently one ajax asks if the protein exists and if it does returns but also kicks off a parallel task. The checker ajax loops until the tasks are doen.

&#10005; The backend is diabolically messy. Fix ajax to send a data check. On success send a long timeout request that does the hardwork and in parallel send quick status update ajax loop. _I.e._ have two concurrent ajaxes (ajaces? ajantes (aἴᾰντες)? oh, it's dual so ajante/aἴᾰντε). The longer ajax means that the Session does not hold thread names that need to be awkwardly retrieved and the instance isn't JSON serialised.

&#10005; Card to show predicted effect. And show all the data if requested. Such as sequence.

## Moving to Protein()
&#10003; Parallelise.

&#10005; Prepare. See "Prepare"

&#10003; Detatch mutational data from protein.

&#10005; Finish moving from `Tracker_analyser.Variant` to `protein.Protein` class (a cleaner and unlinked to tracker variant).

&#10005; Rewrite Pfam to use Monkeypatched ET as opposed to the messy dictionary shortcut

&#10005; Do something about Go and Tissue (vide infra)

&#10005; Deactivate manual data? This ought to be session specific not global.

## Extra data

&#10005; coservation... this is tricky. I think the best bet is to use Uniprot's Uniprot-50 or -80 and do a blast beforehand.
&#10005; phosphorylation... Phosphosite downloaded. Just needs retrieval.


## Preallocate

&#10005; Run local Blast against PDB for the whole proteome. Everything is in place

&#10005; Make models? See models.

## Database

&#10005; Users and such. Alchemy running.



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
Tour is not working. This has strong dejavu. It is not FeatureViewer's doing though!

## Arrow
It would be really nice having a chevron pointing from one card to the other.
