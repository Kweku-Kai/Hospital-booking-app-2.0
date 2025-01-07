from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',  # Replace with your MySQL host
        user='root',  # Replace with your MySQL username
        password='password',  # Replace with your MySQL password
        database='patient_booking_system'
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO patients (patientId, firstName, lastName, gender, contactNumber)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['patientId'], data['firstName'], data['lastName'], data['gender'], data['contactNumber']))
        connection.commit()
    except Error as e:
        return jsonify(success=False, error=str(e))
    finally:
        cursor.close()
        connection.close()
    return jsonify(success=True)

@app.route('/book', methods=['POST'])
def book():
    data = request.form.to_dict()
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO bookings (patientId, caseType, purpose, bookingDate, bookingTime)
            VALUES (%s, %s, %s, CURDATE(), %s)
        """, (data['bookingPatientId'], data['caseType'], data['purpose'], data['bookingTime']))
        connection.commit()
    except Error as e:
        return jsonify(success=False, error=str(e))
    finally:
        cursor.close()
        connection.close()
    return jsonify(success=True)

@app.route('/bookings')
def get_bookings():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bookings WHERE bookingDate = CURDATE()")
    bookings = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(bookings)

@app.route('/search_results')
def search_results():
    patient_id = request.args.get('patientId')
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE patientId = %s", (patient_id,))
    patient = cursor.fetchone()
    if patient:
        cursor.execute("SELECT * FROM bookings WHERE patientId = %s", (patient_id,))
        patient_bookings = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('search_results.html', patient=patient, bookings=patient_bookings)
    else:
        cursor.close()
        connection.close()
        return 'Patient not found', 404

if __name__ == '__main__':
    app.run(debug=True)
