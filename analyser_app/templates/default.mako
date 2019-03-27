<%inherit file="layout.mako"/>

<%block name="topmost">
    <section class="jumbotron text-center">
        <div class="container">
            <h1 class="jumbotron-heading">SNV analyser</h1>
            <p class="lead text-muted">This tool gathers information from various sources about a gene and ranks possible effect a SNV may have.
                <br/>(signal peptide loss, binding site, active site or ddG)</p>
        </div>
    </section>
</%block>



################ main


<div class="card shadow-sm" id="input_card">
    <h3 class="card-header">Input new</h3>
    <div class="card-body">
        <div class="row">
            ### gene
            <div class="col-12 col-lg-6">
                <div class="input-group mb-3">
        <div class="input-group-prepend">
            <label class="input-group-text" id="gene_label">Gene name </label>
        </div>
        <input type="text" class="form-control" placeholder="gene name" aria-label="gene name" aria-describedby="gene_label" id="gene" value="IGF2">
                    <div class="invalid-feedback">Gene name not recognised.</div>
                    <div class="valid-feedback">Gene name accepted.</div>
        </div>
            </div>
            ### mutation
            <div class="col-6 col-lg-3">
                <div class="input-group mb-3">
        <div class="input-group-prepend">
            <label class="input-group-text" id="mutation_label">missense </label>
        </div>
        <input type="text" class="form-control" placeholder="p.M1M" aria-label="mutation" aria-describedby="mutation_label" id="mutation" value="p.M1M">
                    <div class="invalid-feedback">Mutation name not recognised.</div>
                    <div class="valid-feedback">Mutation name accepted.</div>
        </div>
            </div>
            ### analyse button
            <div class="col-6 col-lg-3">
                <div class="btn-group" role="group" aria-label="analyse">
                    <button type="button" class="btn btn-outline-success" id="analyse">Analyse</button>
                    <button type="button" class="btn btn-outline-danger" id="reset">Reset</button>
                    <button type="button" class="btn btn-outline-info" id="demo">Demo</button>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="card mt-5 shadow-sm" id="retrieval_card">
    <h3 class="card-header">Retrieve previous</h3>
    <div class="card-body">
        <p>This would be Session specific. Authentication? Alchemy SQLite DB included, but no models made.</p>
    </div>
</div>

<div class="card mt-5" id="result_card" style="display: None;">
    <h3 class="card-header">Results</h3>
    <div class="card-body">
    </div>
</div>

############ code
<%block name="script">
    <%include file="default.mako.js"/>
</%block>
