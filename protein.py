__description__ = """
Protein was formerly called Variant.
"""


import os, pickle, threading
from datetime import datetime
from warnings import warn
from ET_monkeypatch import ET
from settings_handler import global_settings
from collections import defaultdict

import requests # for xml fetcher.
import re, xmlschema # for xml parser.



#######################
class Protein:
    """
    This class handles each protein entry from Uniprot. See __init__ for the list of variables stored.
    It fills them from various other sources.

        >>> Protein()
        >>> Protein(xml_entry) # equivalent to Protein()._parse_unicode_xml(xml_entry)
        >>> Protein.load('filename')

    NB. The ET.Element has to be monkeypatched. See `help(ElementalExpansion)`
    """
    error_tollerant = False  #mainly for dubug. # formally called croak
    settings = global_settings
    # these older commands should be made redundant
    #    fetch = True
    #    croak = True
    #    tollerate_no_SNV = True

    # decorator
    def _failsafe(func):
        def wrapper(self, *args, **kargs):
            # the call happned after chekcing if it should croak on error so to make the traceback cleaner.
            if self.error_tollerant:
                try:
                    return func(self, *args, **kargs)
                except Exception as error:
                    print('Error caught in method `Protein().{n}`: {e}'.format(n=func.__name__, e=error))
                    return None
            else:
                return func(self, *args, **kargs)

        return wrapper

    def __getattr__(self, item):
        if item not in self.__dict__:
            if item in self.other:  ## it is in the trash!
                warn('Accessed attribute in other list. Thanks for proving the key:value pair. But please dont abuse this backdoor!')
                self.__dict__[item] = self.other[item]
            else:
                warn('Accessed non-existant attribute {item} for Protein instance. Likely cause the code changed, but the from_pickle flag is True.'.format(v=self, item=item))
                self.__dict__[item] = 'Unknown'
        return self.__dict__[item]

    ############################# UNIPROT PARSING METHODS #############################
    @_failsafe
    def _parse_protein_element(self, elem):
        for name_el in elem:
            if name_el.is_tag('recommendedName') and name_el.has_text():
                self.recommended_name = name_el.text.rstrip()
            elif name_el.is_tag('recommendedName'):
                for subname_el in name_el:
                    if subname_el.is_tag('fullName'):
                        self.recommended_name = subname_el.text.rstrip()
                    else:
                        self.alternative_shortname_list.append(subname_el.text.rstrip())
            else:
                for subname_el in name_el:
                    if subname_el.is_tag('fullName'):
                        self.alternative_fullname_list.append(subname_el.text.rstrip())
                    else:
                        self.alternative_shortname_list.append(subname_el.text.rstrip())

    @_failsafe
    def _parse_protein_dbReference(self, elem):
        if elem.has_attr('type','Pfam'):
            pass
            # no need as pfam is parsed separately as it has better info.
            #self.Uniprot_pfam = [(xref['id'], xref['property'][0]['value']) for xref in clean_dict[''] if xref['type'] == 'Pfam']
        elif elem.has_attr('type','GO'):
            pass
        elif elem.has_attr('type','PDB'):
            chain = elem.get_sub_by_type('chains')
            if chain is not None:  ## this is so unpredictable. It needs to be done by blast.
                loca=chain.attrib['value'].split('=')[1].split('-')
                self.pdbs.append({'description': elem.attrib['id'], 'id': elem.attrib['id'], 'x': loca[0], 'y': loca[1]})
        elif elem.has_attr('type', 'Ensembl'):
            self.ENST = elem.attrib['id']
            for subelem in elem:
                if subelem.is_tag('molecule'):
                    if subelem.attrib['id'][-2:] != '-1':
                        return None ## this is not the isoform 1 !!!
                elif subelem.has_attr('type', 'protein sequence ID'):
                    self.ENSP = subelem.attrib['value']
                elif subelem.has_attr('type', 'gene ID'):
                    self.ENSG = subelem.attrib['value']
        else:
            pass

    @_failsafe
    def _parse_protein_gene(self, elem):
        for name_el in elem:
            if name_el.is_tag('name'):
                if name_el.has_attr('type', 'primary'):
                    self.gene_name = name_el.text
                elif name_el.has_attr('type', 'synonym'):
                    self.alt_gene_name_list.append(name_el.text)
        return self

    @_failsafe
    def _parse_protein_comment(self,elem):
        if elem.has_attr('type','interaction') or elem.has_attr('type','subunit'):
            for subelem in elem:
                if subelem.is_tag('interactant'):
                    partner = subelem.get_subtag('label')
                    if partner is not None:
                        self.partners['interactant'].append(partner.text)
                elif subelem.is_tag('text'):  ## some entries are badly annotated and have only a text line..
                    self.partners['interactant'].append(subelem.text)
        elif elem.has_attr('type','disease'):
            for subelem in elem:
                if subelem.is_tag('disease'): #yes. the comment type=disease has a tag disease. wtf
                    disease = {'id': subelem.attrib['id']}
                    for key in ('description', 'name'):
                        subsub = subelem.get_subtag(key)
                        if subsub is not None:
                            disease[key] = subsub.text
                    mim = subelem.get_sub_by_type('MIM')
                    if min:
                        disease['MIM'] = mim.attrib['id']
                    self.diseases.append(disease)

    @_failsafe
    def _parse_protein_feature(self,elem):
        """ These are the possible feature types:
        * active site
        * binding site
        * calcium-binding region
        * chain
        * coiled-coil region
        * compositionally biased region
        * cross-link
        * disulfide bond
        * DNA-binding region
        * domain
        * glycosylation site
        * helix
        * initiator methionine
        * lipid moiety-binding region
        * metal ion-binding site
        * modified residue
        * mutagenesis site
        * non-consecutive residues
        * non-terminal residue
        * nucleotide phosphate-binding region
        * peptide
        * propeptide
        * region of interest
        * repeat
        * non-standard amino acid
        * sequence conflict
        * sequence variant
        * short sequence motif
        * signal peptide
        * site
        * splice variant
        * strand
        * topological domain
        * transit peptide
        * transmembrane region
        * turn
        * unsure residue
        * zinc finger region
        * intramembrane region"""
        if elem.attrib['type'] not in self.features:  ##avoiding defaultdictionary to avoid JSON issue.
            self.features[elem.attrib['type']]=[]
        locadex=self._get_location(elem)
        if locadex:
            self.features[elem.attrib['type']].append(self._get_location(elem))
        return self



    def _get_location(self, elem):
        location = elem.get_subtag('location')
        if location is None:
            return None
        position = location.get_subtag('position')
        start = location.get_subtag('start')
        end =  location.get_subtag('end')
        if position is not None:  # single residue
            x = position.attrib['position']
            return {'x': x, 'y': x, 'description': elem.attrib['description'], 'id': '{t}_{s}'.format(s=x, t=elem.attrib['type'].replace(' ','').replace('-',''))}
        elif start and end:  # region or disulfide
            x = start.attrib['position']
            y = end.attrib['position']
            return {'x': x, 'y': y, 'description': elem.attr['description'], 'id': '{t}_{x}_{y}'.format(x=x, y=y, t=elem.attrib['type'].replace(' ', '').replace('-',''))}

    def _parse_unicode_xml(self, entry):
        """
        loads the Protein instance with the data from the uniprot XML entry element.
        Unlike the previous version the elemtn tree is parsed directly as opposed to converitng into a dictionary that seemed at first a wiser strategy but wasn't.
        Do note htat the ET.Element has to be monkeypatched. See `help(ElementalExpansion)`
        :param entry: the entry element of the XML parsed by Element Tree.
        :return:
        """
        for elem in entry:
            if elem.is_tag('accession'):
                self.accession_list.append(elem.text.rstrip())
            elif elem.is_tag('name'):
                self.uniprot_name = elem.text.rstrip()
            elif elem.is_tag('sequence'):
                self.sequence = elem.text.rstrip()
            elif elem.is_tag('protein'):
                self._parse_protein_element(elem)
            elif elem.is_tag('dbReference'):
                self._parse_protein_dbReference(elem)
            elif elem.is_tag('gene'):
                self._parse_protein_gene(elem)
            elif elem.is_tag('feature'):
                self._parse_protein_feature(elem)
            elif elem.is_tag('comment'):
                self._parse_protein_comment(elem)
            elif elem.is_tag('keyword'):
                pass

    ############################# INIT #############################
    def __init__(self, entry=None, gene_name='', uniprot_name = '', sequence='', **other):
        ### predeclaration (and cheatsheet)
        self.xml = entry
        self.gene_name = gene_name
        self.uniprot_name = uniprot_name ## S39AD_HUMAN
        #### uniprot derivved
        self.alt_gene_name_list = []
        self.accession_list = [] ## Q96H72 etc.
        self.sequence = sequence  ###called seq in early version causing eror.rs
        self.recommended_name = '' #Zinc transporter ZIP13
        self.alternative_fullname_list = []
        self.alternative_shortname_list = []
        self.features={}  #see _parse_protein_feature. Dictionary of key: type of feature, value = list of dict with the FeatureViewer format (x,y, id, description)
        self.partners ={'interactant': []} # lists not sets as it gave a pickle issue.
        self.diseases=[] # 'description', 'name', 'id', 'MIM'
        self.pdbs = []  # {'description': elem.attrib['id'], 'id': elem.attrib['id'], 'x': loca[0], 'y': loca[1]}
        ### junk
        self.other = other ### this is a garbage bin. But a handy one.
        self.logbook = [] # debug purposes only. See self.log()
        ### fill
        if entry:
            self._parse_uniprot_xml(entry)

    def parallel_parse_protein(self, uniprot, gene_name, return_complete=True):
        """
        A parallel version of the protein fetcher.
        It deals with the non-mutation parts of the Variant.
        oNly `.uniprot` and `.gene` attributes are needed.
        :param uniprot:
        :param gene_name:
        :param return_complete: a boolean flag that either returns the threads if False, or waits for the threads to complete if true.
        :return:
        """
        self.settings.verbose = False  # for now.
        self.from_pickle = False
        self.uniprot = uniprot
        self.gene = gene_name  # gene_name
        tasks = {'Uniprot': self.parse_uniprot,
                 'PFam': self.parse_pfam,
                 'ELM': self.query_ELM,
                 'pLI': self.get_pLI,
                 'ExAC': self.get_ExAC,
                 'manual': self.add_manual_data,
                 'GO terms': self.fetch_go,
                 'Binding partners': self.fetch_binders}
        threads = {}
        for k, fn in tasks.items():
            t = threading.Thread(target=fn)
            t.start()
            threads[k] = t
        if return_complete:
            for tn, t in threads.items():
                t.join()
            return self
        else:
            return (self, threads)

    ############################# IO #############################
    def dump(self, file=None):
        if not file:
            file = os.path.join(self.settings.pickle_folder, '{0}.p'.format(self.uniprot_name))
        pickle.dump(self.__dict__, open(file, 'wb'))
        self.log('Data saved to {} as pickled dictionary'.format(file))

    @classmethod
    def load(cls, file):
        self = cls.__new__(cls)
        self.__dict__ = pickle.load(open(file, 'rb'))
        self.log('Data from the pickled dictionary {}'.format(file))
        return self

    def write_uniprot(self, file=None):
        if not file:
            file=self.uniprot_name+'.xml'
        with open(file,'w') as w:
            w.write(
                '<?xml version="1.0" encoding="UTF-8"?><uniprot xmlns="http://uniprot.org/uniprot" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' +
                'xsi:schemaLocation="http://uniprot.org/uniprot http://www.uniprot.org/docs/uniprot.xsd">')
            if isinstance(self.xml,str):
                w.write(self.xml)
            else:
                w.write(ET.tostring(self.xml).decode())
            w.write('</uniprot>')


    def log(self, text):
        msg = '[{}]\t'.format(str(datetime.now())) + text
        self.logbook.append(msg)
        if self.settings.verbose:
            print(msg)

    ############################# Data gathering #############################
    def xml_fetcher(self, mode):  # mode = uniprot or pfam
        file = os.path.join(self.settings.get_folder_of(mode), self.uniprot + '_' + mode + '.xml')
        if os.path.isfile(file):
            with open(file, 'r') as w:
                xml = w.read()
            self.log('{0} read from file {1}'.format(mode, file))
        else:
            self._assert_fetchable(mode)
            if mode == 'uniprot':
                requestURL = 'https://www.ebi.ac.uk/proteins/api/proteins?offset=0&size=100&accession={acc}&taxid=9606'.format(
                    acc=self.uniprot)
            elif mode == 'pfam':
                requestURL = 'https://pfam.xfam.org/protein?output=xml&acc={acc}'.format(acc=self.uniprot)
            else:
                raise ValueError('Only options for mode are uniprot or pfam')
            req = requests.get(requestURL, headers={"Accept": "application/xml"})
            if req.status_code != 200:
                raise ConnectionError('Could not retrieve data: ' + req.text)
            xml = req.text
            with open(file, 'w') as w:
                w.write(xml)
        return xml

    def xml_parser(self, mode, xml):
        """
        THIS METHOD WILL BE DEPRACATED ONCE PFAM PARSER IS REWRITTEN!!
        This is weird. uniprot works fine getting it parsed via its XML schema, while pfam fails even with validation = lax.
        So the pfam data uses stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree
        and not schema. I favour the latter as it ain't a just a snippet from SO, but the latter seems okay.
        I looked at how https://github.com/prody/ProDy/blob/master/prody/database/pfam.py does it and they
        simply returns the ET root yet say it returns a dictionary. :-S
        :param mode:
        :param xml:
        :return:
        """

        def deep_clean(element, damn):  # the values have the annoying {http} field this removes them.
            try:
                if isinstance(element, dict):
                    return {k.replace(damn, '').replace('@', '').replace('#', ''): deep_clean(element[k], damn) for k in
                            element}
                elif isinstance(element, list):
                    return [deep_clean(e, damn) for e in element]
                elif isinstance(element, str):
                    if re.fullmatch('\d*', element):
                        return int(element)
                    elif re.fullmatch('-?\+?\d*\.?\d*e?\d*', element):
                        return float(element)
                    else:
                        return element.replace(damn, '')  # there should not be a damn
                else:
                    return element
            except ValueError:
                return element

        # from https://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree
        def etree_to_dict(t):
            d = {t.tag: {} if t.attrib else None}
            children = list(t)
            if children:
                dd = defaultdict(list)
                for dc in map(etree_to_dict, children):
                    for k, v in dc.items():
                        dd[k].append(v)
                d = {t.tag: {k: v[0] if len(v) == 1 else v
                             for k, v in dd.items()}}
            if t.attrib:
                d[t.tag].update(('@' + k, v)
                                for k, v in t.attrib.items())
            if t.text:
                text = t.text.strip()
                if children or t.attrib:
                    if text:
                        d[t.tag]['#text'] = text
                else:
                    d[t.tag] = text
            return d

        sch_URL = {'uniprot': 'https://www.uniprot.org/docs/uniprot.xsd',
                   'pfam': 'https://pfam.xfam.org/static/documents/schemas/protein.xsd'}[mode]

        etx = ET.XML(xml)
        if mode == 'uniprot':
            schema = xmlschema.XMLSchema(sch_URL)
            entry_dict = schema.to_dict(etx)['{http://uniprot.org/uniprot}entry'][0]
        elif mode == 'pfam':
            protoentry_dict = etree_to_dict(etx)
            if '{https://pfam.xfam.org/}matches' in protoentry_dict['{https://pfam.xfam.org/}pfam'][
                '{https://pfam.xfam.org/}entry']:
                entry_dict = protoentry_dict['{https://pfam.xfam.org/}pfam']['{https://pfam.xfam.org/}entry'][
                    '{https://pfam.xfam.org/}matches']['{https://pfam.xfam.org/}match']
            else:
                entry_dict = []
        else:
            raise ValueError
        damn = {'uniprot': '{http://uniprot.org/uniprot}', 'pfam': '{https://pfam.xfam.org/}'}[mode]
        return deep_clean(entry_dict, damn)

    def xml_fetch_n_parser(self, mode):  # mode = Unprot or pfam
        assert mode in ['uniprot', 'pfam'], 'Unknown mode: ' + mode
        xml = self.xml_fetcher(mode)
        return self.xml_parser(mode, xml)


    def parse_uniprot(self):
        """
        This is an rewritten version that does not use ET -> dict.
        """
        xml = self.xml_fetcher('uniprot')
        self.xml = ET.fromstring(xml)[0]
        self._parse_unicode_xml(self.xml)




    def fetch_ENSP(self):
        """EMBL ids should vome from the Unirpto entry. However, in some cases too many it is absent."""
        for row in self.settings.open('ensembl'):
            if self.gene in row:
                if row.count(' ') > 5:
                    self.ENSP = row.split()[5]
                return self
        else:
            warn('Unknown Ensembl protein id for ' + self.gene)


    def predict_effect(self):
        pass
        ##TOdo write>!

    ## depraction
    def write(self, file=None):
        raise Exception('DEPRACATED. use write_uniprot')



import unittest

class TestProtein(unittest.TestCase):

    def test_warn(self):
        print('Two userwarnings coming up')
        Protein.settings.verbose = True
        irak = Protein()
        with self.assertWarns(UserWarning) as cm:
            foo = irak.foo
        with self.assertWarns(UserWarning) as cm:
            irak.other['bar'] = 'bar'
            self.assertEqual(irak.bar, 'bar')


    def test_parse(self):
        print('testing parsing')
        irak = Protein()
        irak.uniprot = 'Q9NWZ3'
        irak.gene = 'IRAK4'
        irak.parse_uniprot()
        self.assertEqual(irak.sequence[0], 'M')




if __name__ == '__main__':
    print('*****Test********')

    unittest.main()
    #irak.parse_uniprot()





















