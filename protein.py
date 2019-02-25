__description__ = """
Protein was formerly called Variant.
"""


import os
import pickle
import re
import threading
from collections import defaultdict
from datetime import datetime
from warnings import warn

import requests  # for xml fetcher.

from ET_monkeypatch import ET #monkeypatched version
from settings_handler import global_settings


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
        self.partners ={'interactant': [],  #from uniprot
                        'BioGRID': [],  #from biogrid downlaoad
                        'SSL': [],  #Slorth data
                        'stringDB highest': [],  # score >900
                        'stringDB high': [],  #900 > score > 700
                        'stringDB medium': [], #400 > score > 400
                        'stringDB low': [] #score < 400
                        } # lists not sets as it gave a pickle issue.
        self.diseases=[] # 'description', 'name', 'id', 'MIM'
        self.pdbs = []  # {'description': elem.attrib['id'], 'id': elem.attrib['id'], 'x': loca[0], 'y': loca[1]}
        ### ExAC
        self.ExAC_type = 'Unparsed' # Dominant | Recessive | None | Unknown (=???)
        self.pLI = -1
        self.pRec = -1
        self.pNull = -1
        ### junk
        self.other = other ### this is a garbage bin. But a handy one.
        self.logbook = [] # debug purposes only. See self.log()
        self._threads = {}
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
    def _assert_fetchable(self, text):
        if not self.settings.fetch:
            raise FileNotFoundError(
                text + ' failed previously (or never run previously) and `.settings.fetch` is enabled')


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
        return self

    @_failsafe
    def parse_pfam(self):
        # https://pfam.xfam.org/help#tabview=tab11
        xml = self.xml_fetch_n_parser('pfam')
        if isinstance(xml, list):
            self.pfam = xml
        elif isinstance(xml, dict):
            self.pfam = [xml]
        else:
            raise ValueError('not list or dict pfam data: ' + str(xml))

    @_failsafe
    def fetch_binders(self):
        file = os.path.join(self.settings.binders_folder, self.uniprot + '.json')
        if os.path.isfile(file):
            with open(file) as f:
                self.partners = json.load(f)
        else:
            for row in self.settings.open('ssl'):
                # CHEK1	MTOR	ENSG00000149554	ENSG00000198793	H. sapiens	BioGRID	2208318, 2342099, 2342170	3
                if self.gene in row:
                    protein_set = set(row.split('\t')[:2])
                    protein_set.discard(self.gene)
                    if protein_set == 1:
                        self.partners['SSL'].append(protein_set.pop())
                    else:  # most likely a partial match.
                        pass
                        # warn('Impossible SSL '+row)
            for row in self.settings.open('huri'):
                # Unique identifier for interactor A	Unique identifier for interactor B	Alternative identifier for interactor A	Alternative identifier for interactor B	Aliases for A	Aliases for B	Interaction detection methods	First author	Identifier of the publication	NCBI Taxonomy identifier for interactor A	NCBI Taxonomy identifier for interactor B	Interaction types	Source databases	Interaction identifier(s)	Confidence score	Complex expansion	Biological role A	Biological role B	Experimental role A	Experimental role B	Interactor type A	Interactor type B	Xref for interactor A	Xref for interactor B	Xref for the interaction	Annotations for interactor A	Annotations for interactor B	Annotations for the interaction	NCBI Taxonomy identifier for the host organism	Parameters of the interaction	Creation date	Update date	Checksum for interactor A	Checksum for interactor B	Checksum for interaction	negative	Feature(s) for interactor A	Feature(s) for interactor B	Stoichiometry for interactor A	Stoichiometry for interactor B	Participant identification method for interactor A	Participant identification method for interactor B
                # -	uniprotkb:Q6P1W5-2	ensembl:ENST00000507897.5|ensembl:ENSP00000426769.1|ensembl:ENSG00000213204.8	ensembl:ENST00000373374.7|ensembl:ENSP00000362472.3|ensembl:ENSG00000142698.14	human orfeome collection:2362(author assigned name)	human orfeome collection:5315(author assigned name)	"psi-mi:""MI:1112""(two hybrid prey pooling approach)"	Yu et al.(2011)	pubmed:21516116	taxid:9606(Homo Sapiens)	taxid:9606(Homo Sapiens)	"psi-mi:""MI:0407""(direct interaction)"	-	-	-	-	-	-	"psi-mi:""MI:0496""(bait)"	"psi-mi:""MI:0498""(prey)"	"psi-mi:""MI:0326""(protein)"	"psi-mi:""MI:0326""(protein)"	-	-	-	"comment:""vector name: pDEST-DB""|comment:""centromeric vector""|comment:""yeast strain: Y8930"""	"comment:""vector name: pDEST-AD""|comment:""centromeric vector""|comment:""yeast strain: Y8800"""	"comment:""Found in screens 1."""	taxid:4932(Saccharomyces cerevisiae)	-	6/30/2017	-	-	-	-	-	DB domain (n-terminal): gal4 dna binding domain:n-n	AD domain (n-terminal): gal4 activation domain:n-n	-	-	"psi-mi:""MI1180""(partial DNA sequence identification)"	"psi-mi:""MI1180""(partial DNA sequence identification)"
                if ':' + self.gene + '(' in row:  #
                    protein_set = re.findall('\:(\w+)\(gene name\)', row)
                    if len(protein_set) == 2:
                        protein_set = set(protein_set)
                        protein_set.discard(self.gene)
                        if protein_set == 1:
                            self.partners['HuRI'].append(protein_set.pop())
                    # t = set(row.split('\t')[:2])
                    # print(t)
                    # if t:
                    #     for p in t:
                    #         if 'uniprot' in p:
                    #             # match uniprot id to gene with go_human or similar.
                    #             match=[r for r in self.settings.open('go_human') if p.replace('uniprotkb:','') in r]
                    #             if match:
                    #                 self.partners['HuRI'].append(match[0].split('\t')[2]) #uniprotKB	A0A024RBG1	NUDT4B		GO:0003723
                    #             else:
                    #                 warn('Unmatched',p)
                    #         else:
                    #             warn('Unmatched', p)
                    else:
                        warn('Impossible HuRI ' + row)
            for row in self.settings.open('biogrid'):
                # ID Interactor A	ID Interactor B	Alt IDs Interactor A	Alt IDs Interactor B	Aliases Interactor A	Aliases Interactor B	Interaction Detection Method	Publication 1st Author	Publication Identifiers	Taxid Interactor A	Taxid Interactor B	Interaction Types	Source Database	Interaction Identifiers	Confidence Values
                # entrez gene/locuslink:6416	entrez gene/locuslink:2318	biogrid:112315|entrez gene/locuslink:MAP2K4	biogrid:108607|entrez gene/locuslink:FLNC	entrez gene/locuslink:JNKK(gene name synonym)|entrez gene/locuslink:JNKK1(gene name synonym)|entrez gene/locuslink:MAPKK4(gene name synonym)|entrez gene/locuslink:MEK4(gene name synonym)|entrez gene/locuslink:MKK4(gene name synonym)|entrez gene/locuslink:PRKMK4(gene name synonym)|entrez gene/locuslink:SAPKK-1(gene name synonym)|entrez gene/locuslink:SAPKK1(gene name synonym)|entrez gene/locuslink:SEK1(gene name synonym)|entrez gene/locuslink:SERK1(gene name synonym)|entrez gene/locuslink:SKK1(gene name synonym)	entrez gene/locuslink:ABP-280(gene name synonym)|entrez gene/locuslink:ABP280A(gene name synonym)|entrez gene/locuslink:ABPA(gene name synonym)|entrez gene/locuslink:ABPL(gene name synonym)|entrez gene/locuslink:FLN2(gene name synonym)|entrez gene/locuslink:MFM5(gene name synonym)|entrez gene/locuslink:MPD4(gene name synonym)	psi-mi:"MI:0018"(two hybrid)	"Marti A (1997)"	pubmed:9006895	taxid:9606	taxid:9606	psi-mi:"MI:0407"(direct interaction)	psi-mi:"MI:0463"(biogrid)	biogrid:103	-
                if self.gene in row:
                    protein_set = set([re.search('locuslink:([\w\-\.]+)\|?', e.replace('\n', '')).group(1) for e in row.split('\t')[2:4]])
                    protein_set.discard(self.gene)
                    if len(protein_set) == 1:
                        matched_protein = protein_set.pop()
                        self.partners['BioGRID'].append(matched_protein)
            if len(self.ENSP) > 10:
                with self.settings.open('string') as ref:
                    for row in ref:
                        if self.ENSP in row:
                            protein_set = set(row.split())
                            protein_set.discard('9606.' + self.ENSP)
                            score = 0
                            converted_gene = ''
                            for matched_protein in protein_set:
                                if matched_protein.isdigit():
                                    score = int(matched_protein)
                                else:
                                    matched_protein = matched_protein.replace('9606.', '')
                                    with self.settings.open('ensembl') as ref:
                                        for gene in ref:
                                            if matched_protein in gene:
                                                converted_gene = gene.split('\t')[2]
                                                break
                                        else:
                                            converted_gene = matched_protein  # a lie
                            if score > 900:  # highest confidence
                                self.partners['stringDB highest'].append(converted_gene)
                            elif score > 700:  # high confidence
                                self.partners['stringDB high'].append(converted_gene)
                            elif score > 400:  # medium confidence
                                self.partners['stringDB medium'].append(converted_gene)
            with open(file, 'w') as f:
                json.dump({db: list(self.partners[db]) for db in self.partners}, f)  # makes no difference downstream
        return self


    def fetch_ENSP(self):
        """EMBL ids should vome from the Unirpto entry. However, in some cases too many it is absent."""
        for row in self.settings.open('ensembl'):
            if self.gene in row:
                if row.count(' ') > 5:
                    self.ENSP = row.split()[5]
                break
        else:
            warn('Unknown Ensembl protein id for ' + self.gene)
        return self

    def parse_all(self, mode='parallel'):
        """
        Gets all the data.
        :param mode: parallel | backgroud (=parallel but not complete) | serial (or anythign)
        :return:
        """
        tasks = {'Uniprot': self.parse_uniprot,
                 'PFam': self.parse_pfam,
                 'ELM': self.query_ELM,
                 'pLI': self.get_pLI,
                 'ExAC': self.get_ExAC,
                 'manual': self.add_manual_data,
                 'GO terms': self.fetch_go,
                 'Binding partners': self.fetch_binders}
        if mode in ('parallel','background'):
            threads = {}
            for k, fn in tasks.items():
                t = threading.Thread(target=fn)
                t.start()
                threads[k] = t
            if mode == 'parallel':
                for tn, t in threads.items():
                    t.join()
                return self
            else:
                self._threads = threads
                return self
        else:
            for task_fn in tasks.values():
                task_fn()
        return self

    def predict_effect(self):
        pass
        ##TOdo write>!

    #to do fix
    def parse_ExAC_type(self):
        if self.pLI < 0:  # error.
            self.ExAC_type='Unknown'
        elif self.pLI > max(self.pRec, self.pNull):
            self.ExAC_type ='Dominant'
        elif self.pRec > max(self.pLI, self.pNull):
            self.ExAC_type ='Recessive'
        elif self.pNull > max(self.pLI, self.pRec):
            self.ExAC_type ='None'
        else:
            self.ExAC_type ='Unknown'
        return self

    @_failsafe
    def parse_pLI(self):
        for line in csv.DictReader(self.settings.open('ExAC_pLI'), delimiter='\t'):
            # transcript	gene	chr	n_exons	cds_start	cds_end	bp	mu_syn	mu_mis	mu_lof	n_syn	n_mis	n_lof	exp_syn	exp_mis	exp_lof	syn_z	mis_z	lof_z	pLI	pRec	pNull
            if self.gene == line['gene']:
                self.pLI = float(line['pLI'])  # intolerant of a single loss-of-function variant (like haploinsufficient genes, observed ~ 0.1*expected)
                self.pRec = float(line['pRec'])  # intolerant of two loss-of-function variants (like recessive genes, observed ~ 0.5*expected)
                self.pNull = float(line['pNull'])  # completely tolerant of loss-of-function variation (observed = expected)
                self.parse_ExAC_type()
                break
        else:
            warn('Gene {} not found in ExAC table.'.format(self.gene))
        return self


    ## depraction
    def write(self, file=None):
        raise Exception('DEPRACATED. use write_uniprot')



import unittest, json, csv



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

    def test_full_parse(self):
        return 1
        print('testing serial parsing')
        irak = Protein(uniprot = 'Q9NWZ3', gene = 'IRAK4')
        irak.parse_all(mode='serial')

    def test_extend(self):
        print('testing extended')
        with open('data/human_prot_namedex.json') as f:
            namedex = json.load(f)

        def get_friend(name):
            print(name)
            try:
                friend = Protein(uniprot=namedex[name], gene=name)
                friend.parse_uniprot()
                friend.parse_pLI()
                #friend.fetch_binders()
                return friend
            except Exception as err:
                print(err)
                return None

        dock = get_friend('DOCK11')
        dock.fetch_binders()
        print(dock.partners)
        with open('Dock11_test.csv','w',newline='') as fh:
            sheet = csv.DictWriter(fh, fieldnames='name uniprot uniprot_name group disease pLI pRec pNull'.split())
            sheet.writeheader()
            friends=set([f for l in dock.partners.values() for f in l])
            for friend in friends:
                groups = [g for g in dock.partners.keys() if friend in dock.partners[g]]
                fprot = get_friend(friend)
                if fprot:
                    sheet.writerow({'name': friend,
                                    'uniprot': fprot.uniprot,
                                    'uniprot_name': fprot.uniprot_name,
                                    'group': ' | '.join(groups),
                                    'disease': ' | '.join([d['name'] for d in fprot.diseases]),
                                    'pLI': fprot.pLI,
                                    'pRec': fprot.pRec,
                                    'pNull': fprot.pNull
                    })
                else:
                    sheet.writerow({'name': friend})


if __name__ == '__main__':
    print('*****Test********')

    unittest.main()
    #irak.parse_uniprot()





















