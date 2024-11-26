from flask import Flask, render_template, url_for, request, jsonify, redirect, flash
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import csv

app = Flask(__name__) #Created an instance of the Flask framework, created an app
app.secret_key = '019481204712'
print(__name__)

@app.route("/") # root directory website
def home():
    return render_template('homepage.html') #look for templates html file, and then run the given html file

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/loginpage")
def login():
    return render_template('login.html')

@app.route("/account")
def account():
    return render_template('account.html')

def update_session(email):
    rows = []
    updated = False
    with open('database.csv', mode='r') as database:
        csv_reader = csv.reader(database, delimiter=',')
        rows = list(csv_reader)  # Read all rows into a list

    # Loop through the rows to find the user and update the session
    for row in rows:
        if len(row) < 4:
            continue  # Skip rows that don't have the expected number of columns
        if row[1] == email:  # Check if the email matches
            row[3] = str(int(row[3]) + 1)  # Increment the session value by 1
            updated = True
            break

    # If updated, write the modified rows back to the CSV
    if updated:
        with open('database.csv', mode='w', newline='') as database:
            csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerows(rows)  # Write all rows back into the CSV
        print("Session updated successfully.")
    else:
        print("User not found.")



def verify_login(email, password):
    with open('database.csv', mode='r') as database:
        csv_reader = csv.reader(database, delimiter=',')
        for row in csv_reader:
            if len(row) < 4:
                continue  # Skip rows that don't have the expected number of columns
            if row[1] == email and row[2] == password:
                return True
    return False


@app.route("/login", methods=['GET', 'POST'])
def log_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Verify login
        user_found = False
        with open('database.csv', mode='r') as database:
            csv_reader = csv.reader(database)
            for row in csv_reader:
                if len(row) >= 3:  # Ensure the row has enough columns
                    if row[1] == email:  # Check if the email exists
                        user_found = True
                        if row[2] == password:  # Check if the password matches
                            return redirect(url_for('thankyou'))
                        else:
                            flash("Invalid password. Please try again.", "error")
                            return redirect(url_for('login'))  # Invalid password, go back to login
        
        if not user_found:  # If email is not found
            flash("You don't have an account, please sign up", "error")
            return redirect(url_for('signup'))  # Redirect to sign-up page

    return render_template('login.html')  # Render login form if GET request

def write_to_csv(data):
    print("Attempting to write data to CSV")  #x Debugging line
    with open('database.csv', mode='a', newline='') as database:  # Use newline='' to prevent extra line breaks
        name = data["name"]
        email = data["email"]
        password = data["password"]
        session = 1
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, password, session])
        print("Data written successfully")  # Debugging line




@app.route('/sign_up', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()

            # Check if the email already exists
            with open('database.csv', mode='r') as database:
                csv_reader = csv.reader(database)
                for row in csv_reader:
                    if len(row) >= 3 and row[1] == data['email']:  # Check if row has sufficient columns
                        flash("You already have an account, please login", "error")
                        return redirect(url_for('login'))  # Redirect to login page

            # If email doesn't exist, save the data
            write_to_csv(data)
            return redirect('/thankyou.html')

        except Exception as e:
            print("Error:", e)
            return 'Did not save to database'
    else:
        return 'Something went wrong. Try again!!'

@app.route('/submit_account', methods=['POST', 'GET'])
def submit_account():
    if request.method == 'POST':
        try:
            # Collect the form data
            data = request.form.to_dict()

            # Validate the data (e.g., ensure required fields are filled)
            required_fields = ['name', 'age', 'college', 'major', 'classes', 'hobbies']
            for field in required_fields:
                if not data.get(field):
                    flash(f"{field.capitalize()} is required.", "error")
                    return redirect(url_for('account'))  # Redirect back to the account page

            # Save the data to the CSV
            with open('account_data.csv', mode='a', newline='') as database:
                csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([
                    data['name'],
                    data['age'],
                    data['college'],
                    data['major'],
                    data['classes'],
                    data['hobbies']
                ])

            flash("Account information submitted successfully!", "success")
            return redirect(url_for('thankyou'))  # Redirect to a thank-you page

        except Exception as e:
            print("Error:", e)
            flash("An error occurred. Please try again.", "error")
            return redirect(url_for('account'))  # Redirect back to the account page

    return 'Invalid request method.'






# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/submit_form', methods=['POST'])
# def submit_form():

#     port = 465  # For SSL
#     smtp_server = "smtp.gmail.com"
#     sender_email = "hackernewsupdates@gmail.com"  # Enter your address
#     receiver_email = "Suvan8806@gmail.com"  # Enter receiver address
#     password = "efroymraqfvkqtma"

#     # Retrieve data from the form
#     sender= request.form['sender_email']
#     subject = request.form['subject']
#     message = request.form['message']


#     # Create the email message
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject
#     # Attach the message text
#     body = f"Message from: {sender}\n\n{message}"
#     msg.attach(MIMEText(body, 'plain'))
    
    
#     # Send the email
#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#       server.login(sender_email, password)
#       server.sendmail(sender_email, receiver_email, msg.as_string())
#       print("Sent!")

#     return redirect('/thankyou.html')


print("Testing")

@app.route("/thankyou.html") # root directory website
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)