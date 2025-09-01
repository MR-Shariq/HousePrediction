from flask import Flask, request, jsonify, render_template
import BangalorePricePrediction as util

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict')
def predict():
    return render_template("predict.html")


@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    sqft = float(request.form['sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(location, sqft, bhk, bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/api/get_area_names')
def get_area_names():
    areas = ['Super built-up  Area', 'Built-up  Area', 'Plot  Area', 'Carpet  Area']
    response = jsonify({
        'area': areas
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/get_availability_names')
def get_availability_names():
    availability = ['Ready To Move', 'Immediate Possession', 'Under Construction', '19-Dec', '18-May', '17-Oct', '16-Jun', '15-Apr', '14-May', '13-Mar', '12-Oct', '11-May', '10-Sep', '09-May', '08-Mar', '07-Jun', '06-May', '05-Jun', '04-Aug', '03-Sep', '02-May', '01-Dec', '00-Jun', 'Ready To Move', 'Immediate Possession', 'Under Construction']
    response = jsonify({
        'availability': availability
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server for Home Price Prediction...")
    app.run(debug=True)
