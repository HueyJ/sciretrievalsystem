from flask import render_template, g, redirect, url_for, request, current_app
from webapp.forms import SearchForm
from flask_babel import _
from webapp.main import bp
from query_process import QueryProcessor
from math import ceil
from urllib.parse import unquote_plus, quote_plus
import json, _thread

per_page = 5

@bp.before_request
def before_request():
    g.search_form = SearchForm()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    if g.search_form.validate_on_submit():
        return redirect(url_for('main.query', query=g.search_form.search.data))
    return render_template('index.html', title=_('Home'), form=g.search_form)

@bp.route("/query/<search_terms>", methods=['GET', 'POST'])
@bp.route("/query/", methods=['GET', 'POST'])
def query(search_terms=None):
    if 'curr_page' not in locals():
        curr_page = 1
    if g.search_form.validate_on_submit() or search_terms is not None:
        search_terms = g.search_form.search.data or search_terms
        search_terms = unquote_plus(search_terms).replace("&#46", ".")
        query_processor = QueryProcessor()
        # if 'results' not in g:
        #     g.results = query_processor.process(search_terms)
        #     page_num = int(ceil(len(g.results) / float(per_page)))
        #     __cache_results(search_terms, g.results)
        results = query_processor.process(search_terms)
        page_num = int(ceil(len(results) / float(per_page)))
        __cache_results(search_terms, results)
        return render_template('query.html', title=search_terms,
                                form=g.search_form,
                                # results=__current_results(curr_page,
                                #                             per_page,
                                #                             search_terms),
                                page_num=page_num)

@bp.route("/aquery/<search_terms>/<curr_page>", methods=['GET'])
def aquery(search_terms=None, curr_page=None):
    return __current_results(curr_page, per_page, search_terms)

def __current_results(curr_page, per_page, search_terms):
    curr = int(curr_page) - 1
    per = per_page
    # if 'results' in g:
    #     return g.results[curr*per:curr*per+per]
    # else:
    #     results = json.loads(current_app.redis.get(search_terms))
    results = json.loads(current_app.redis.get(search_terms))
    return json.dumps(results[curr*per:curr*per+per])

def __cache_results(search_terms, results):
    current_app.redis.set(search_terms, json.dumps(results))
