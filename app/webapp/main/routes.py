from flask import render_template, g, redirect, url_for
from webapp.forms import SearchForm
from flask_babel import _
from webapp.main import bp
from query_process import QueryProcessor

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        search_terms = form.search.data
        query_processor = QueryProcessor()
        results = query_processor.process(search_terms)
        print(results)
        # search_history = SearchHistory(search_terms=search_terms, user_ip=request.remote_addr)
        # db.session.add(search_history)
        # db.session.commit()
        return render_template('query.html', title=search_terms, form=form,
                                results=results)
    return render_template('index.html', title=_('Home'), form=form)


# {% if post.language and post.language != g.locale %}
# <span id="translation{{ post.id }}">
#     <a href="javascript:translate(
#                 '#post{{ post.id }}',
#                 '#translation{{ post.id }}',
#                 '{{ post.language }}',
#                 '{{ g.locale }}');">{{ _('Translate') }}</a>
# </span>
#             {% endif %}
