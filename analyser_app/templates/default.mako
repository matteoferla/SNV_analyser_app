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


<div class="card">
    <h3 class="card-header">Input new</h3>
    <div class="card-body">
        <div class="row">
            ### gene
            <div class="col-12 col-lg-6">
                <div class="input-group mb-3">
        <div class="input-group-prepend">
            <label class="input-group-text" id="gene_label">Gene name </label>
        </div>
        <input type="text" class="form-control" placeholder="gene name" aria-label="gene name" aria-describedby="gene_label" id="gene">
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
        <input type="text" class="form-control" placeholder="p.M1M" aria-label="mutation" aria-describedby="mutation_label" id="mutation">
                    <div class="invalid-feedback">Mutation name not recognised.</div>
                    <div class="valid-feedback">Mutation name accepted.</div>
        </div>
            </div>
            ### analyse button
            <div class="col-6 col-lg-1">
                <div class="btn-group" role="group" aria-label="analyse">
                    <button type="button" class="btn btn-primary" id="analyse">Analyse</button>
                </div>
            </div>
        </div>


        <hr>
        <h3>Retrieve previous</h3>
        <p>This would be Session specific. Authentication?</p>
    </div>
</div>

############ code
<%block name="script">
    <%include file="default.mako.js"/>
</%block>
