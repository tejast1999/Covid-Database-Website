from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, static_url_path='/static')

# Create the user table in the SQLite database
conn = sqlite3.connect('vaccine.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS user
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   aadhaar_number TEXT NOT NULL,
                   name TEXT NOT NULL,
                   dob TEXT NOT NULL,
                   mobile_no TEXT NOT NULL,
                   dose TEXT NOT NULL,
                   vaccine_name TEXT NOT NULL)''')
conn.commit()
conn.close()

# Define the route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get the Aadhaar number and mobile number entered by the user
        aadhaar_number = request.form["aadhaar_number"]
        mobile_no = request.form["mobile_no"]

        # Connect to the SQLite database
        conn = sqlite3.connect('vaccine.db')
        cursor = conn.cursor()

        # Check if the user exists in the database
        cursor.execute("SELECT * FROM user WHERE aadhaar_number = ? AND mobile_no = ?", (aadhaar_number, mobile_no))
        user = cursor.fetchone()

        # Close the database connection
        conn.close()

        # If user exists, redirect to the dashboard page
        if user:
            return redirect(url_for('dashboard', aadhaar_number=aadhaar_number))

        # If user doesn't exist, display an error message
        else:
            error_message = "Invalid Aadhaar number or mobile number"
            return render_template("login.html", error_message=error_message)

    # If method is GET, display the login page
    else:
        return render_template("login.html")

# Define the route for the dashboard page
@app.route('/dashboard/<aadhaar_number>', methods=['GET', 'POST'])
def dashboard(aadhaar_number):
    # Connect to the SQLite database
    conn = sqlite3.connect('vaccine.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Get the form data submitted by the user
        new_dose = request.form['dose']
        new_vaccine_name = request.form['vaccine_name']

        # Update the user's details in the database
        cursor.execute("UPDATE user SET dose = ?, vaccine_name = ? WHERE aadhaar_number = ?",
                       (new_dose, new_vaccine_name, aadhaar_number))
        conn.commit()

        # Fetch the updated user details from the database
        cursor.execute("SELECT * FROM user WHERE aadhaar_number = ?", (aadhaar_number,))
        user = cursor.fetchone()

        # Close the database connection
        conn.close()

        # Render the dashboard template with the updated user details
        return render_template('dashboard.html', user=user, success_message='Details updated successfully!')

    else:
        # Get the user's details from the database
        cursor.execute("SELECT * FROM user WHERE aadhaar_number = ?", (aadhaar_number,))
        user = cursor.fetchone()

        # Close the database connection
        conn.close()

        # Render the dashboard template with the user's details
        return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

# Define the route for registering a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the form data submitted by the user
        aadhaar_number = request.form['aadhaar_number']
        name = request.form['name']
        dob = request.form['dob']
        mobile_no = request.form['mobile_no']
        dose = request.form['dose']
        vaccine_name = request.form['vaccine_name']

        # Connect to the SQLite database
        conn = sqlite3.connect('vaccine.db')
        cursor = conn.cursor()

        # Insert the new user into the database
        cursor.execute("INSERT INTO user (aadhaar_number, name, dob, mobile_no, dose, vaccine_name) VALUES (?, ?, ?, ?, ?, ?)",
                       (aadhaar_number, name, dob, mobile_no, dose, vaccine_name))
        conn.commit()

        # Close the database connection
        conn.close()

        # Redirect to the login page
        return redirect(url_for('login'))

    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)