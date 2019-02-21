import os, pickle
from warnings import warn
from ET_monkeypatch import ET

#######################
class Protein:
    """
    This class handles each protein entry from Uniprot. See __init__ for the list of variables stored.
    NB. The ET.Element has to be monkeypatched. See `help(ElementalExpansion)`
    """
    error_tollerant = False

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
            #self.Uniprot_pfam = [(xref['id'], xref['property'][0]['value']) for xref in clean_dict[''] if xref['type'] == 'Pfam']
        elif elem.has_attr('type','GO'):
            pass
            #self.GO = [(xref['id'], xref['property'][0]['value']) for xref in clean_dict['dbReference'] if xref['type'] == 'GO']

    @_failsafe
    def _parse_protein_gene(self, elem):
        for name_el in elem:
            if name_el.is_tag('name'):
                if name_el.has_attr('type', 'primary'):
                    self.gene_name = name_el.text
                elif name_el.has_attr('type', 'synonym'):
                    self.alt_gene_name_list.append(name_el.text)

    def __init__(self, entry):
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
        ### fill
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
                pass
            elif elem.is_tag('comment'):
                pass
            elif elem.is_tag('keyword'):
                pass

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

    def write(self, file=None):
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



