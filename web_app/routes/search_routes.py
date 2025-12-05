from flask import Blueprint, render_template, request

search_routes = Blueprint("search_routes", __name__)

@search_routes.route("/search/form")
@search_routes.route("/search")
def search_form():
    print("SEARCH FORM...")
    return render_template("search_form.html")


@search_routes.route("/search/results", methods=["POST"])
def search_results():
    print("SEARCH RESULTS...")
    request_data = dict(request.form)
    print(f"Form Data Received: {request_data}")


    return render_template("search_results.html")