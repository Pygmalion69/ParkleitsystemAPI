#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
import urllib.request
from html_table_parser import HTMLTableParser
from html_table_parser import HTMLParagraphParser

app = Flask(__name__)

url = 'https://www.kleve.de/de/inhalt/parken/'

table_parser = HTMLTableParser()
paragraph_parser = HTMLParagraphParser();


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/parkleitsystem', methods=['GET'])
def get_parkleitsystem_data():
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    xhtml = f.read().decode(f.headers.get_content_charset(), 'ignore')
    table_parser.feed(xhtml)
    table = table_parser.tables[0]
    print(table)
    list_response = []
    for row in table:
        dict = {}
        dict['Parkplatz'] = row[0]
        dict['Status'] = row[1]
        dict['Gesamt'] = int(row[2])
        dict['Frei'] = int(row[3])
        latlon = row[4].split(',')
        dict['Lat'] = float(latlon[0])
        dict['Lon'] = float(latlon[1])
        list_response.append(dict)
    return jsonify(list_response)


@app.route('/api/stand', methods=['GET'])
def get_stand():
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    xhtml = f.read().decode('utf-8')
    paragraph_parser.feed(xhtml)
    return jsonify(paragraph_parser.stand)


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.run(debug=True)
