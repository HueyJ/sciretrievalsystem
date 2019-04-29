from flask import render_template, g, redirect, url_for
from webapp.forms import SearchForm
from flask_babel import _
from webapp.main import bp
from query_process import QueryProcessor
from math import ceil

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search_terms = form.search.data
        query_processor = QueryProcessor()
        results = query_processor.process(search_terms)
        total_num = len(results)
        per_page = 2
        curr_page = 0
        pagination = Pagination(total_num, per_page, curr_page)
        return render_template('query.html', title=search_terms, form=form,
                                results=pagination.get_curr_results(results),
                                pagination=pagination)
    return render_template('index.html', title=_('Home'), form=form)

class Pagination(object):

    def __init__(self, total_num, per_page, curr_page):
        self.total_num = total_num
        self.per_page = per_page
        self.curr_page = curr_page

    def get_curr_results(self, results):
        curr_results = results
        if not self.has_prev:
            curr_results = curr_results[:self.per_page]
        elif not self.has_next:
            curr_results = curr_results[(self.per_page * self.curr_page):]
        else:
            curr_results = curr_results[(self.per_page * self.curr_page)\
            :(self.per_page * self.curr_page) + self.per_page]
        return curr_results

    @property
    def page_num(self):
        return int(ceil(self.total_num / float(self.per_page)))

    @property
    def next_page(self):
        if self.has_next:
            self.curr_page += 1
        return self.curr_page

    @property
    def prev_page(self):
        if self.has_prev:
            self.curr_page -= 1
        return self.curr_page

    @property
    def has_prev(self):
        return self.curr_page > 0

    @property
    def has_next(self):
        return self.page_num > self.curr_page
