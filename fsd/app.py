from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import connect_db, create_table  # Import database functions
from predict import predict_institutions
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"

create_table()

# Routes for rendering pages
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session['user'] = email
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": True, "redirect": url_for("predict")})
            return redirect(url_for("predict"))
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"success": False, "error": "Invalid email or password"})
            return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return jsonify({"success": False, "error": "Email and password required"}), 400

        hashed_password = generate_password_hash(password)

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", 
                         (email, hashed_password))
            conn.commit()
            conn.close()
            return jsonify({"success": True, "message": "Registration successful!"})
        except mysql.connector.IntegrityError:
            return jsonify({"success": False, "error": "Email already registered"}), 400
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    return render_template("signup.html")

@app.route('/predict')
def predict():
    if 'user' not in session:
        print("User session not found! Redirecting to login.")  # Debugging log
        return redirect(url_for("login"))  # Redirect to login if not logged in
    
    print("User session found! Rendering predictor page.")  # Debugging log
    return render_template("predictor.html")

@app.route('/predict', methods=['POST'])
def predict_Coll():
    rank = int(request.form.get('rank'))
    category_gender = request.form.get('categoryGender')
    branch_code = request.form.get('branchCode')
    inst_Reg = request.form.get('inst_reg')
    results = predict_institutions(rank, category_gender, branch_code, inst_Reg)

    return jsonify({"data": results})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True,port=8000)
