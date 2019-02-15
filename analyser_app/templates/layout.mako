<!DOCTYPE html>
<html lang="{{ '${request.locale_name}' }}">
<%page args="request, bootstrap='regular', cdn='remote', needs_tour=False, needs_plotly=False, needs_ngl=False, needs_clip=False"/>
## bootstrap: regular 4|materials (BDM)
## cdn: local|remote|home

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
    % else:
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    % endif

    ######################## FONTAWESOME
    % if cdn == 'remote':
        <link rel="stylesheet" href="https://pro.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-LRlmVvLKVApDVGuspQFnRQJjkv0P7/YFrw84YYQtmYG4nK8c+M+NlmYDCv0rKWpG" crossorigin="anonymous">
    % elif cdn == 'home':
        <link rel="stylesheet" href="http://www.matteoferla.com/Font-Awesome-Pro/css/all.min.css" crossorigin="anonymous">
    % else: ## local
        <link rel="stylesheet" href="Font-Awesome-Pro/css/all.min.css">
    % endif

    ######################## BS TOUR
    % if needs_tour:
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-tour/0.11.0/css/bootstrap-tour-standalone.css">
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
<main role='main' class="container-fluid w-100 mx-0 px-0">
    <%block name="topmost"/>
    <div class="row mt-10">
        <div class="col-lg-8 offset-lg-2">
            ${ next.body() }
        </div>
    </div>
</main>

<div aria-live="polite" aria-atomic="true" class="d-flex justify-content-center align-items-end" style="min-height: 200px;" id="toaster">
</div>

<br/>
<footer class="footer">
    <div class="container">
        <p>This is confidential and experimental, please do not distribute. EU copyright whatsits compliant.</p>
    </div>
</footer>




################################################################################################################################################
################################################################################################################################################


############ BS
<script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
% if bootstrap == 'materials':
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.6.1/js/mdb.min.js"></script>
% endif

######## optional assets
% if needs_ngl:
    % if cdn == 'remote':   ### this is not good.
        <script src="https://cdn.rawgit.com/arose/ngl/v0.10.4-1/dist/ngl.js" type="text/javascript"></script>
    % elif cdn == 'home':
        <script src="http://www.matteoferla.com/ngl/dist/ngl.js" type="text/javascript"></script>
    % else: ## local
        <script src="ngl/dist/ngl.js" type="text/javascript"></script>
    % endif
% endif

% if needs_clip:  ## no CDN issue.
    <script src="https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.0/clipboard.min.js"></script>
% endif

% if needs_tour:   ## no CDN issue.
     <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-tour/0.11.0/js/bootstrap-tour.min.js"></script>
% endif

% if needs_ploty:
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
% endif

######## script block
<script type="text/javascript">
    $( document).ready(function () {
        <%block name="script"/>
    });
</script>


</body>
</html>
