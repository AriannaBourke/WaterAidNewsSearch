from wateraid.main.utils import search_query, insert_results
from flask import Blueprint, render_template, request, redirect, url_for

main_blueprint = Blueprint('main_blueprint', __name__)


@main_blueprint.route("/", methods=['GET', 'POST'])
@main_blueprint.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == "POST" and "search" in request.form:
        search = request.form.get("search")
        # Perform Watson query with user input search term
        query_results = search_query(search)
        # Insert search results into database
        insert_results(query_results, search)
        return redirect(url_for('search_blueprint.search_results', search=search))
    return render_template('home.html')


@main_blueprint.route("/help", methods=['GET', 'POST'])
def help():
    return render_template('help.html')
