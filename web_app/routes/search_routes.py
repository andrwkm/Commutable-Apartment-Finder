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
    print(f"Form Data Received: {dict(request.form)}")  # Keep this for debugging

    search_term = request.form.get("search_query") or ""
    print(f"Search Term: {search_term}")

    min_price = request.form.get("minRent") or None
    print(f"Min Price: {min_price}")
    max_price = request.form.get("maxRent") or None
    print(f"Max Price: {max_price}")
    min_bedrooms = request.form.get("minBeds") or None
    print(f"Min Bedrooms: {min_bedrooms}")
    max_bedrooms = request.form.get("maxBeds") or None
    print(f"Max Bedrooms: {max_bedrooms}")

    min_bathrooms = request.form.get("minBaths") or None
    print(f"Min Bathrooms: {min_bathrooms}")
    max_bathrooms = request.form.get("maxBaths") or None
    print(f"Max Bathrooms: {max_bathrooms}")

    # Check if the key exists in request.form to see if it's checked
    cats_okay = "cats" in request.form
    print(f"Cats Okay: {cats_okay}")
    dogs_okay = "dogs" in request.form
    print(f"Dogs Okay: {dogs_okay}")
    no_smoking = "no_smoking" in request.form
    print(f"No Smoking: {no_smoking}")
    wheelchair_accessible = "accessible" in request.form
    print(f"Wheelchair Accessible: {wheelchair_accessible}")
    air_conditioning = "air-conditioning" in request.form
    print(f"Air Conditioning: {air_conditioning}")
    ev_charging = "EV-charging" in request.form
    print(f"EV Charging: {ev_charging}")
    no_application_fee = "no-application-fee" in request.form
    print(f"No Application Fee: {no_application_fee}")
    no_broker_fee = "no-broker-fee" in request.form
    print(f"No Broker Fee: {no_broker_fee}")

    wd_in_unit = "unit" in request.form
    print(f"W/D In Unit: {wd_in_unit}")
    wd_hookup = "hookups" in request.form
    print(f"W/D Hookup: {wd_hookup}")
    laundry_in_bldg = "building" in request.form
    print(f"Laundry In Building: {laundry_in_bldg}")
    laundry_on_site = "site" in request.form
    print(f"Laundry On Site: {laundry_on_site}")
    no_laundry = "no-laundry" in request.form
    print(f"No Laundry On Site: {no_laundry}")

    return render_template("search_results.html")