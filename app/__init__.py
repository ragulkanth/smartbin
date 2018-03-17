from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_ip):
    app = FlaskAPI(__ip__, instance_relative_config=True)
    app.config.from_object(app_config[config_ip])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    from api.models import BinStatus

    @app.route('/binstatus/', methods=['POST', 'GET'])
    def binstatus():
        if request.method == "POST":
            ip = str(request.data.get('ip', ''))
            level = int(request.data.get('level', ''))
            if ip and level >=0:
                binstatus = BinStatus(ip = ip, level = level)
                binstatus.save()
                response = jsonify({
                    'id': binstatus.id,
                    'ip': binstatus.ip,
                    'timestamp': binstatus.timestamp,
                    'level': binstatus.level
                })
                response.status_code = 201
                return response
        else:
            # GET
            binstats = BinStatus.get_all()
            results = []

            for binstatus in binstats:
                obj = {
                    'id': binstatus.id,
                    'ip': binstatus.ip,
                    'timestamp': binstatus.timestamp,
                    'level': binstatus.level
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
    
    @app.route('/getbinstat/', methods=['POST'])
    def getbinstat():
        ip = str(request.data.get('ip', ''))
        if ip:
            binstats = BinStatus.query.filter_by(ip = ip).all()
            results = []
            for binstatus in binstats:
                obj = {
                    'id': binstatus.id,
                    'ip': binstatus.ip,
                    'timestamp': binstatus.timestamp,
                    'level': binstatus.level
                }
                results.append(obj)
            response = jsonify(results)
            response.satus_code = 200
            return resoponse
    return app
