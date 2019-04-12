<%page args="protein, home=''"/>

<%
    prolink = 'class="prolink" data-toggle="protein" data-target="viewport"'
%>

<div class="container-fluid" id="results">
    <div style="width:47vw; position:fixed; top:7rem; bottom: 24px; right: 24px;">
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
    <div class="row">
                <!-- Main text -->
                <div class="col-6 mb-4 pl-4">
                    <div class="card shadow-sm">
                        <div class="card-header"><h3 class="card-title">
                            ${protein.gene_name} ${mutation} <small>(${protein.recommended_name})</small>
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
                          <div class="arrow-right"></div><div class="arrow-right2">
                          </div>
                      <ul class="list-group list-group-flush">

                          ###################### simple ###################################

                        ${line_fore('Mutation')}
                            <span ${prolink|n} data-focus="residue" data-selection="${mutation.residue_index}:CURRENTCHAIN">
                                ${mutation.long_name(mutation.from_residue)} at position ${mutation.residue_index}</span> is mutated to ${mutation.long_name(mutation.to_residue)}
                      ${line_aft()}

                          ###################### apriori ###################################

                        ${line_fore('Effect independent of structure')}
                          ${mutation.apriori_effect}
                          %if mutation.to_residue == '*':
                              <span ${prolink|n} data-focus="domain" data-selection="1-${mutation.residue_index}:CURRENTCHAIN">remnant</span>
                              and <span ${prolink|n} data-focus="domain" data-selection="${mutation.residue_index}-99999:CURRENTCHAIN">lost</span>
                          %endif
                          ${line_aft()}

                          ###################### location ###################################

                          ${line_fore('Location')}
                            <p>The mutation is ${int(mutation.residue_index/len(protein)*100)}% along the protein.
                            <% feats= protein.get_features_near_position(mutation.residue_index) %>
                                %if feats:
                                    Namely, within domain:</p>
                                        <ul>
                                    %for f in feats:
                                        <li><span ${prolink|n}
                                                  %if f['type'] in ('domain','propeptide','splice variant','signal peptide','repeat','coiled-coil region','compositionally biased region','short sequence motif','topological domain','transit peptide', 'transmembrane region','intramembrane region','region of interest','peptide'):
                                                  data-focus="domain"
                                                  %else:
                                                  data-focus="residue"
                                                  %endif
                                                  data-selection="${f['x']}-${f['y']}:CURRENTCHAIN">
                                            ${f['type']} &mdash; (${f['x']}&ndash;${f['y']})</span> ${f['description']}</li>
                                    %endfor
                                        </ul>
                                %else:
                                    </p>
                                %endif
                          ${line_aft()}

                          ###################### gNOMAD ###################################
                          <%
                              neighbours = protein.get_gNOMAD_near_position(mutation)
                          %>
                          % if neighbours:
                            ${line_fore('Nearby mutations in the population')}
                                <p>The following motifs may be nearby: </p>
                                <ul class="fa-ul">
                                % for m in neighbours:
                                    <li>
                                        %if m['impact'] == 'HIGH':
                                            <span class="fa-li" data-toggle="tooltip" title="impact: high"><i class="far fa-exclamation-triangle"></i></span>
                                        %elif m['impact'] == 'MODERATE':
                                            <span class="fa-li" data-toggle="tooltip" title="impact: moderate"><i class="far fa-info-circle"></i></span>
                                        %else:
                                            <span class="fa-li" data-toggle="tooltip" title="impact: ${m['impact'].lower()}"><i class="far fa-comment"></i></span>
                                        %endif

                                        <span ${prolink|n} data-focus="residue" data-selection="${m['x']}:CURRENTCHAIN">${m['description']}</span>
                                    </li>
                                % endfor
                                </ul>
                              ${line_aft()}
                          % endif

                          ###################### motifs ###################################
                          % if mutation.elm:
                            ${line_fore('Possible motifs')}
                                <p>The following motifs may be nearby: <span data-toggle="tooltip" title="Even when the location matches and the mutation is on the surface it is still hypothetical and requires litterature checks"><i class="far fa-question"></i></span> </p>
                                <ul class="fa-ul">
                                % for m in mutation.elm:
                                    <li><span class="fa-li" >
                                    %if m['status'] == 'kept':
                                        <i class="far fa-info-circle"></i>
                                    %else:
                                        <i class="far fa-exclamation-triangle"></i>
                                    %endif
                                        </span>

                                        Possible motif ${m['status']}: <span data-toggle="tooltip" title="${m['description']} (${m['regex']}, p = ${m['probability']})" class="undelined">${m['name']}</span>
                                        <span ${prolink|n} data-selection="${m['x']}-${m['y']}:CURRENTCHAIN" data-focus="residue">(${m['x']}-${m['y']})</span>
                                    </li>
                                % endfor
                                </ul>
                              ${line_aft()}
                          % endif


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
    </div>
    <div class="row">
                <!-- Feature -->
                <div class="col-6 mb-4 pl-4">
                    <div class="card shadow-sm">
                        <div class="card-header"><h5 class="card-title">
                            <i class="far fa-dna"></i> Features
                        </h5><h6 class="card-subtitle mb-2 text-muted">
                            (Click on a feature to visualise it on the structure)
                        </h6></div>

                        ###################### arrow ###################################
                        ## todo move to stylesheet.

                      <div class="card-body">
                        <div class="arrow-right"></div><div class="arrow-right2"></div>

                          ###################### end of arrow ###################################

                        <div id="fv"></div>
                      </div>
                    </div>
                </div>
            </div>

<%include file="results.js.mako" args="protein=protein, home=''"/>
<%include file="report/create_modal.mako"/>

</div>



