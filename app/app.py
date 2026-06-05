from flask import Flask,request
from flask import jsonify
from database import *
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask('twinkle-backend-service')

def logger_init():
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    log_handler = RotatingFileHandler(
        os.path.join(log_dir,'app.log'),
        backupCount=5,
        maxBytes=10485760,
    )

    log_handler.setLevel(logging.INFO)
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(log_formatter)
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_formatter)

logger_init()

@app.route('/api/v1/health', methods=['GET'])
def get_health():
    status = {'status': 'ok'}
    app.logger.info(status)
    return jsonify(status)

@app.route('/api/v1/get/user/<user_id>',methods=['GET'])
def get_users_by_id(user_id):
    users = db_get_users(app,user_id)
    return jsonify({'users': users})

@app.route('/api/v1/get/users',methods=['GET'])
def get_all_users():
    users = db_get_all_users(app)
    app.logger.info(f"Fetched users: {users}")
    return jsonify({'users': users})

@app.route('/api/v1/create/user',methods=['POST'])
def create_user():
    user_details = request.get_json(force=True)
    username = user_details.get('username')
    email = user_details.get('email')
    try:
        user = db_create_user(app,username,email)
        return jsonify(user.data), 201
    except Exception as e:
        app.logger.error(f"Error connecting to database: {e}")
        return "Try again later", 500



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)