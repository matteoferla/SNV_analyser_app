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
                            ${protein.gene_name} ${mutation}
                        </h3><h6 class="card-subtitle mb-2 text-muted">
                            Predicted effects
                        </h6></div>

                        ###################### standard line ###################################

                        <%def name="line_fore(text)">
                            <li class="list-group-item">
                                <div class="row">
                                    <div class="col-12 col-md-3"><span class="font-weight-bold text-right align-middle">${text}</span></div>
                                    <div class="col-12 col-md-9 text-left border-left">
                        </%def>

                        <%def name="line_aft()">
                                    </div></div> </li>
                        </%def>

                        ###################### lines ###################################

                      <div class="card-body">
                      <ul class="list-group list-group-flush">

                          ###################### simple ###################################

                        ${line_fore('Mutation')}
                            <span class="prolink" data-toggle="protein" data-target="viewport" data-focus="residue" data-selection="${mutation.residue_index}">
                                ${mutation.long_name(mutation.from_residue)} at position ${mutation.residue_index}</span> is mutated to ${mutation.long_name(mutation.to_residue)}
                      ${line_aft()}

                          ###################### apriori ###################################

                        ${line_fore('Effect independent of structure')}
                            ${mutation.apriori_effect}
                          ${line_aft()}

                          ###################### location ###################################

                          ${line_fore('Location')}
                            <p>The mutation is ${int(mutation.residue_index/len(protein)*100)}% along the protein.
                            <% feats= protein.get_features_near_position(mutation.residue_index) %>
                                %if feats:
                                    Namely, within domain:</p>
                                        <ul>
                                    %for f in feats:
                                        <li><span class="prolink" data-toggle="protein" data-target="viewport"
                                                  %if f['type'] in ('domain','propeptide','splice variant','signal peptide','repeat','coiled-coil region','compositionally biased region','short sequence motif','topological domain','transit peptide', 'transmembrane region','intramembrane region','region of interest','peptide'):
                                                  data-focus="domain"
                                                  %else:
                                                  data-focus="residue"
                                                  %endif
                                                  data-selection="${f['x']}-${f['y']}">
                                            ${f['type']} &mdash; (${f['x']}&ndash;${f['y']})</span> ${f['description']}</li>
                                    %endfor
                                        </ul>
                                %else:
                                    </p>
                                %endif
                          ${line_aft()}

                          ###################### external ###################################

                        ${line_fore('External links')}
                            <a href="https://www.uniprot.org/uniprot/${protein.uniprot}" target="_blank">Uniprot:${protein.uniprot} <i class="far fa-external-link-square"></i></a> &mdash;
                            <a href="https://www.rcsb.org/pdb/protein/${protein.uniprot}" target="_blank">PDB:${protein.uniprot} <i class="far fa-external-link-square"></i></a> &mdash;
                            <a href="https://gnomad.broadinstitute.org/gene/${protein.gene_name}" target="_blank">gNOMAD:${protein.gene_name} <i class="far fa-external-link-square"></i></a>
                        ${line_aft()}

                            ###################### end ###################################

                      </ul>
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

                        ###################### arrow ###################################
                        ## todo move to stylesheet.

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

                          ###################### end of arrow ###################################

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
                        <div id="viewport" style="width:100%; height: 0; padding-bottom: 100%;">
                            <button type="button"
                                    class="btn btn-outline-secondary rounded-circle bg-white"
                                    style="position:absolute; top:4.5rem; right:10px; z-index:1001"
                                    id="viewport_menu_popover"
                                    data-toggle="popover"
                                            data-html="true"
                                            data-trigger="manual"
                                            data-title="Options"
                                            data-content='To do. Plug me in with stuff stolen from Cosmic3D'>
                                <b>&nbsp;<i class="far fa-ellipsis-v"></i>&nbsp;</b>
                            </button>
                        </div>
                      </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>


##<%include file="results.tour.js.mako" args="protein=protein, home=''"></%include>
<%include file="results.js.mako" args="protein=protein, home=''"></%include>
