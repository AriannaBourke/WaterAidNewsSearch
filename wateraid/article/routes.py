from wateraid.account.utils import delete_article
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from wateraid.article.utils import article_query, emotions, insert_saved, results, save_article_query, set_button, button_query

article_blueprint = Blueprint('article_blueprint', __name__)


@article_blueprint.route("/article/<page_id>", methods=['GET', 'POST'])
@login_required
def article(page_id):
    page_id = page_id
    userid = current_user.email
    results_list = []
    # Query database for article with matching id
    results_found = article_query(page_id)
    # create results list and format date
    results_list, format_date = results(results_found)

    # Watson NLU to find emotions
    found_emotions = emotions(results_list)

    # saving article to db under user ID
    if request.method == "POST" and 'save_form' in request.form:
        save = request.form.get("save_form")
        results_found = save_article_query(page_id)
        insert_saved(results_found, userid)

    # deleting article in db under user ID
    if request.method == "POST" and 'unsave_form' in request.form:
        un_save = request.form.get("unsave_form")
        delete_article(page_id, userid)

    # set button status
    id = button_query(page_id)
    button = set_button(page_id, userid, id)

    return render_template('article.html', search_results=results_list[0:1],
                           title='Article Information', page_id=page_id, nlu_results=found_emotions,
                           button=button, format_date=format_date)
