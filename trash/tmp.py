
domains=[{
            'x': domain['location']['start'],
            'y': domain['location']['end'],
            'id': 'domain_{s}_{e}'.format(s=domain['location']['start'],e=domain['location']['end']),
            'description': domain['id']+' '+domain['accession']}
        for domain in variant.pfam]

    gnomad=[{
            'x': int(allele[0].split("-")[0]),
            'y': int(allele[0].split("-")[0]),
            'id': 'variant_{s}'.format(s=allele[0].split("-")[0]),
            'description': allele[1][0]+allele[0]+allele[1][-1]}
        for allele in variant.iter_allele() if allele[0].split("-")[0].isdigit()]

    modified=[{
            'x': resi,
            'y': resi,
            'id': 'modified_{s}'.format(s=resi),
            'description': resn} for resi, resn in variant.modified_residues]

    our=[{'x': variant.resi,
            'y': variant.resi,
            'id': 'modified_{s}'.format(s=variant.resi),
            'description': variant.mutation}]

    elm=[{
        'x': motif[0],
        'y': motif[1],
        'id': 'modified_{s}_{e}'.format(s=motif[0],e=motif[1]),
        'description': motif[2]} for motif in variant.ELM]



import os
print(os.getcwd())
print(os.path.isdir(os.path.join(os.getcwd(),'templates')))

results_template = Template(filename=os.path.join(os.getcwd(),'templates','results.mako'), format_exceptions=True,
                     lookup=TemplateLookup(directories=[os.path.join(os.getcwd(),'templates')]))










elif is_tag(elem, 'feature'):
self.modified_residues = [(feat['location']['position']['position'], feat['description']) for feat in
                          clean_dict['feature'] if feat['type'] == 'modified residue']
for i, resn in self.modified_residues:
    if i == self.resi:
        self.mutational_effect.append(
            '{self.from_resn}{self.resi} is converted into a {resn}'.format(self=self, resn=resn))
    elif self.resi - 5 < i < self.resi + 5:
        self.mutational_effect.append(
            '{self.from_resn}{self.resi} is close to {i} which is a {resn}'.format(self=self, resn=resn, i=i))
    elif self.to_resn == '*' and self.resi < i:
        self.mutational_effect.append(
            'Truncation removes {i} which is a {resn}'.format(self=self, resn=resn, i=i))



if 'comment' in clean_dict:
    for interaction in [com for com in clean_dict['comment'] if com['type'] in ('interaction', 'subunit')]:
        if 'interactant' in interaction:
            for entry in interaction['interactant']:
                if 'label' in entry:
                    self.partners['interactant'].add(entry['label'])
        if 'text' in interaction:
            self.partners['Uniprot comment'].add(get_text_part(interaction))
    for disease in [com for com in clean_dict['comment'] if com['type'] == 'disease']:  # in ('tissue specificity',
        if 'disease' in disease:
            self.disease.append(disease['disease'])
        if 'text' in disease:
            self.disease.append(get_text_part(disease))
    tissues = [com for com in clean_dict['comment'] if com['type'] == 'tissue specificity']
    if tissues:
        self.tissue = get_text_part(tissues[0])
    try:
        for ensembl in [com for com in clean_dict['dbReference'] if com['type'] == 'Ensembl']:
            if ensembl['molecule']['id'].replace('-1', '') == self.accession_list[0]:  # canonical
                for p in ensembl['property']:
                    if p['type'] == 'protein sequence ID':
                        self.ENSP = p['value']
    except:  ## Todo
        for row in self.settings.open('ensembl'):
            if self.gene in row:
                if row.count(' ') > 5:
                    self.ENSP = row.split()[5]
                break
        else:
            warn('Unknown Ensembl protein id for ' + self.gene)

if not self.Uniprot:
    self.Uniprot = clean_dict['name'][0]
self.log('Uniprot parsed {}'.format(self.Uniprot))
