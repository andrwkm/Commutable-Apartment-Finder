# Commutable-Apartment-Finder
Application that finds the perfect NYC apartment listings based on user inputs and commute preferences.

While there is a deployed web service, this is best performed when cloned and run LOCALLY.
## Setup

Clone the repo to download it from Github.

Navigate to the repo using the command line.

```sh
cd ~/Documents/GitHub/Commutable-Apartment-Finder
```

Create a virtual environment and activate it.

```sh
conda create -n commutable_apartment_finder python=3.11
```

```sh
conda activate commutable_apartment_finder
```

Install package dependencies:

```sh
pip install -r requirements.txt
```

## Configuration

Requires a Google Maps API key to function properly. To obtain an API key, go to https://console.cloud.google.com/, create a project, and enable Distance Matrix API and Geocoding API for that project. Then create credentials to generate an API key. Obtain the key from "Show key" button under Credentials tab.

Create a `.env` file in the root directory of the project with the following content:

```sh
GOOGLE_MAPS_API_KEY="____KEY_HERE____"
```

## Usage

To run scraper, use the command line to navigate to the repo directory and run:
```sh
python app/craigslist_scraper.py
```

Commute calculator:
```sh
python app/commute_calculator.py
```

### Web App

Run the web app using following command then navigate to http://localhost:5000 on a browser.

```sh
# Mac OS:
FLASK_APP=web_app flask run

# Windows OS:
# ... if `export` doesn't work for you, try `set` instead
# ... or set FLASK_APP variable via ".env" file
export FLASK_APP=web_app
flask run
```

## Testing

Run tests using:

```sh
pytest
```
