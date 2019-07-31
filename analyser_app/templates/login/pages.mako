<div id="pages-content">
    %if user:
        ################ admin
        %if user.role == 'admin':
            <h6>Admin console</h6>
            <p><a href="/admin">Click here to go to admin console.</a></p>
        %endif

        <%
            owned = user.owned.select(request)
            visited = user.visited.select(request)
        %>

        ################# owned
        %if owned:
            <h6>Edited pages</h6>
            <ul>
                %for page in owned:
                    <li class="list-group-item" data-page="${page.identifier}">
                        <a href="/data/${page.identifier}">${page.title}</a>
                        <button class="btn btn-danger btn-sm float-right py-0" onclick="deletePage('${page.identifier}')"><i class="far fa-trash-alt"></i></button>
                    </li>
                %endfor
            </ul>
        %endif
        ######end of owned

        #### visited
        %if visited:
            <h6>Visited pages</h6>
            <ul>
                %for page in visited:
                    <li class="list-group-item" data-page="${page.identifier}">
                        <a href="/data/${page.identifier}">${page.title}</a>
                    </li>
                %endfor
            </ul>
        %endif
        ######end of visited

    %endif
</div>
