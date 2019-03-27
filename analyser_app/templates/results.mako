<%page args="protein, home=''"/>

<div class="container-fluid" id="results">
    <div class="row">
        <!-- sidebar -->
        <div class="col-md-2 d-flex flex-column">
            <a class="btn btn-success" id="new_analysis"><i class="far fa-search"></i> New query</a>
            <a class="btn btn-info" id="guide"><i class="far fa-compass"></i> Guided Tour</a>
            <a class="btn btn-dark text-muted"><i class="far fa-dumpster-fire"></i> etc</a>
        </div>
        <div class="col-md-10">
            <div class="row">
                <!-- Main text -->
                <div class="col-md-12 mb-4">
                    <div class="card shadow-sm">
                        <div class="card-header"><h3 class="card-title">
                            ${protein.gene_name}
                        </h3><h6 class="card-subtitle mb-2 text-muted">
                            Something.
                        </h6></div>

                      <div class="card-body">
                      Data.
                      </div>
                      </div>
                    </div>
                <!-- Feature -->
                <div class="col-md-7">
                    <div class="card shadow-sm">
                        <div class="card-header"><h5 class="card-title">
                            <i class="far fa-dna"></i> Features
                        </h5><h6 class="card-subtitle mb-2 text-muted">
                            (Click on a feature to visualise it on the structure)
                        </h6></div>

                      <div class="card-body">
                        <div style="
                            right:-30px;
                            top: 140px;
                            position: absolute;
                            width: 0;
                            z-index:1000;
                            height: 0;
                            border-top: 30px solid transparent;
                            border-bottom: 30px solid transparent;
                            border-left: 30px solid rgba(0, 0, 0, 0.125);">
                        </div>
                          <div style="
                            right:-29px;
                            top: 140px;
                            position: absolute;
                            width: 0;
                            z-index:1000;
                            height: 0;
                            border-top: 30px solid transparent;
                            border-bottom: 30px solid transparent;
                            border-left: 30px solid white;">
                        </div>
                        <div id="fv"></div>
                      </div>
                    </div>
                </div>
                <!-- strucutre -->
                <div class="col-md-5">
                    <div class="card shadow-sm">
                        <div class="card-header"><h5 class="card-title">
                            <i class="far fa-cubes"></i> Structure
                        </h5></div>
                      <div class="card-body">
                        <div id="viewport" style="width:100%; height: 0; padding-bottom: 100%;"></div>
                      </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>


##<%include file="results.tour.js.mako" args="protein=protein, home=''"></%include>
<%include file="results.js.mako" args="protein=protein, home=''"></%include>
