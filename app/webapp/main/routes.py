from flask import render_template, g, redirect, url_for, request, current_app
from webapp.forms import SearchForm
from flask_babel import _
from webapp.main import bp
from query_process import QueryProcessor
from math import ceil
from urllib.parse import unquote_plus, quote_plus
import json, _thread

per_page = 10

@bp.before_request
def before_request():
    g.search_form = SearchForm()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    if g.search_form.validate_on_submit():
        return redirect(url_for('main.query',
                                    search_terms=g.search_form.search.data))
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
        results = query_processor.process(search_terms, start=curr_page)
        __cache_results(search_terms, results)
        return render_template('query.html', title=search_terms,
                                form=g.search_form
                                # results=__current_results(curr_page,
                                #                             per_page,
                                #                             search_terms),
                                # page_num=page_num
                                )

@bp.route("/aquery/<search_terms>/<curr_page>", methods=['GET'])
def aquery(search_terms=None, curr_page=None):
    return __current_results(curr_page, per_page, search_terms)

def __current_results(curr_page, per_page, search_terms):
    curr = int(curr_page) - 1
    per = per_page
    results = json.loads(__get_results(search_terms))
    facet = json.dumps(__facet(results))
    page_num = int(ceil(len(results) / float(per_page)))
    results = json.dumps(results[curr*per:curr*per+per])
    return json.dumps({"results":results,"pageNum":page_num, "facet":facet})

def __facet(results):
    facet = {
        "Openaccess": {},
        "Article Type": {},
        "Subject": {},
        "Year": {},
    };
    for result in results:
        result = result["_source"]

        if "aggregationType" in result:
            article_type = result["aggregationType"]
            if article_type not in facet["Article Type"]:
                facet["Article Type"][article_type] = 1
            else:
                facet["Article Type"][article_type] += 1

        if "subject" in result:
            subjects = result["subject"][:-1].split(",")
            for subject in subjects:
                subject = subject.strip()
                if subject not in facet["Subject"]:
                    facet["Subject"][subject] = 1
                    facet["Subject"][subject] += 1

        if "coverDate" in result:
            year = result["coverDate"].split("-")[0]
            if year not in facet["Year"]:
                facet["Year"][year] = 1
            else:
                facet["Year"][year] += 1

        if "openaccess" in result:
            openaccess = result["openaccess"].split("-")[0]
            if openaccess not in facet["Openaccess"]:
                facet["Openaccess"][openaccess] = 1
            else:
                facet["Openaccess"][openaccess] += 1

    # facet["Year"].sort(reverse=True)
    # print(facet)
    return facet

def __get_results(search_terms):
    return current_app.redis.get(search_terms)


def __cache_results(search_terms, results):
    current_app.redis.set(search_terms, json.dumps(results))
