def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('analyse', '/analyse')
    config.add_route('task_check','/task_check')
    config.add_route('random', '/get_random')
    config.add_route('login', '/login')
    config.add_route('admin', '/admin')
