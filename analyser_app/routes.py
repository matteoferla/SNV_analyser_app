def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('gene_check', '/gene_check')
    config.add_route('mut_check', '/mut_check')
    config.add_route('task_check','/task_check')
    config.add_route('get_results', '/get_results')
