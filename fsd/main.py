from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import connect_db, create_table  # Import database functions
from predict import predict_institutions
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"

create_table()

# Routes for rendering pages
@app.route("/bhanu")
def bhanu():
    return {"bhanu": "bhanu"}



if __name__ == '__main__':
    app.run(debug=True, port=8000)
