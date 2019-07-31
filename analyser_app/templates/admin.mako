<%inherit file="layout_components/layout_w_card.mako"/>

<%block name="buttons">
            <%include file="layout_components/vertical_menu_buttons.mako" args='tour=False'/>
</%block>
<%block name="title">
            &mdash; Admin console
</%block>
<%block name="subtitle">
            Restricted access.
</%block>


<%block name="main">
% if user and user.role == 'admin':
    <%
        icon = {'basic': 'user', 'friend': 'user-tie', 'guest': 'user-secret', 'admin': 'user-crown', 'new': 'user-astronaut', 'hacker': 'user-ninja', 'trashcan': 'dumpster'}
        log = ''.join(reversed(open('analyser_app.log','r').readlines()[-200:])) #for some ducked up reason, templates are in root.

    %>
    <h3>Users</h3>
    <p class="card-text">There are ${len(users)} regististered users.</p>

    <ul class="fa-ul">
            %for u in users:
                <li data-user="${u.name}">
                    <a href="#mod" data-toggle="modal" data-target="#mod" data-user="${u.name}">
                    <span class="fa-li" >
                %if u.role in icon:
                    <i class="far fa-${icon[u.role]}" title="This user has the role: ${u.role}"></i>
                %else:
                    <i class="far fa-user-ninja" title="This user has a weird role: ${u.role}!?"></i>
                %endif
                </span> ${u.name} </a></li>
            %endfor
        </ul>
    <h3>Command station</h3>
        <div class="row border rounded w-100 p-2 m-2">
                <div class="col-lg-3">
                <div class="input-group">
                  <div class="input-group-prepend">
                    <span class="input-group-text" id="msg_title_label">Title</span>
                  </div>
                  <input type="text" class="form-control" placeholder="Title" aria-label="title" aria-describedby="msg_title_label" id="msg_title">
                </div>
            </div>
                <div class="col-lg-5">
                <div class="input-group">
                  <div class="input-group-prepend">
                    <span class="input-group-text" id="msg_descr_label">Msg</span>
                  </div>
                  <input type="text" class="form-control" placeholder="Title" aria-label="title" aria-describedby="msg_descr_label" id="msg_descr">
                </div>
            </div>
                <div class="col-lg-2">
                    <div class="btn-group">
                      <button type="button" class="btn  btn-outline-secondary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Add
                      </button>
                      <div class="dropdown-menu">
                      % for bg in ('danger', 'warning', 'info', 'success', 'primary', 'secondary'):
                          <a class="dropdown-item bg-${bg}" onclick="setMsg('bg-${bg}')">As ${bg}</a>
                      % endfor
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" onclick="setMsg('')">in white</a>
                      </div>

                      <button type="button" class="btn btn-outline-secondary" onclick="clearMsg()">Clear</button>
                    </div>
                </div>


        </div>
    <h3>Reversed request log</h3>
    <div style="height: 70vh; overflow: scroll;">
        <pre><code>${log}</code></pre>
    </div>


% else:
    <div class="card bg-warning my-3 w-100">
        <div class="card-header"><h5 class="card-title">Restricted</h5></div>
  <div class="card-body">
    <p class="card-text">Please log out and log in as admin. Then referesh the page. If you would like admin access, please email matteo.</p>
  </div>
</div>
% endif
</%block>



<%block name="modals">
    <div class="modal" tabindex="-1" role="dialog" id="mod">
      <div class="modal-dialog modal-lg" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">ERROR</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <p>Error ah!</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" id="mod-save">Save changes</button>
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
</%block>









<%block name="script">
    % if user and user.role == 'admin':
        <script type="text/javascript">
        <%include file="admin.js"/>
        </script>
    %endif

</%block>
