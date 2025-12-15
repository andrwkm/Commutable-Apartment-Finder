from flask import Blueprint, render_template, request

from app.craigslist_scraper import scrape_craigslist
from app.commute_calculator import add_commute_times

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
    furnished = "furnished" in request.form
    print(f"Furnished: {furnished}")
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

    results_df = scrape_craigslist(
        search_term, 
        min_price, max_price, 
        min_bedrooms, max_bedrooms,
        min_bathrooms, max_bathrooms, 
        cats_okay=cats_okay, dogs_okay=dogs_okay, furnished=furnished, no_smoking=no_smoking, wheelchair_accessible=wheelchair_accessible, 
        air_conditioning=air_conditioning, ev_charging=ev_charging, no_application_fee=no_application_fee, no_broker_fee=no_broker_fee, 
        wd_in_unit=wd_in_unit, wd_hookup=wd_hookup, laundry_in_bldg=laundry_in_bldg, laundry_on_site=laundry_on_site, no_laundry=no_laundry)
    
    office_address = request.form.get("office") or ""
    commute_mode = request.form.get("transport") or "walking"
    max_commute_time = int(request.form.get("commuteTime") or 0)
    
    edited_results = add_commute_times(results_df, destination=office_address, mode=commute_mode)

    print("Calculated Commute Times")


    if max_commute_time is not None:
        print("Filter by commute time")
        edited_results = edited_results[edited_results['Commute_Minutes'] <= max_commute_time]

    #rounding commute minutes for easier reading
    edited_results['Commute_Minutes'] = edited_results['Commute_Minutes'].round(2)

    #final results to dict
    results = edited_results.to_dict('records')
    return render_template("search_results.html", results=results)