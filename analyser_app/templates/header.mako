<header>


    ######################### drawer
    <div class="collapse bg-oxford" id="navbarHeader">
        <div class="container-fluid">
            <div class="row">


                <div class="col-md-2 offset-md-1 py-4">
                    <h4 class="text-white">Links</h4>
                    <ul class="list-unstyled">
                        <li><a href="/" class="text-white"><i class="fas fa-home"></i> Home</a></li>
                        <li><a href="#navbarHeader" id="guide" class="text-white"><i class="far fa-compass"></i> Guided Tour</a></li>
                        <li><a href="https://github.com/matteoferla/VENUS" class="text-white"><i class="fab fa-github"></i> GitHub Repo</a></li>
                        <li><a href="mailto:matteo@well.ox.ac.uk" class="text-white"><i class="fas fa-envelope"></i> Email me</a></li>
                    </ul>
                </div>


                <div class="col-md-6 offset-md-1 py-4">
                    <h4 class="text-white">About</h4>
                    <p class="text-muted">This tool gathers information from various sources about a gene and ranks possible effect a SNV may have.
                <br/>(signal peptide loss, binding site, active site or ddG).</p>
                </div>
            </div>
        </div>
    </div>


    ########################## navbar
    <div class="navbar navbar-dark bg-oxford text-light shadow-sm mb-4">
        <div class="row w-100 text-center">
            <div class="col-2 mx-2 hidden-sm align-self-center">
                <img src="static/ox_full.svg" style="height: 3rem;" class="navbar-brand">
            </div>

            <div class="col-3 mx-2 align-self-center">
                <a href="/" class="navbar-brand">
                    ########<i class="fas fa-vial"></i>&nbsp;
                    <h1><img src="static/protein.svg" style="height: 2.5rem;"> VENUS</h1>
                </a>
            </div>
            <div class="col-4 hidden-sm align-self-center">
                <span class="text-muted text-center"
                  data-target="#navbarHeader"
                  aria-controls="navbarHeader"
                  aria-expanded="false">Assessing the effect of amino acid variants have on structure</span>
            </div>

            <div class="col-2 mx-2 align-self-center">
                ###########rhs block
                <span id="user"></span> &nbsp;
                <button class="btn btn-outline-light" type="button" id="new_analysis" style="display: none;">
                <i class="far fa-undo  fa-lg"></i></button>
                <button class="btn btn-outline-light" type="button" data-toggle="collapse" data-target="#navbarHeader"
                    aria-controls="navbarHeader" aria-expanded="false" aria-label="Toggle navigation">
                    <i class="far fa-bars fa-lg"></i>
                </button>
            </div>

        </div>
    </div>



</header>
