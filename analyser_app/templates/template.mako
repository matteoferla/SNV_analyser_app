<%page args="variant, home,others"/>
### IGNORE THIS. THIS IS DEPRACATED AND DISUSED!
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="Protein informatics">
    <meta name="author" content="Matteo">
    <meta name="robots" content="noindex">
    <title>${variant.gene}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
          integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <link rel="stylesheet" href="${home}/../../Font-Awesome-Pro/css/all.css" crossorigin="anonymous">

    <%def name="card(title, subtitle='',body='',listitems=None, show=False, card_i=[0])">
        <%
            card_i[0]+=1
            card_id='card'+str(card_i[0])
            if show:
                (state_1,state_2)=(' show','')
            else:
                (state_2,state_1)=(' show','')
        %>
        <div class="card mb-3 shadow-sm" style="flex-grow: 2" id="${card_id}">
            <div class="card-header bg-secondary">
                <h5 class="card-title text-light">${title}  &nbsp;
                    <button class="btn btn-dark float-right" type="button" data-toggle="collapse" data-target="#${card_id} .collapse">
                        <span class="collapse${state_2}"><i class="far fa-book-open"></i> Show</span>
                        <span class="collapse${state_1}"><i class="far fa-book"></i> Hide</span>
                    </button>
                </h5>
                % if subtitle:
                    <h6 class="card-subtitle mb-2 text-body">${subtitle}</h6>
                % endif
                    </div>
                <div class="card-body collapse${state_1}">
                % if body:
                    <p class="card-text">${body}</p>
                % endif
                % if listitems:
                    <ul class="list-group list-group-flush">
                    % for a in listitems:
                        %if len(a) == 3: ##tuple of enboldened title, value and html-id
                        <li class="list-group-item" id="${a[2]}"><b>${a[0]}: </b>&nbsp; &nbsp;${a[1]}</li>
                        %elif len(a) ==2: ##tuple of enboldened title, value
                        <li class="list-group-item"><b>${a[0]}: </b>&nbsp; &nbsp;${a[1]}</li>
                        %else: ##tuple of value
                        <li class="list-group-item">${a[0]}</li>
                        %endif
                    % endfor
                    </ul>
                % endif
                    <!--preserve this bit just in case
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                      <button type="button" class="btn btn-sm btn-outline-secondary">View</button>
                      <button type="button" class="btn btn-sm btn-outline-secondary">Edit</button>
                    </div>
                    <small class="text-muted">9 mins</small>
                  </div>-->
                </div>
            </div>
    </%def>
</head>
<body>

<%include file="layout_components/header.mako" args="home=home,others=others"/>

<main role="main">

    <section class="jumbotron text-center">
        <div class="container">
            <h1 class="jumbotron-heading">${variant.gene} ${variant.mutation}</h1>
            <p class="lead text-muted">${variant.fullname}</p>
        </div>
    </section>

    <div class="album py-5 bg-light">
        <div class="container">

            <div class="card-columns" style="column-count: 2;"> <!--not row! Masonry-style-->

                <!-- Error -->
                <div id="error_div" class="hidden">
                    ${card(
                        title='<i class="fas fa-bug"></i> Error',
                        subtitle='Client-side error',
                        body='<p id="error_p"></p>'
                    )}
                </div>

                <!-- User data -->
                % if variant.user_text:
                    ${card(
                    title='<i class="fas fa-user-tag"></i> User generated content',
                    subtitle='Manual annotations for {}'.format(variant.fullname),
                    body=variant.user_text,
                    show=True
                )}
                % endif

                <!-- mutation card -->
                ${card(
                    title='<i class="fas fa-band-aid"></i> Mutation',
                    subtitle='Predicted effects of {}'.format(variant.mutation),
                    body='',
                    show=True,
                    listitems=[('From', '{f}<br/><b>Residue index:</b>&nbsp; &nbsp;{i}<br/><b>To:</b>&nbsp; &nbsp;{t}'.format(f=variant.from_resn,
                                                                                                      i=variant.resi,
                                                                                                      t=variant.to_resn)),
                        ('Mutational effects',
                        ''.join(['<br/>&nbsp;<i class="fas fa-chevron-right"></i> {}'.format(a) for a in
                                 variant.mutational_effect])),
                        ('Blossum score',variant.blossum_score)
                       ]
                )}

                <!-- case notes -->
                <%
                    if 'case_log' in variant.other and variant.other['case_log']:
                        case_log =  [(str(entry['CaseLogDate']) +' '+str(entry['CaseLogKind']),str(entry['CaseLogEntry']) + ('<i>'+str(entry['CaseLogCreatedBy'])+'/'+str(entry['CaseLogLastEditBy'])+'</i>')) for entry in variant.other['case_log']]
                    else:
                        case_log = None
                    if 'caseNotes' not in variant.other:
                        variant.other['caseNotes']=''

                %>
                % if variant.other['caseNotes'] or case_log:
                    ${card(
                        title='<i class="fas fa-sticky-note"></i> Case notes',
                        subtitle='Notes for the whole patient case {}'.format(variant.other['caseLocalIdentifier']),
                        body=variant.other['caseNotes'],
                        listitems=case_log
                    )}
                % endif

                <!-- pfam -->
                ${card(
                    title='<i class="fas fa-map-signs"></i> Pfam domains',
                    subtitle='Pfam info for {}'.format(variant.gene),
                    body='<p><a href=http://www.rcsb.org/pdb/protein/{0} target="_blank" >PDB page for {0} <i class="fas fa-external-link-square"></i></a></p><svg id="pfam_gfx" width="100%" height="50px" ></svg>'.format(variant.accession_list[0] if variant.accession_list else variant.Uniprot),
                    listitems=[('<a target="_blank" href="https://pfam.xfam.org/family/{0}">{0} <i class="fas fa-external-link-square"></i></a> {1}'.format(x['accession'],x['id']),'{0}-{1}'.format(x['location']['start'],x['location']['end']),x['accession']) for x in variant.pfam]
                )}

                <!-- PDB card -->
                % if variant.pdb_file:
                    ${card(
                    title='<i class="fas fa-cubes"></i> Structure',
                    show=True,
                    subtitle='User generated PDB file <a href="{1}/{0}.pdb"  download>{0} <i class="fas fa-external-link-square"></i></a>'.format(variant.gene, home),
                    body='<div id="viewport" style="width:100%; height: 0; padding-bottom: 100%;"></div>'
                )}
                % elif variant.pdb_code:
                    ${card(
                    title='<i class="fas fa-cubes"></i> Structure',
                    show=True,
                    subtitle='PDB file <a target="_blank" href="https://www.rcsb.org/structure/{0}">{0} <i class="fas fa-external-link-square"></i></a>'.format(variant.pdb_code),
                    body='<div id="viewport" style="width:100%; height: 0; padding-bottom: 100%;"></div>'
                )}
                % endif


                <!-- structure card -->
                ${card(
                    title='<i class="fas fa-archway"></i> Other Structural data',
                    subtitle='Structure for {}'.format(variant.gene),
                    listitems=[('Closest crystallised protein spanning the mutation','{m} (score: {s}, from: {f}, len: {l})'.format(m=variant.match,s=variant.match_score,f=variant.match_start,l=variant.match_start)),
                            ('PFAM (via Uniprot)',variant.Uniprot_pfam),
                            ('PFAM (via Genbank)',variant.NCBI_pfam),
                            ('Genbank regions',variant.NCBI_regions)]
                )}

                <!-- binding partners -->
                % if any(variant.partners.values()):
                    ${card(
                    title='<i class="fas fa-handshake-alt"></i> Interactions',
                    subtitle='Interactions for {0}'.format(variant.gene),
                    listitems=[(db,', '.join(sorted(variant.partners[db]))) for db in ('HuRI','interactant','SSL','BioGRID','Uniprot comment','stringDB highest','stringDB high','stringDB medium') if db in variant.partners]
                )}
                % endif

                <!-- disease -->
                % if variant.disease:
                    <%
                    disease_list=[]
                    for disease in variant.disease:
                        if isinstance(disease,dict):
                            if 'dbReference' in disease and disease['dbReference']['type']=='MIM':
                                disease['link']=int(disease['dbReference']["id"])
                                disease_body = 'Uniprot lists <a href="https://www.omim.org/entry/{link}" data-toggle="tooltip" title="{description}">{name}</a> as the cause'.format(**disease)
                            else:
                                disease_body = 'Uniprot lists <span data-toggle="tooltip" title="{description}">{name}</span> as the associated disease'.format(**disease)
                            if 'CaseDisease' in variant.other:
                                disease_body+=', while the Case has '+variant.other['CaseDisease']
                            disease_list.append((disease['acronym'],disease_body))
                        else:
                            disease_list.append(('Text',disease))
                    %>
                    ${card(
                    title='<i class="fas fa-briefcase-medical"></i> Disease',
                    subtitle='Disease info for {0}'.format(variant.gene),
                    body='<p>'+variant.tissue+'</p>',
                    listitems=disease_list
                )}
                % endif

                <!-- seq card -->
                ${card(
                    title='<i class="fas fa-dna"></i> Sequence',
                    subtitle='Amino acid sequence of the chosen isoform',
                    body='<div id="sequence-viewer"></div>'
                )}

                <!--GO-->
                % if variant.go_terms:
                    ${card(
                    title='<i class="fas fa-chess-knight"></i> GO terms',
                    subtitle='Gene ontology terms for the gene {0}'.format(variant.gene),
                    listitems=[(term.id,'({0}) {1}'.format(term.namespace, term.name)) for term in variant.go_terms]
                )}
                % endif

                <!-- pLI -->
                ${card(
                    title='<i class="fas fa-leaf"></i> ExAC data',
                    subtitle='Healthy individual data for {}'.format(variant.gene),
                    body='<a target="_blank" href="http://exac.broadinstitute.org/gene/{0}">ExAC Link <i class="fas fa-external-link-square"></i></a>'.format(variant.ENSG),
                    listitems=[('pLI',round(variant.pLI*100)/100),
                                ('pRec',round(variant.pRec*100)/100),
                                ('pNull',round(variant.pNull*100)/100)]
                )}

                <!-- parsed card -->
                ${card(
                    title='<i class="fas fa-flask"></i> Parsed data',
                    subtitle='Gathered data about {}'.format(variant.gene),
                    listitems=[('Transcript ID',variant.ResultTranscriptID),
                            ('Protein ID','<a href=https://www.ncbi.nlm.nih.gov/protein/{0} target="_blank" >{0} <i class="fas fa-external-link-square"></i></a> (NCBI) &mdash; <a target="_blank" href="https://www.uniprot.org/uniprot/{1}">{1} <i class="fas fa-external-link-square"></i></a>  (Uniprot) {2} (Uniprot name)'.format(variant.protein_id,variant.Uniprot,variant.Uniprot_name)),
                            ('Transcript variant ID list',' &mdash; '.join(['<a target="_blank" href="https://www.uniprot.org/uniprot/{0}">{0} <i class="fas fa-external-link-square"></i></a>'.format(a) for a in variant.accession_list])),
                            ('Protein description',variant.description),
                            ('GO terms',variant.GO),
                            ('Modified residues',variant.modified_residues),
                            ('Miscellaneous uniprot data',variant.Uniprot_data)]
                )}

                <!-- metadata card -->
                ${card(
                    title='<i class="far fa-address-card"></i> Metadata',
                    subtitle='Data from HICF2 Tracker DB for ID {}'.format(variant.resultID),
                    listitems=[(k,variant.other[k]) for k in variant.other]
                )}

                <!-- log card -->
                ${card(
                    title='<i class="fas fa-cogs"></i> Log',
                    subtitle='Logged data from the script',
                    listitems=[(i,a) for i,a in enumerate(variant.logbook)]
                )}

                <!-- Template -->
                <% '''
                ${card(
                    title='template card',
                    subtitle='xxxx {}'.format(0),
                    body='XXXX',
                    listitems=[('a','A'),
                            ('B','b')]
                )}'''
                %>

            </div> <!-- card column-->
        </div>
    </div>

</main>

<footer class="text-muted">
    <div class="container">
        <p class="float-right">
            <a href="#">Back to top</a>
        </p>
        <p>This data is confidential and experimental, please do not distribute.</p>
    </div>
</footer>

 <%include file="code.mako" args="home=home,others=others"/>

<!-- local -->
<script src="sequence-viewer.js" type="text/javascript"></script>
<script src="ngl.js" type="text/javascript"></script>
<!-- code -->
<script type="text/javascript" >
$( document ).ready(function() {
    try {
        $('#error_div').hide();
        // Seq viever
        var seq = new Sequence("${variant.seq}");
        seq.render('#sequence-viewer',{'toolbar': true,'charsPerLine': 50,'search': true,'title':'${variant.protein_id} &nbsp;'});
        seq.selection(${variant.resi}-1, ${variant.resi}, 'red');
        seq.addLegend([{color: 'red', name: '${variant.mutation}'}]);
        // domain layout
        function domain_graphics() {
            var svg=d3.select('#pfam_gfx');
            //if (! d3.select("#arrows").empty()) {d3.select("#arrows").remove()}
            // midline
            svg.append("svg:line")
                    .attr("x1", 0)
                    .attr("y1", 25)
                    .attr("x2", "100%")
                    .attr("y2", 25)
                    .attr("stroke-width",3)
                    .attr('stroke','black');
            // load data
            var pfam = ${variant.pfam};
            var l=${variant.protein_length};
            // parse
            //e.g. {'location': {'start': 214.0, 'end': 299.0, 'ali_start': 216.0, 'ali_end': 298.0, 'hmm_start': 3.0, 'hmm_end': 86.0, 'evalue': '4.3e-12', 'bitscore': 56.2}, 'accession': 'PF00047', 'id': 'ig', 'type': 'Pfam-A'}
            pfam.forEach(function(element) {
                var group=svg.append("g");
                group.append('rect')
                        .attr('x',(parseFloat(element.location.start)/l*100).toString()+"%")
                        .attr('width',((parseFloat(element.location.end)-parseFloat(element.location.start))/l*100).toString()+'%')
                        .attr("y", 5)
                        .attr("height", 40)
                        .attr("stroke-width",1)
                        .attr('stroke','black')
                        .attr('fill','gainsboro');
                group.attr('title',element.id);
                group.attr('data-toggle','tooltip');
                group.on("mouseover", function() {
                        $('#'+element.accession).addClass('list-group-item-primary');
                    })
                    .on("mouseout", function() {
                        $('#'+element.accession).removeClass('list-group-item-primary');
                    });
            });
            var group_allele=svg.append("g");
            % for allele in variant.iter_allele():
                % if allele[0].split("-")[0].isdigit():
                    var xa='${int(allele[0].split("-")[0])/len(variant.seq)*100}%';
                    group_allele.append('line')
                        .attr('x1',xa)
                        .attr('x2',xa)
                        .attr('y1',20)
                        .attr('y2',50)
                        .attr("stroke-width",2)
                            % if allele.count('/') > 0 and allele[1].split('/')[1] in ['X','*','_','fs','del']:
                        .attr('stroke','coral')
                            % else:
                        .attr('stroke','gold')
                            % endif
                        .attr('title','${''.join(allele)}')
                        .attr('data-toggle','tooltip');
                % endif
            % endfor
            var x1=${variant.resi}/l*100;
            var x=x1.toString()+'%';
            group_allele.append('line')
                    .attr('x1',x)
                    .attr('x2',x)
                    .attr('y1',0)
                    .attr('y2',50)
                    .attr("stroke-width",3)
                    .attr('stroke','indianred')
                    .attr('title','${variant.clean_mutation}')
                    .attr('data-toggle','tooltip');

        }
        domain_graphics();
        // NGL
        % if variant.allele_residues:
            var alleles = new NGL.Selection( "${' or '.join([str(i) for (f,i,t) in variant.allele_residues])}" );
        % else:
            var alleles = 0;
        % endif

        function show_mutant(obj) {
            % if variant.pdb_chain:
                var resi=':${variant.pdb_chain} and '+(${variant.resi}).toString();
            % else:
                var resi=(${variant.resi}).toString();
            % endif
            var selection = new NGL.Selection( resi );
            var radius = 5;
            var atomSet = obj.structure.getAtomSetWithinSelection( selection, radius );
            // expand selection to complete groups
            var atomSet2 = obj.structure.getAtomSetWithinGroup( atomSet );
            obj.addRepresentation( "licorice", { sele: atomSet2.toSeleString()} );
            obj.addRepresentation( "hyperball", { sele: resi} );
            obj.addRepresentation( "cartoon" );
            % if variant.has_allele_pdb_file:
                obj.addRepresentation( "licorice", { sele: alleles.string} );
            % endif
            window.zoom=atomSet2.toSeleString();
            obj.autoView(window.zoom);
        }
        function show_alleles(obj) {
            var schemeId = NGL.ColormakerRegistry.addSelectionScheme([
            ["salmon", "_C"],
            ["red", "_O"],
            ["yellow", "_S"],
            ["blue", "_N"],
            ["white", "*"]
            ], "Mutant");
            obj.removeAllRepresentations();
            obj.addRepresentation( "licorice", { sele: alleles.string, color: schemeId} );
            obj.autoView(window.zoom);
        }
        // load stage
        % if variant.pdb_file or variant.pdb_code:
            var stage = new NGL.Stage( "viewport",{backgroundColor: "white"});
            window.stage = stage;
            stage.setParameters({backgroundColor: "white"});
            window.addEventListener( "resize", function( event ){stage.handleResize();}, false );
        % endif
        % if variant.has_allele_pdb_file:
            stage.loadFile( "${home}/${variant.gene}_allele.pdb", { defaultRepresentation: true } ).then(function (o) {show_alleles(o);window.allele=o});
        % endif
        % if variant.pdb_file: ##okay, this is problematic and should be coded differently...
            stage.loadFile( "${home}/${variant.gene}.pdb", { defaultRepresentation: true } ).then(function (o) {show_mutant(o);window.pdb=o});
        % elif variant.pdb_code:
            stage.loadFile( "rcsb://${variant.pdb_code}", { defaultRepresentation: true } ).then(function (o) {show_mutant(o);window.pdb=o});
        % endif
        //throw "No errors.";
        if (!! window.stage) {stage.autoView(window.zoom);}
    $('[data-toggle="tooltip"]').tooltip();
    }
    catch (error) {
        console.log(error);
        $('#error_div').removeClass('hidden');
        $('#error_div').show();
        $('#error_p').text(error);
    }
});
</script>

<%include file="code.mako" args="home=home,others=others"/>

</body>
</html>
