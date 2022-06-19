from flask import Flask, render_template, request, jsonify
import os
import yaml
import joblib
import numpy as np
import json
import logging



params_path = "params.yaml"
webapp_root = "webapp"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder = static_dir, template_folder = template_dir)

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def predict(data):
    logger = logging.getLogger("predict")
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict(data)
    logger.info('> %f' % prediction)
    return prediction 

def api_response(request):
    logger = logging.getLogger("predict")
    try:
        data = np.array([list(request.json.values())])
        response = predict(data)
        response = {"response":response}
        return response
    except Exception as e:
        logger.info('> %s' % e)
        error = {"error":"Something went wrong!! Try again"}
        return error


@app.route("/", methods=["GET", "POST"])
def index():
    logger = logging.getLogger("predict")
    if request.method == "POST":
        try:
        
            if request.form:
                Item_Identifier = request.form['Item_Identifier']
                Item_Visibility = float(request.form['Item_Visibility'])
                Item_MRP = float(request.form['Item_MRP'])
                Outlet_Establishment_Year = request.form['Outlet_Establishment_Year']
                Outlet_Identifier = request.form['Outlet_Identifier']
                Outlet_Type = request.form['Outlet_Type']

                d2 = json.load(open("data/dictd.txt"))
                Item_Identifier = d2[Item_Identifier]


                if Outlet_Identifier == 'OUT018':
                    Outlet_Identifier_OUT018 = 1
                    Outlet_Identifier_OUT027 = 0	
                    Outlet_Identifier_OUT045 = 0
                elif Outlet_Identifier == 'OUT027':
                    Outlet_Identifier_OUT018 = 0
                    Outlet_Identifier_OUT027 = 1	
                    Outlet_Identifier_OUT045 = 0
                elif Outlet_Identifier == 'OUT045':
                    Outlet_Identifier_OUT018 = 0
                    Outlet_Identifier_OUT027 = 0	
                    Outlet_Identifier_OUT045 = 1
                else:
                    Outlet_Identifier_OUT018 = 0
                    Outlet_Identifier_OUT027 = 0	
                    Outlet_Identifier_OUT045 = 0
                

                if Outlet_Type == 'Supermarket Type1':
                    Outlet_Type_Supermarket_Type1 = 1
                    Outlet_Type_Supermarket_Type2 = 0
                    Outlet_Type_Supermarket_Type3 = 0
                elif Outlet_Type == 'Supermarket Type2':
                    Outlet_Type_Supermarket_Type1 = 0
                    Outlet_Type_Supermarket_Type2 = 1
                    Outlet_Type_Supermarket_Type3 = 0
                elif Outlet_Type == 'Supermarket Type3':
                    Outlet_Type_Supermarket_Type1 = 0
                    Outlet_Type_Supermarket_Type2 = 0
                    Outlet_Type_Supermarket_Type3 = 1
                else:
                    Outlet_Type_Supermarket_Type1 = 0
                    Outlet_Type_Supermarket_Type2 = 0
                    Outlet_Type_Supermarket_Type3 = 0

                # data = dict(request.form).values()
                data = [[Item_Identifier, Item_Visibility, Item_MRP, Outlet_Establishment_Year, Outlet_Identifier_OUT018, Outlet_Identifier_OUT027,
                         Outlet_Identifier_OUT045, Outlet_Type_Supermarket_Type1, Outlet_Type_Supermarket_Type2, Outlet_Type_Supermarket_Type3]]
                response = predict(data)
                return render_template("index.html", response=response)
            
            elif request.json:
                response = api_response(request)
                return jsonify(response)

        except Exception as e:
            logger.error(e)
            error = {"error": "Something went wrong!! Try again later!"}
            error = {"error": e}

            return render_template("404.html", error=error)
        else:
                logger.info('> Invalid data')

        
    else:
        return render_template("index.html")

logger = logging.getLogger("predict")
handler  = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s|%(levelname)s|%(name)s|%(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080)