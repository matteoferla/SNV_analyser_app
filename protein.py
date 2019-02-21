import os, pickle
from warnings import warn
from ET_monkeypatch import ET
from settings_handler import global_settings



#######################
class Protein:
    """
    This class handles each protein entry from Uniprot. See __init__ for the list of variables stored.
    It fills them from various other sources.

        >>> Protein()
        >>> Protein(xml_entry) # equivalent to Protein()._parse_unicode_xml(xml_entry)
        >>> Protein.load(filename)

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
            if item not in self.other:
                warn('Accessed non-existant attribute {item} for {v.gene}. Likely cause the code changed, but the from_pickle flag is True.'.format(v=self, item=item))
                self.__dict__[item] = 'STALE PICKLE!'
            else:
                warn('Accessed attribute in other list. The keys read are kept controlled in the case someone has a candiate not in tracker to check!')
                self.__dict__[item] = self.other[item]
        return self.__dict__[item]

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
            if chain:  ## this is so unpredictable. It needs to be done by blast.
                loca=chain.attrib['value'].split('=')[1].split('-')
                self.pdbs.append({'description': elem.attrib['id'], 'id': elem.attrib['id'], 'x': loca[0], 'y': loca[1]})
        elif elem.has_attr('type', 'Ensembl'):
            self.ENST = elem.attr['id']
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

    def fetch_ENSP(self):
        for row in self.settings.open('ensembl'):
            if self.gene in row:
                if row.count(' ') > 5:
                    self.ENSP = row.split()[5]
                return self
        else:
            warn('Unknown Ensembl protein id for ' + self.gene)

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
                    if partner:
                        self.partners['interactant'].append(partner.text)
                elif subelem.is_tag('text'):  ## some entries are badly annotated and have only a text line..
                    self.partners['interactant'].append(subelem.text)
        elif elem.has_attr('type','disease'):
            for subelem in elem:
                if subelem.is_tag('disease'): #yes. the comment type=disease has a tag disease. wtf
                    disease = {'id': subelem.attrib['id']}
                    for key in ('description', 'name'):
                        subsub = subelem.get_subtag(key)
                        if subsub:
                            disease[key] = subsub.text
                    mim = subelem.get_sub_by_type('MIM')
                    if min:
                        disease['MIM'] = min.attrib['id']
                    self.disease.append(disease)

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
        if not location:
            return None
        position = location.get_subtag('position').attrib['position']
        start = location.get_subtag('start').attrib['position']
        end =  location.get_subtag('end').attrib['position']
        if position:  # single residue
            return {'x': position, 'y': position, 'description': elem.attr['description'], 'id': '{t}_{s}'.format(s=position, t=elem.attrib['type'].replace(' ','').replace('-',''))}
        elif start and end:  # region or disulfide
            return {'x': start, 'y': end, 'description': elem.attr['description'], 'id': '{t}_{s}_{e}'.format(s=start, e=end, t=elem.attrib['type'].replace(' ', '').replace('-',''))}

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

    def __init__(self, entry=None):
        ### predeclaration (and cheatsheet)
        self.xml = entry
        self.gene_name = ''
        self.uniprot_name = '' ## S39AD_HUMAN
        self.alt_gene_name_list = []
        self.accession_list = [] ## Q96H72 etc.
        self.sequence = ''
        self.recommended_name = '' #Zinc transporter ZIP13
        self.alternative_fullname_list = []
        self.alternative_shortname_list = []
        self.features=[]
        self.partners ={'interactant': []} # lists not sets as it gave a pickle issue.
        ### fill
        if entry:
            self._parse_uniprot_xml(entry)

    def dump(self, file=None):
        if not file:
            file = os.path.join(self.settings.pickle_folder, '{0}.p'.format(self.uniprot_name))
        pickle.dump(self.__dict__, open(file, 'wb'))
        self.log('Data saved to {} as pickled dictionary'.format(file))

    @classmethod
    def load(cls, file, verbose=None):
        self = cls.__new__(cls)
        self.__dict__ = pickle.load(open(file, 'rb'))
        if verbose != None:
            self.verbose = verbose
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






















    ## depraction
    def write(self, file=None):
        raise Exception('DEPRACATED. use write_uniprot')



