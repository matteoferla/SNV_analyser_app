<%inherit file="layout_components/layout.mako"/>




################ main
<%block name="body">
<div class="card shadow-sm" id="input_card">
    <h3 class="card-header">Input new</h3>
    <div class="card-body">
        <div class="row">
            ### gene
            <div class="col-12 col-lg-5">
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
        <p>Finish me.</p>
    </div>
</div>

<div class="card mt-5" id="result_card" style="display: None;">
    <h3 class="card-header">Results</h3>
    <div class="card-body">
    </div>
</div>
</%block>


############ modal
<%block name="modals">
</%block>


############ code
<%block name="script">
    <%include file="main.js"/>
</%block>
