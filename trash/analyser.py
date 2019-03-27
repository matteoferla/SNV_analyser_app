##################### JUSNK




def parse_uniprot(xml):
    return _read_xml('Uniprot', xml)


def parse_pfam(xml):
    return _read_xml('Pfam', xml)


def _read_xml(mode, xml):
    """
    This is weird. Uniprot works fine getting it parsed via its XML schema, while Pfam fails even with validation = lax.
    So the Pfam data uses stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree
    and not schema. I favour the latter as it ain't a just a snippet from SO, but the latter seems okay.
    I looked at how https://github.com/prody/ProDy/blob/master/prody/database/pfam.py does it and they
    simply returns the ET root yet say it returns a dictionary. :-S
    :param mode: 'Uniprot' | 'Pfam'
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

    sch_URL = {'Uniprot': 'https://www.uniprot.org/docs/uniprot.xsd',
               'Pfam': 'https://pfam.xfam.org/static/documents/schemas/protein.xsd'}[mode]

    etx = ET.XML(xml)
    if mode == 'Uniprot':
        schema = xmlschema.XMLSchema(sch_URL)
        entry_dict = schema.to_dict(etx)['{http://uniprot.org/uniprot}entry'][0]
    elif mode == 'Pfam':
        protoentry_dict = etree_to_dict(etx)
        if '{https://pfam.xfam.org/}matches' in protoentry_dict['{https://pfam.xfam.org/}pfam'][
            '{https://pfam.xfam.org/}entry']:
            entry_dict = protoentry_dict['{https://pfam.xfam.org/}pfam']['{https://pfam.xfam.org/}entry'][
                '{https://pfam.xfam.org/}matches']['{https://pfam.xfam.org/}match']
        else:
            entry_dict = []
    else:
        raise ValueError
    damn = {'Uniprot': '{http://uniprot.org/uniprot}', 'Pfam': '{https://pfam.xfam.org/}'}[mode]
    return deep_clean(entry_dict, damn)





# print(parse_uniprot(open(uniprot_master_file).read()))
