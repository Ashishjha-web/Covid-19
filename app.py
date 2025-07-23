# @Ashish Jha

from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_URL = "https://disease.sh/v3/covid-19/countries/"

# Route: Home Page (Introduction)
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

# Route: Symptoms Page
@app.route('/symptoms')
def symptoms():
    return render_template("symptoms.html")

# Route: Prevention Page
@app.route('/prevention')
def prevention():
    return render_template("prevention.html")

# Route: Covid Data Page (GET shows country list, POST shows data)
@app.route('/live-stats', methods=['GET', 'POST'])
def live_stats():
    data = {}
    error = None

    try:
        response = requests.get(API_URL)
        countries_data = response.json()
        countries = sorted([c['country'] for c in countries_data])
    except:
        countries_data = []
        countries = []
        error = "Could not fetch country list."

    if request.method == 'POST':
        selected_country = request.form.get('country')
        if selected_country:
            country_info = next((c for c in countries_data if c['country'].lower() == selected_country.lower()), None)
            if country_info:
                data = {
                    'country': country_info['country'],
                    'flag': country_info['countryInfo']['flag'],
                    'cases': country_info['cases'],
                    'deaths': country_info['deaths'],
                    'recovered': country_info['recovered'],
                    'todayCases': country_info['todayCases']
                }
            else:
                error = "Country data not found."

    return render_template("live_stats.html", countries=countries, data=data, error=error)

# Route: Contact Us Page
@app.route('/contactus')
def contactus():
    return render_template("contactus.html")

if __name__ == '__main__':
    app.run(debug=True)
