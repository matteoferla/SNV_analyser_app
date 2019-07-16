<!DOCTYPE html>
<html lang="{{ '${request.locale_name}' }}">
<%page args="request, bootstrap='regular', cdn='home', needs_tour=False, needs_feat=False, needs_plotly=False, needs_ngl=False, needs_clip=False"/>
## bootstrap: regular 4|materials (BDM)
## cdn: local|remote|home
<%
    needs_tour = False #Uncaught TypeError: No method named "destroy"
%>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="SNV analyser">
    <meta name="author" content="Matteo Ferla">
    <link rel="shortcut icon" href="${request.static_url('analyser_app:static/flavicon.png')}">

    <title>SNV Analyser</title>

    ######################## BOOTSTRAP
    % if bootstrap == 'materials':
        <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.6.1/css/mdb.min.css" rel="stylesheet">
        <script type="text/javascript">alert('toast will not work')</script>
    % else:
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    % endif

    ######################## FONTAWESOME
    % if cdn == 'remote':
        <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-LRlmVvLKVApDVGuspQFnRQJjkv0P7/YFrw84YYQtmYG4nK8c+M+NlmYDCv0rKWpG" crossorigin="anonymous">
    % elif cdn == 'home':
        <link rel="stylesheet" href="https://www.matteoferla.com/Font-Awesome-Pro/css/all.min.css" crossorigin="anonymous">
    % else: ## local
        <link rel="stylesheet" href="Font-Awesome-Pro/css/all.min.css">
    % endif

    ######################## BS TOUR
    % if needs_tour:
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-tour/0.11.0/css/bootstrap-tour-standalone.css">
    % endif


    ######################## FEAT
    % if needs_feat:
        <link rel="stylesheet" href="https://www.matteoferla.com//feature-viewer/css/style.css">
    % endif

    ######################## THEME.CSS
    <link href="${request.static_url('analyser_app:static/theme.css')}" rel="stylesheet">

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="//oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="//oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
</head>


################################################################################################################################################
################################################################################################################################################

<body>
<div class="position-absolute w-100 d-flex flex-column p-4" id="toaster">
</div>

<main role='main' class="container-fluid w-100 mx-0 px-0">
    <%block name="topmost">
        <%include file="header.mako"/>
    </%block>
    <div class="row mt-10">
        <div class="col-lg-8 offset-lg-2">
            ${ next.body() }
        </div>
    </div>
</main>
% if 1==0:
<br/>
<footer class="footer">
    <div class="container">
        <p>This is confidential and experimental, please do not distribute. EU copyright whatsits compliant.</p>
    </div>
</footer>
% endif


<%block name="modals"/>
<%include file="../login/user_modal.mako"/>


################################################################################################################################################
################################################################################################################################################


############ BS
<script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
% if bootstrap == 'materials':
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.6.1/js/mdb.min.js"></script>
% endif

######## optional assets
% if needs_ngl:
    % if cdn == 'remote':   ### this is not good.
        <script type="text/javascript">alert('rawgit CDN is out of date');</script>
        <script src="https://cdn.rawgit.com/arose/ngl/v0.10.4-1/dist/ngl.js" type="text/javascript"></script>
    % elif cdn == 'home':
        <script src="https://www.matteoferla.com/ngl/dist/ngl.js" type="text/javascript"></script>
    % else: ## local
        <script src="ngl/dist/ngl.js" type="text/javascript"></script>
    % endif
    <script src="${request.static_url('analyser_app:static/ngl.extended.js')}" type="text/javascript"></script>
% endif

% if needs_clip:  ## no CDN issue.
    <script src="https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.0/clipboard.min.js"></script>
% endif

% if needs_ploty:
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
% endif

% if needs_feat:
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.js"></script>
    <script src="https://www.matteoferla.com//feature-viewer/dist/feature-viewer.min.js" type="text/javascript"></script>
% endif

% if needs_tour:   ## no CDN issue.
     <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-tour/0.11.0/js/bootstrap-tour.min.js"></script>
% endif


######## script block
<script type="text/javascript">
    $( document).ready(function () {
        <%block name="script"/>
        <%include file="../login/user_modal.js"/>


        ///////// username
        window.set_username = function (name, icon, quietly) {
        icon = icon || 'user';
        if (! name) {name = '<i>Guest</i>'; icon = 'user-secret'}
        $("#user").html('<span id="user"><a href="#" class="text-light" data-toggle="modal" data-target="#login"><i class="far fa-'+icon+'"></i> '+name+'</a></span>');
        if (! quietly) {
            $("#user").animate({fontSize: '3em'}, "fast").animate({fontSize: '1em'}, "slow");}
        };

        //__init__
        %if user:
            $('#login-content').hide();
            $('#logout-content').show();
            $("#username-name").text("${user.name}");
            $("#username-rank").text("${user.role}");
            %if user.role == 'admin':
                set_username("${user.name}", 'user-crown', true);
            %else:
                set_username("${user.name}", null, true);
            %endif
        %else:
            set_username(null, null, true);
        %endif
    });
</script>

<script src="https://browser.sentry-cdn.com/5.1.1/bundle.min.js" crossorigin="anonymous"></script>
<script type="text/javascript">
    //Sentry.init({ dsn: 'https://632323cd831e4a32ab4a50d3b8fadf06@sentry.io/1446673' });
    window.onerror = Sentry.captureException;
</script>

</body>
</html>
