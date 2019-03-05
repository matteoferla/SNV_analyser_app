<script type="text/javascript">
// feature
//fix d3 version issue.
//d3.scale={linear: d3.scaleLinear};
<%
    print(protein.features)
    print(protein.features.keys())
%>
window.ft = new FeatureViewer('${protein.sequence}',
           '#fv',
            {
                showAxis: true,
                showSequence: true,
                brushActive: true, //zoom
                toolbar:true, //current zoom & mouse position
                bubbleHelp:false,
                zoomMax:50 //define the maximum range of the zoom
            });

%if protein.mutation is not None:
	ft.addFeature({
        data: [{'x':${protein.mutation.residue_index},'y': ${protein.mutation.residue_index}, 'id': 'our_${protein.mutation.residue_index}', 'description': 'p.${str(protein.mutation)}'}],
        name: "Candidate SNP",
        className: "our_SNP",
        color: "indianred",
        type: "unique",
        filter: "Variant"
    });
%endif

			
%if protein.pdbs:
    ft.addFeature({
        data: ${str(protein.pdbs)|n},
        name: "Crystal structures",
        className: "pdb",
        color: "lime",
        type: "rect",
        filter: "Domain"
    });
%endif

%if 'domain' in protein.features:
    ft.addFeature({
        data: ${str(protein.features['domain'])|n},
        name: "Domain",
        className: "domain",
        color: "lightblue",
        type: "rect",
        filter: "Domain"
    });
%endif

<%
    combo=[]
    for key in ('transmembrane region','intramembrane region','region of interest','peptide','site','active site','binding site','calcium-binding region','zinc finger region','metal ion-binding site','DNA-binding region','lipid moiety-binding region', 'nucleotide phosphate-binding region'):
        if key in protein.features:
            combo.extend(protein.features[key])
%>
%if combo:
    ft.addFeature({
        data: ${str(combo)|n},
        name: "region of interest",
        className: "domain",
        color: "teal",
        type: "rect",
        filter: "Domain"
    });
%endif

<%
    combo=[]
    for key in ('propeptide','signal peptide','repeat','coiled-coil region','compositionally biased region','short sequence motif','topological domain','transit peptide'):
        if key in protein.features:
            combo.extend(protein.features[key])
    print(combo)
%>
%if combo:
    ft.addFeature({
        data: ${str(combo)|n},
        name: "other regions",
        className: "domain",
        color: "lavender",
        type: "rect",
        filter: "Domain"
    });
%endif

<%
    combo=[]
    for key in ('initiator methionine','modified residue','glycosylation site','non-standard amino acid'):
        if key in protein.features:
            combo.extend(protein.features[key])
%>
%if combo:
    ft.addFeature({
        data: ${str(combo)|n},
        name: "Modified residues",
        className: "modified",
        color: "slateblue",
        type: "unique",
        filter: "Modified"
    });
%endif

<%
    combo=[]
    for key in ('helix', 'turn', 'strand'):
        if key in protein.features:
            combo.extend(protein.features[key])
%>
%if combo:
    ft.addFeature({
        data: ${str(combo)|n},
        name: "Secondary structure",
        className: "domain",
        color: "olive",
        type: "rectangle",
        filter: "Domain"
    });
%endif



%if 'sequence variant' in protein.features:
    ft.addFeature({
        data: ${str(protein.features['sequence variant'])|n},
        name: "seq. variant",
        className: "modified",
        color: "firebrick",
        type: "unique",
        filter: "Modified"
    });
%endif

%if 'disulfide bond' in protein.features:
    ft.addFeature({
        data: ${str(protein.features['disulfide bond'])|n},
        name: "disulfide bond",
        className: "dsB",
        color: "orange",
        type: "path",
        filter: "Modified Residue"
    });
%endif

%if 'cross-link' in protein.features:
    ft.addFeature({
        data: ${str(protein.features['cross-link'])|n},
        name: "disulfide bond",
        className: "dsB",
        color: "orange",
        type: "path",
        filter: "Modified Residue"
    });
%endif

$('.domain,.dsB').each(function () {
        var id = $(this)[0].id;
        var ab = id.split('_')[1];
        var ad = id.split('_')[2];
        $(this).css('cursor', 'pointer');
        $(this).click(function () {
            NGL.specialOps.show_domain('viewport', ab+'-'+ad+':'+ops.current_chain);
        });
    });



$('.variant,.modified,.our_SNP').each(function () {
        var id = $(this)[0].id;
        var ab = id.split('_')[1] + ops.current_chain;
        $(this).css('cursor', 'pointer');
        $(this).click(function () {
            NGL.specialOps.show_residue('viewport', ab+':'+ops.current_chain);
        });
    });

//structure
% if protein.pdbs:
    var stage = new NGL.Stage( "viewport",{backgroundColor: "white"});
    window.stage = stage;
    window.addEventListener( "resize", function( event ){stage.handleResize();}, false );
    stage.loadFile( "rcsb://${protein.pdbs[0]['description'].lower()}", { defaultRepresentation: true } );//.then(function (o) {show_mutant(o);window.pdb=o});
    NGL.stageIds['viewport'] = stage;
    ops.current_chain = '${protein.pdbs[0]['id'].split('_')[1]}';
% endif


$('#new_analysis').click(function () {
    $('#retrieval_card').show(1000);
    $('#input_card').show(1000);
    $('#results').detach();
});

</script>
