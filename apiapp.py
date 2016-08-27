#!flask/bin/python3.5
from flask import Flask, jsonify

import requests
from bs4 import BeautifulSoup


import datetime

app = Flask(__name__)

url = 'https://www.kleve.de/parkleitsystem/pls.xml'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/parkleitsystem', methods=['GET'])
def get_parkleitsystem_data():
    result = requests.get(url)
    xmldoc = result.content
    soup = BeautifulSoup(xmldoc, "lxml-xml")

    timestamp = soup.Daten.Zeitstempel.string
    stand_datetime = datetime.datetime.strptime(timestamp, "%d.%m.%Y %H:%M:%S")

    parkings = soup.find_all('Parkhaus')

    list_response = []

    for parking in parkings:
        dict = {}
        dict['Parkplatz'] = parking.Name.string
        dict['Status'] = parking.Status.string
        dict['Gesamt'] = int(parking.Gesamt.string)
        dict['Frei'] = int(parking.Gesamt.string) - int(parking.Aktuell.string)
        dict['Lat'] = float(parking.LAT.string)
        dict['Lon'] = float(parking.LON.string)
        dict['Stand'] = stand_datetime
        list_response.append(dict)

    response = jsonify(list_response)
    return response


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.run(debug=True)
