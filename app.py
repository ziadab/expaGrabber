# javascript:prompt("Access Token",/access_token(?:%[A-F0-9]{2}){3}(.{64})/.exec(document.cookie)[1]);void(0);

from flask import Flask, jsonify, request
import requests
import pprint

app = Flask(__name__)


def findNumber(country_code, number):
    if country_code != None and number != None:
        if len(number) == 10 and country_code == "+212":
            return country_code + number[1:]
        elif len(number) == 13 and number.startswith("+212"):
            return number
        else:
            return country_code + number
    else:
        return "No Number :'("
    


@app.route("/")
def index():
    access_token = request.args.get('access_token', type = str)
    #print(access_token)
    if access_token == None: 
        return jsonify({"error": "No access token"}), 400
    else:
        data = requests.get("https://gis-api.aiesec.org/v2/people?access_token={}".format(access_token))

        if data.status_code == 401: 
            return jsonify({"error": "invalid access token"}), 401
        else:
            data = data.json()["data"]
            modifiedArray = []
            for neeko in data:
                katarina = {}
                katarina["Name"] = neeko["full_name"]
                katarina["Email"] = neeko["email"]
                # print(neeko["country_code"], neeko["phone"])
                # pprint.pprint(neeko)
                katarina["Phone"] = findNumber(neeko["country_code"], neeko["phone"]) 
                modifiedArray.append(katarina)

            return jsonify(modifiedArray), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
