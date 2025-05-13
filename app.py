#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import json

from flask import Flask, request, jsonify
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials, firestore

import os
from dotenv import load_dotenv



app = Flask(__name__)
CORS(app)

load_dotenv()  # Load variables from .env

SECRET_KEY = os.getenv("SECRET_KEY")
FIREBASE_CREDENTIAL = os.getenv("FIREBASE_CREDENTIAL")



# Firebase Initialization
cred = credentials.Certificate(FIREBASE_CREDENTIAL)
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/api/health', methods=['POST'])
def receive_health_data():
    data = request.json
    try:
        user_id = data['user_id']
        health_data = {
            'heartbeat': data.get('heartbeat', 0),
            'temperature': data.get('temperature', 0.0),
            'blood_pressure': data.get('blood_pressure', '0/0'),
            'oxygen_level': data.get('oxygen_level', 0.0),
            'last_updated': data.get('last_updated', '')
        }
        # Save to Firestore
        db.collection('health_data').document(user_id).set(health_data)
        return jsonify({'status': 'success', 'message': 'Data stored successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

@app.route('/api/health/<user_id>', methods=['GET'])
def get_health_data(user_id):
    try:
        # Retrieve health data from Firestore
        doc_ref = db.collection('health_data').document(user_id)
        doc = doc_ref.get()

        if doc.exists:
            return jsonify({'status': 'success', 'data': doc.to_dict()}), 200
        else:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)