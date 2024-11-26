from flask import Flask, render_template, url_for, request, redirect, flash, session
import sqlite3
from db import create_database, add_user, verify_login, update_session, get_user_by_email, update_user_info
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from flask import Flask, render_template, jsonify
import os

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    
app = Flask(__name__)
app.secret_key = '019481204712'
# Your College Scorecard API endpoint
API_URL = "https://api.data.gov/ed/collegescorecard/v1/schools"
#API_KEY = os.getenv("VL5KYWbqcDjaoTi3r71Nqpth9mV5bGYgbOlzC88y")



# Create database on startup
create_database()

@app.route("/")
def home():
    return render_template('homepage.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/get_colleges", methods=["GET"])
def get_colleges():
    params = {
        'api_key': API_KEY,
        'fields': 'school.name',  # You can adjust the fields if you need more data
        'per_page': 100  # Adjust the number of colleges fetched if necessary
    }
    
    # Call the College Scorecard API
    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        colleges = [school['school']['name'] for school in data.get('results', [])]
        return jsonify({'colleges': colleges})
    else:
        return jsonify({'colleges': []}), 500

# Signup route (when the user signs up)
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'logged_in' in session and session['logged_in']:
        flash("You are already logged in. Redirecting to your account.", "info")
        return redirect(url_for('account'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        college = request.form['college']
        major = request.form['major']
        classes = request.form['classes']
        hobbies = request.form['hobbies']

        # Check if the email already exists in the SQLite database
        if get_user_by_email(email):
            flash("Email already exists. Please log in.", "error")
            return redirect(url_for('login'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Add the new user to the SQLite database
        add_user(name, email, hashed_password, age, college, major, classes, hobbies)
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login route (when the user logs in)
@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'logged_in' in session and session['logged_in']:
        flash("You are already logged in. Redirecting to your account.", "info")
        return redirect(url_for('account'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Retrieve the user from the database
        user_data = get_user_by_email(email)

        if user_data:
            # Check if the password matches the hashed password
            if check_password_hash(user_data[3], password):  # assuming password is in index 3
                session['logged_in'] = True
                session['email'] = email

                # Update session in the database
                update_session(email)

                flash("Logged in successfully!", "success")
                return redirect(url_for('account'))
            else:
                flash("Invalid email or password.", "error")
                return redirect(url_for('login'))
        else:
            flash("User not found.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route("/account", methods=['GET', 'POST'])
def account():
    if 'logged_in' not in session or not session['logged_in']:
        flash("You must be logged in to access the account page.", "error")
        return redirect(url_for('login'))

    email = session['email']
    user_data = get_user_by_email(email)

    if user_data:
        # If the user is found, display their profile
        user_info = {
            'name': user_data[1],
            'email': user_data[2],
            'age': user_data[4],
            'college': user_data[5],
            'major': user_data[6],
            'classes': user_data[7],
            'hobbies': user_data[8]
        }
        return render_template('account.html', user_info=user_info)

    flash("User not found.", "error")
    return redirect(url_for('login'))

@app.route("/edit_account", methods=["GET", "POST"])
def edit_account():
    if 'logged_in' not in session or not session['logged_in']:
        flash("You must be logged in to edit your account information.", "error")
        return redirect(url_for('login'))

    email = session['email']
    user_data = get_user_by_email(email)  # Retrieve the user from the database

    if request.method == 'POST':
        # Collect new form data from user
        age = request.form['age']
        college = request.form['college']
        major = request.form['major']
        classes = request.form['classes']
        hobbies = request.form['hobbies']

        # Update the user information in the database
        update_user_info(email, age, college, major, classes, hobbies)

        flash("Account information updated successfully!", "success")
        return redirect(url_for('account'))  # Redirect to account page

    # If GET request, show the form with the current values filled in
    if user_data:
        return render_template('edit_account.html', user_info=user_data)
    else:
        flash("User not found.", "error")
        return redirect(url_for('login'))
    
@app.route("/howtouse")
def howtouse():
    return render_template('howtouse.html')

@app.route("/features")
def features():
    return render_template('features.html')

@app.route("/community")
def community():
    return render_template('community.html')

@app.route("/Aboutus")
def Aboutus():
    return render_template('Aboutus.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

@app.route('/submit_form', methods=['POST'])
def submit_form():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "Studyfuze4@gmail.com"  # Enter your address
    receiver_email = "Studyfuze4@gmail.com"  # Enter receiver address
    password = "lfwe epjs zpvs mosk"  # Enter your email password

    # Retrieve data from the form
    sender = request.form['sender_email']
    subject = request.form['subject']
    message = request.form['message']

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message text
    body = f"Message from: {sender}\n\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Sent!")

        # Flash a success message and redirect back to the contact page
        flash("Thank you for your message! We will get back to you shortly.", "success")
    except Exception as e:
        print(f"Error sending email: {e}")
        flash("There was an error sending your message. Please try again later.", "error")

    return redirect(url_for('contact'))  # Assuming the contact page route is named 'contact'

def get_users(college=None, class_name=None, major=None):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # SQL query to search based on college and/or class
    query = "SELECT * FROM users WHERE 1=1"
    params = []

    if college:
        query += " AND college = ?"
        params.append(college)

    if class_name:
        query += " AND classes LIKE ?"
        params.append(f"%{class_name}%")
    
    if major:
        query += " AND major LIKE ?"
        params.append(f"%{major}%")

    cursor.execute(query, params)
    users = cursor.fetchall()

    conn.close()

    # Format users as a list of dictionaries for easier rendering in templates
    formatted_users = [
        {
            "name": user[1],  # name is at index 1
            "email": user[2],  # email is at index 2
            "age": user[4],  # age is at index 3
            "college": user[5],  # college is at index 4
            "major": user[6],  # major is at index 5
            "classes": user[7],  # classes is at index 6 (can be a comma-separated string)
            "hobbies": user[8]  # hobbies is at index 7
        }
        for user in users
    ]

    return formatted_users


@app.route('/search', methods=['GET', 'POST'])
def search():
    users = []

    if request.method == 'POST':
        college = request.form.get('college')
        class_name = request.form.get('class')
        major = request.form.get('major')

        # Call the get_users function with the form data (including major)
        users = get_users(college=college, class_name=class_name, major=major)

    return render_template('search.html', users=users)






@app.route('/user/<email>')
def user_bio(email):
    print(f"Fetching user with email: {email}")  # Debugging print

    # Proceed to get the user data
    user_data = get_user_by_email(email)
    if user_data:
        user_info = {
            'name': user_data[1],
            'email': user_data[2],
            'age': user_data[4],
            'college': user_data[5],
            'major': user_data[6],
            'classes': user_data[7],
            'hobbies': user_data[8]
        }
        return render_template('user_bio.html', user_info=user_info)
    else:
        flash("User not found.", "error")
        return redirect(url_for('search'))



