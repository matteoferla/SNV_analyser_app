__description___ ="""
The input page checks clientside whether the inputs exist or are valid.

Then an ajax request (gene_check) is triggered in which the gene is matched to an ID thanks to a database of synonyms. It is fast enough that this step could be implement on change as many pages do.
Parallelly, a bunch of tasks are kicked off to assemble the data using the method `parallel_parse_protein`.

The the mutation is checked &mdash;TBImpl.

Then every second, the status_check ajax request asks what is not done. Unfortunately, session cannot store objects so the thread names are stored.
Whereas it is true that Thread names can be assigned, the importance is their uniqueness. So a rather complex scheme is in place:
    
    request.session['threads'] = {Unique_thread_name: thread_description_that_makes_sense, ...}


"""

from pyramid.view import view_config
from Tracker_analyser import Variant
Variant.from_pickle = False

from mako.template import Template
from mako.lookup import TemplateLookup

import json, threading, time, os

namedex = json.load(open('data/human_prot_namedex.json','r'))
seqdex = json.load(open('data/human_prot_seqdex.json','r'))
genedex = json.load(open('data/human_prot_genedex.json','r'))

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
        request.session['gene_name']=gene_name
        ### if there is already a pickle file...
        if os.path.isfile(os.path.join('data', 'pickle', uniprot + '.p')):
            ### if there is already a pickle file...
            request.session['threads'] =dict() ## this is an odd case.
        else:
            (variant, threads) = parallel_parse_protein(uniprot=uniprot, gene_name=gene_name, return_complete=False)
            request.session['threads']={fn.name: tn for tn, fn in threads.items()}
            saver = threading.Thread(target=save_factory(variant, threads, request))
            saver.start()
        request.session['uniprot'] = uniprot
        #request.session['data'] = {} ### does not work!!!
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
        variant=Variant()
        seq = seqdex[request.session['uniprot']]
        variant.parse_mutation(request.POST['mutation'])
        if variant._check_sequence(seq):
            return {'valid': 1}
        else:
            return {'error': variant.msg_error_sequence(seq)}
    except Exception as err:
        return {'error': str(err)}


@view_config(route_name='task_check', renderer="json")
def status_check_view(request):
    if 'threads' in request.session:
        unfinished=[t.name for t in threading.enumerate() if t.name in request.session['threads'].keys()]
        status = [tdescr for tname, tdescr in request.session['threads'].items() if tname in unfinished]
        return {'status': status, 'unfinished': len(status)}

    else:
        return {'error': 'No job found'}

@view_config(route_name='get_results', renderer="../templates/results.mako") # default mako renderer giving me problems.
def get_results_view(request):
    variant = Variant.load('data/pickle/'+request.session['uniprot']+'.p')
    variant.parse_mutation(request.POST['mutation']) ## added here like this to avoid it getting saved.
    variant.predict_effect()
    return {'variant': variant}

#### move out once complte.
def parallel_parse_protein(uniprot, gene_name, return_complete=True):
    """
    A parallel version of the protein fetcher.
    It deals with the non-mutation parts of the Variant.
    :param uniprot:
    :param gene_name:
    :param return_complete: a boolean flag that either returns the threads if False, or waits for the threads to complete if true.
    :return:
    """
    self = Variant()
    self.verbose = True  # for now.
    self.from_pickle = False
    self.uniprot = uniprot
    self.gene = gene_name  # gene_name
    tasks={'Uniprot':           self.parse_uniprot,
           'PFam':              self.parse_pfam,
           'ELM':               self.query_ELM,
           'pLI':               self.get_pLI,
           'ExAC':              self.get_ExAC,
           'manual':            self.add_manual_data,
           'GO terms':          self.fetch_go,
           'Binding partners':  self.fetch_binders}
    threads={}
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
        variant.resi=1
        variant.to_resn='M'
        variant.from_resn = 'M'
        #request.session['data']=variant.__dict__
        variant.dump('data/pickle/'+variant.uniprot+'.p')
    return saver
