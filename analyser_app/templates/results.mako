<%page args="variant, home=''"/>
## variant is a dictionary here!!

<div class="container-fluid ">
    <div class="row">
        <!-- sidebar -->
        <div class="col-md-2 d-flex flex-column">
            <a class="btn btn-info" id="guide"><i class="far fa-compass"></i> Guided Tour</a>
            <a class="btn btn-dark text-muted"><i class="far fa-dumpster-fire"></i> etc</a>
            <a class="btn btn-dark text-muted"><i class="far fa-dumpster-fire"></i> etc</a>
        </div>
        <div class="col-md-10">
            <div class="row">
                <!-- Main text -->
                <div class="col-md-12" id="user_text">${variant.user_text}</div>
                <!-- Feature -->
                <div class="col-md-7">
                    <div class="card">
                        <div class="card-header"><h5 class="card-title">
                            <i class="far fa-dna"></i> Features
                        </h5><h6 class="card-subtitle mb-2 text-muted">
                            (Click on a feature to visualise it on the structure)
                        </h6></div>

                      <div class="card-body">
                        <div id="fv"></div>
                      </div>
                    </div>
                </div>
                <!-- strucutre -->
                <div class="col-md-5">
                    <div class="card">
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


<%include file="results.tour.js.mako" args="variant=variant, home=''"></%include>
<%include file="results.js.mako"      args="variant=variant, home=''"></%include>
