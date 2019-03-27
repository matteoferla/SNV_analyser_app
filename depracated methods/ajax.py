


@view_config(route_name='gene_check', renderer="json")
def gene_check_view(request):
    """
    This is the first one that gets called. It starts a series of parallel jobs, whose IDs are stored in request.session['threads'].
    :param request:
    :return:
    """
    print(request.POST)
    if request.POST['gene'] in namedex:
        uniprot = namedex[request.POST['gene']]
        gene_name = genedex[uniprot]
        request.session['gene_name'] = gene_name
        ### if there is already a pickle file...
        if os.path.isfile(os.path.join('data', 'pickle', uniprot + '.p')):
            ### if there is already a pickle file...
            request.session['threads'] = dict()  ## this is an odd case.
        else:
            (variant, threads) = parallel_parse_protein(uniprot=uniprot, gene_name=gene_name, return_complete=False)
            request.session['threads'] = {fn.name: tn for tn, fn in threads.items()}
            saver = threading.Thread(target=save_factory(variant, threads, request))
            saver.start()
        request.session['uniprot'] = uniprot
        # request.session['data'] = {} ### does not work!!!
        return {'uniprot_name': uniprot}
    else:
        return {'error': 'Not found'}





@view_config(route_name='mut_check', renderer="json")
def mut_check_view(request):
    """
    Absolutely no storing of the mutation data or else it might get pickled.
    :param request:
    :return:
    """
    try:
        variant = Protein()
        variant.sequence = seqdex[request.session['uniprot']]
        mutation = Mutation(request.POST['mutation'])
        if variant.check_mutation(mutation):
            return {'valid': 1}
        else:
            return {'error': variant.msg_error_sequence(variant.sequence)}
    except Exception as err:
        print(err)
        return {'error': str(err)}

        if os.path.isfile(os.path.join('data', 'pickle', uniprot + '.p')) and 1==0: ### if there is already a pickle file, which theere should be eventually.
            request.session['threads'] = dict()  ## this is an odd case.
        else:
            protein.parse_all(mode='background')



@view_config(route_name='task_check', renderer="json")
def status_check_view(request):
    if 'threads' in request.session:
        unfinished = [t.name for t in threading.enumerate() if t.name in request.session['threads'].keys()]
        status = [tdescr for tname, tdescr in request.session['threads'].items() if tname in unfinished]
        return {'status': status, 'unfinished': len(status)}

    else:
        return {'error': 'No job found'}


@view_config(route_name='get_results', renderer="../templates/results.mako")  # default mako renderer giving me problems.
def get_results_view(request):
    variant = Protein.load('data/pickle/' + request.session['uniprot'] + '.p')
    variant.parse_mutation(request.POST['mutation'])  ## added here like this to avoid it getting saved.
    variant.predict_effect()
    return {'variant': variant}


############################ DEPRACATION IN PROGTRSS
# @view_config(route_name='get_results', renderer="../templates/results.mako") # default mako renderer giving me problems.
def old_get_results_view(request):
    variant = Variant.load('data/pickle/' + request.session['uniprot'] + '.p')
    variant.parse_mutation(request.POST['mutation'])  ## added here like this to avoid it getting saved.
    variant.predict_effect()
    return {'variant': variant}


#### TODO move out once complte.
def parallel_parse_protein(uniprot, gene_name, return_complete=True):
    """
    A parallel version of the protein fetcher.
    It deals with the non-mutation parts of the Variant.
    :param uniprot:
    :param gene_name:
    :param return_complete: a boolean flag that either returns the threads if False, or waits for the threads to complete if true.
    :return:
    """
    self = Protein()
    self.verbose = True  # for now.
    self.from_pickle = False
    self.uniprot = uniprot
    self.gene = gene_name  # gene_name
    tasks = {'Uniprot': self.parse_uniprot}
    threads = {}
    for k, fn in tasks.items():
        t = threading.Thread(target=fn)
        t.start()
        threads[k] = t
    if return_complete:
        for tn, t in threads.items():
            t.join()
        return self
    else:
        return (self, threads)


def save_factory(variant, threads, request):
    def saver():
        for tn, t in threads.items():
            t.join()
        variant.resi = 1
        variant.to_resn = 'M'
        variant.from_resn = 'M'
        # request.session['data']=variant.__dict__
        variant.dump('data/pickle/' + variant.uniprot + '.p')

    return saver

