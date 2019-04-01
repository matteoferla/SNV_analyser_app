<%inherit file="layout.mako"/>

% if user and user.role == 'admin':
    <%
        from analyser_app.models import User
        users = self.context._data['request'].dbsession.query(User).all()
    %>
    <div class="card w-100 m-10">
        <div class="card-header">
                <h5 class="card-title">Admin console</h5>
            </div>
      <div class="card-body">
          <p class="card-text">
              There are ${len(users)} regististered users.
              <ul class="fa-ul">
                %for u in users:
                    %if u.role == 'admin':
                        <li><span class="fa-li" ><i class="far fa-user-crown"></i></span> ${u.name}</li>
                    %else:
                        <li><span class="fa-li" ><i class="far fa-user"></i></span> ${u.name} <buttom role="button" class="btn btn-outline-info btn-sm" data-toggle="user" data-target="${u.name}"><i class="far fa-crown"></i> make admin</buttom></li>
                    %endif
                %endfor
              </ul>
          </p>
      </div>
    </div>
% else:
    <div class="card bg-warning my-3 w-100">
        <div class="card-header"><h5 class="card-title">Restricted</h5></div>
  <div class="card-body">
    <p class="card-text">Please log out and log in as admin. Then referesh the page. If you would like admin access, please email matteo.</p>
  </div>
</div>
% endif

<%block name="script">
    <%include file="admin.js"/>
</%block>
