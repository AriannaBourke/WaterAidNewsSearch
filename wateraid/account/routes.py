from flask import Blueprint, render_template, request, redirect, url_for
from wateraid.database import Database
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_args
import re
from wateraid.account.utils import account_pagination, delete_article, keywords_results, no_duplicates, results

account_blueprint = Blueprint('account_blueprint', __name__)


@account_blueprint.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    page, per_page, offset = get_page_args()
    userid = current_user.email
    # find all saved articles for userid
    results_found = Database.saved.find({'userid': userid}).sort('_id', -1)
    # Create pagination parameters
    pagination = account_pagination(results_found, userid)
    # create results list
    results_list = results(results_found)

    # Delete saved article
    if request.method == "POST" and "delete" in request.form:
        delete = request.form.get("delete")
        # delete article from database for userid
        delete_article(delete, userid)
        return redirect(url_for('account_blueprint.account'))

    # Search saved articles using keywords or words included in the title
    if request.method == "POST" and "search" in request.form:
        search = request.form.get("search")
        # Get saved articles included input keywords for userid
        keywords_list = keywords_results(userid, search)
        # Get saved articles including title input for userid
        results_found = Database.saved.find(
            {"userid": userid, "results.results.title":  re.compile(search, re.IGNORECASE)})
        # Create pagination parameters
        page_results = results_found.limit(per_page).skip(offset)
        # Remove duplicates and create list of saved articles
        results_list = no_duplicates(results_found, keywords_list)
        pagination = Pagination(page=page, per_page=per_page, offset=offset,
                                total=page_results.count(),
                                css_framework='bootstrap4')
        return render_template('account.html', search_results=results_list,
                               pagination=pagination)

    return render_template('account.html', search_results=results_list,
                           pagination=pagination)
