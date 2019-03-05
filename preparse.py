import json, csv

from protein import Protein
from warnings import warn



def parse_all():
    for name in json.load(open('data/human_prot_seqdex.json', 'r')).keys():
        Protein.settings.error_tollerant = False
        Protein.settings.tollerate_missing_attributes = False
        Protein.settings.verbose = True
        Protein(uniprot=name).parse_all(mode='parallel')

def shrink_PDB_xml():
    for name in json.load(open('data/human_prot_seqdex.json', 'r')).keys():
        Protein.settings.error_tollerant = False
        Protein.settings.tollerate_missing_attributes = False
        Protein.settings.verbose = True
        #Protein(uniprot=name).

def get_data(name):
    keys = ('uniprot', 'gene_name', 'length', 'fraction_crystallised', 'fraction_crystallised_homologue', 'pLI', 'pRec', 'pNull')
    try:
        p = Protein(uniprot=name).parse_uniprot().parse_pLI()
        p.length = len(p.sequence)
        p.mask = [False for i in p.sequence]
        p.homomask = [False for i in p.sequence]
        for pdb in p.pdbs:  # {'description': elem.attrib['id'], 'id': elem.attrib['id'], 'x': loca[0], 'y': loca[1]}
            for i in range(int(pdb['x'].split(',')[0]), int(pdb['y'].split(',')[0])):
                p.mask[i] = True
        for pdb in p.pdb_matches:
            for i in range(int(pdb['match_start']), int(pdb['match_start']) + int(pdb[
                                                                                      'match_length'])):  # {'match': align.title[0:50], 'match_score': hsp.score, 'match_start': hsp.query_start, 'match_length': hsp.align_length, 'match_identity': hsp.identities / hsp.align_length}
                if i < len(p.homomask):
                    p.homomask[i] = True
        p.fraction_crystallised = sum(p.mask) / p.length
        p.fraction_crystallised_homologue = sum(p.homomask) / p.length
        return {a: getattr(p, a) for a in keys}
    except Exception as err:
        warn(str(err))
        return {'uniprot': name}

def crystal():
    from multiprocessing import Pool
    keys=('uniprot', 'gene_name','length','fraction_crystallised','fraction_crystallised_homologue','pLI','pRec','pNull')
    w = csv.DictWriter(open('crystal.csv','w',newline=''),keys)
    w.writeheader()
    Protein.settings.error_tollerant = True
    Protein.settings.tollerate_missing_attributes = True
    Protein.settings.verbose = False
    for name in json.load(open('data/human_prot_seqdex.json', 'r')).keys():
        data = get_data(name)
        w.writerow(data)

def crystal2():
    from multiprocessing import Pool
    keys=('uniprot', 'gene_name','length','fraction_crystallised','fraction_crystallised_homologue','pLI','pRec','pNull')
    w = csv.DictWriter(open('crystal3.csv','w',newline=''),keys)
    w.writeheader()
    Protein.settings.error_tollerant = True
    Protein.settings.tollerate_missing_attributes = True
    Protein.settings.verbose = False
    for row in csv.DictReader(open('crystal.csv')):
        p = Protein(uniprot=row['uniprot'], gene_name=row['gene_name']).parse_pLI()
        w.writerow({**row,'pLI':p.pLI,'pRec':p.pRec, 'pNull': p.pNull})


data=json.load(open('data/swissprot/INDEX.json'))
keys=('uniprot', 'gene_name','length','fraction_crystallised','fraction_crystallised_homologue','pLI','pRec','pNull')
w = csv.DictWriter(open('crystal4.csv','w',newline=''),keys)
for model in data['index']:
    model['uniprot_ac']
