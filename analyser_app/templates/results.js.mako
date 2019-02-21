<script type="text/javascript">
// feature
//fix d3 version issue.
//d3.scale={linear: d3.scaleLinear};
window.ft = new FeatureViewer('${variant.seq}',
           '#fv',
            {
                showAxis: true,
                showSequence: true,
                brushActive: true, //zoom
                toolbar:true, //current zoom & mouse position
                bubbleHelp:false,
                zoomMax:50 //define the maximum range of the zoom
            });

<%
    domains=str([{
            'x': domain['location']['start'],
            'y': domain['location']['end'],
            'id': 'domain_{s}_{e}'.format(s=domain['location']['start'],e=domain['location']['end']),
            'description': domain['id']+' '+domain['accession']}
        for domain in variant.pfam])

    gnomad=str([{
            'x': int(allele[0].split("-")[0]),
            'y': int(allele[0].split("-")[0]),
            'id': 'variant_{s}'.format(s=allele[0].split("-")[0]),
            'description': allele[1][0]+allele[0]+allele[1][-1]}
        for allele in variant.iter_allele() if allele[0].split("-")[0].isdigit()])

    modified=str([{
            'x': resi,
            'y': resi,
            'id': 'modified_{s}'.format(s=resi),
            'description': resn} for resi, resn in variant.modified_residues])

    our=str([{'x': variant.resi,
            'y': variant.resi,
            'id': 'modified_{s}'.format(s=variant.resi),
            'description': variant.mutation}])

    elm=str([{
        'x': motif[0],
        'y': motif[1],
        'id': 'modified_{s}_{e}'.format(s=motif[0],e=motif[1]),
        'description': motif[2]} for motif in variant.ELM])

%>

% if our:
    ft.addFeature({
        data: ${our|n},
        name: "Candidate SNP",
        className: "our_SNP",
        color: "indianred",
        type: "unique",
        filter: "Variant"
    });
% endif

%if domains:
    ft.addFeature({
        data: ${domains|n},
        name: "Domain",
        className: "domain",
        color: "lightblue",
        type: "rect",
        filter: "Domain"
    });
%endif

% if gnomad:
    ft.addFeature({
        data: ${gnomad|n},
        name: "gNOMAD",
        className: "variant",
        color: "lightblue",
        type: "unique",
        filter: "gNOMAD"
    });
% endif

% if modified:
    ft.addFeature({
        data: ${modified|n},
        name: "Modified residues",
        className: "modified",
        color: "slateblue",
        type: "unique",
        filter: "Modified"
    });
% endif

% if elm:
    ft.addFeature({
        data: ${elm|n},
        name: "Motif prediction",
        className: "elm",
        color: "lavender",
        type: "rect",
        filter: "ELM"
    });
% endif



$('.domain,.elm').each(function () {
        var id = $(this)[0].id;
        var ab = id.split('_')[1];
        var ad = id.split('_')[2];
        $(this).css('cursor', 'pointer');
        $(this).click(function () {
            show_region(ab, ad);
        });
    });



$('.variant,.modified,.our_SNP').each(function () {
        var id = $(this)[0].id;
        var ab = id.split('_')[1];
        $(this).css('cursor', 'pointer');
        $(this).click(function () {
            show_residue(ab);
        });
    });

//$('.header-help').removeAttr('type'); //fix help formatting.
$('.svgHeader').append(`<div class="btn-group">
  <label class="btn btn-secondary active fake-checkbox" checked id='gNOMAD_checkbox'> gNOMAD</label>
  <label class="btn btn-secondary active fake-checkbox" checked id='ELM_checkbox'> ELM</label>
</div>`);

$('.fake-checkbox[checked]').prop("checked",true); // not sure why checked does nothing. its an attribute not a prop unless it's a real checkbox?
$('.fake-checkbox').click(function () {
    $(this).prop("checked", ! $(this).prop("checked"));
    if ($(this).prop("checked") == true) {
        $(this).addClass('btn-secondary');
        $(this).addClass('active');
        $(this).removeClass('btn-light');
    } else {
        $(this).addClass('btn-light');
        $(this).removeClass('btn-secondary');
        $(this).removeClass('active');
    }
});

$('#gNOMAD_checkbox').click(function () {
    if ($(this).prop("checked") == true) {
        $('.variant').hide(); $('.linevariant').hide();
    } else {$('.variant').show(); $('.linevariant').show();}
});

$('#ELM_checkbox').click(function () {
    if ($(this).prop("checked") == true) {
        $('.elm').hide(); $('.lineelm').hide();
    } else {$('.elm').show(); $('.lineelm').show();}
});





function show_mutant(obj) {
        % if variant.pdb_chain:
            var resi=':${variant.pdb_chain} and '+(${variant.resi}).toString();
        % else:
            var resi=(${variant.resi}).toString();
        % endif
        show_residue(resi, obj);
    }

function show_region(ab,ad, protein) {
    protein = (typeof protein === 'undefined') ? stage.compList[0] : protein;
    protein.removeAllRepresentations();
    var schemeId = NGL.ColormakerRegistry.addSelectionScheme([["green", ab.toString()+'-'+ad.toString()],["white", "*"]]);
    protein.addRepresentation( "cartoon", {color: schemeId });
    protein.autoView();
}

function show_residue(resi, protein) {
    protein = (typeof protein === 'undefined') ? stage.compList[0] : protein;
    var selection = new NGL.Selection( resi );
    var schemeId = NGL.ColormakerRegistry.addSelectionScheme([
        ["lightblue",'_C'],["blue",'_N'],["red",'_O'],["white",'_H'],["yellow",'_S'],["orange","*"]
    ]);
    var radius = 5;
    var atomSet = protein.structure.getAtomSetWithinSelection( selection, radius );
    // expand selection to complete groups
    var atomSet2 = protein.structure.getAtomSetWithinGroup( atomSet );
    protein.addRepresentation( "licorice", { sele: atomSet2.toSeleString()} );
    protein.addRepresentation( "hyperball", { sele: resi, color: schemeId} );
    protein.addRepresentation( "cartoon" );
    % if variant.has_allele_pdb_file:
        protein.addRepresentation( "licorice", { sele: alleles.string} );
    % endif
    window.zoom=atomSet2.toSeleString();
    protein.autoView(window.zoom);
}

//structure
% if variant.pdb_file or variant.pdb_code:
    var stage = new NGL.Stage( "viewport",{backgroundColor: "white"});
    window.stage = stage;
    stage.setParameters({backgroundColor: "white"});
    window.addEventListener( "resize", function( event ){stage.handleResize();}, false );
% endif
% if variant.pdb_file: ##okay, this is problematic and should be coded differently...
    ### todo get ${home} to work...
    stage.loadFile( "${variant.gene}.pdb", { defaultRepresentation: true } ).then(function (o) {show_mutant(o);window.pdb=o});
% elif variant.pdb_code:
    stage.loadFile( "rcsb://${variant.pdb_code}", { defaultRepresentation: true } ).then(function (o) {show_mutant(o);window.pdb=o});
% endif
</script>
