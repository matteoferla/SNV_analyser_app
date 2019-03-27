# VENUS (Variant Effect on Structure)
A web app that gathers data on a protein and predict the effect of a SNV from a structural point of view.

# Entrypoint
There is a different entrypoint here.
Namely, in the Tracker_analyser, the entry was a NCBI code, which meant that from there the Uniprot entry was taken.
Here instead all the Uniprot entryies are preparsed to get gene name, synonym and short name into a dictionary that links to the uniprot id.


