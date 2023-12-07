from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import jsonify
import oracledb

app = Flask(__name__)
app.secret_key = 'strawhats'
# Define a dictionary of users and their passwords (plaintext, not recommended for production)
users = {
    'luffy': 'rubber',
    'Zoro': 'swordsman',
}

#pw = getpass.getpass("Enter password: ")
oracledb.init_oracle_client()
print(oracledb.clientversion())

def get_db_connection():
    dsn_t = oracledb.makedsn('navydb.artg.arizona.edu', 1521, 'ORCL')
    connection = oracledb.connect(user="mis531groupS2P", password="vkpK#$}Z73nn68R", dsn=dsn_t, disable_oob=True)
    return connection

# Route to render the login form
@app.route('/')
def login_form():
    return render_template('login.html')

# Route to handle the form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if the username and password match a predefined set
    if username in users and users[username] == password:
        # Authentication successful, redirect to index.html
        return redirect(url_for('index'))
    else:
        flash("User Name or Password is incorrect!")
        # Authentication failed
        return render_template('login.html', error='Authentication failed')

# Route for the index page
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


# ==============================================+

# Placeholder function to fetch client data from the database
def get_clients_data():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("select client_id, ahccs_id, firstname, lastname, street, city, state, zipcode, status, activesince, inactivedate, age, gender, primarylanguage from clients order by client_id")
        clients = cursor.fetchall()
        return clients
    finally:
        cursor.close()
        connection.close()

@app.route('/api/patient_management', methods=['GET'])
def api_get_clients():
    clients_data = get_clients_data()
    return jsonify(clients_data)

@app.route('/patient_management', methods=['GET'])
def patient_management():
    clients_data = get_clients_data()
    return render_template('patient_management.html', clients=clients_data)


@app.route('/addPatients', methods=['POST'])
def add_patient():
    if request.method == 'POST':
        # Get the form data from the request
        ahccs_id = request.form.get('PatientAHCCSInsert').strip()
        first_name = request.form.get('PatientFNAMEInsert').strip()
        last_name = request.form.get('PatientLNAMEInsert').strip()
        street = request.form.get('PatientStreetInsert').strip()
        city = request.form.get('PatientCityInsert').strip()
        state = request.form.get('PatientStateInsert').strip()
        gender = request.form.get('PatientGenderInsert').strip()

        # Insert the data into the database
        insert_patient_data(ahccs_id, first_name, last_name, street, city, state, gender)

        # Redirect to the patient management page or any other desired page
        return redirect(url_for('patient_management'))
    return 'Invalid Request Method'


# Function to insert data into the database
def insert_patient_data(ahccs_id, first_name, last_name, street, city, state, gender):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        # Adjust the SQL query based on your table structure
        sqlQuery = "INSERT INTO clients (ahccs_id, firstname, lastname, street, city, state, gender) VALUES (:ahccs_id, :firstname, :lastname, :street, :city, :state, :gender)"
        cursor.execute(sqlQuery, ahccs_id = ahccs_id, firstname = first_name, lastname=last_name, street=street, city = city, state=state,gender=gender)
        connection.commit()
    finally:
        cursor.close()
        connection.close()

@app.route('/updatePatients', methods=['POST'])
def update_patient():
    if request.method == 'POST':
        # Get the form data from the request
        patient_id = request.form.get('PatientIdUpdate')
        ahccs_id = request.form.get('PatientAHCCSUpdate')
        first_name = request.form.get('PatientFNAMEUpdate')
        last_name = request.form.get('PatientLNAMEUpdate')
        street = request.form.get('PatientStreetUpdate')
        city = request.form.get('PatientCityUpdate')
        state = request.form.get('PatientStateUpdate')
        gender = request.form.get('PatientGenderUpdate')

        # Update the data in the database
        update_patient_data(patient_id, ahccs_id, first_name, last_name, street, city, state, gender)

        # Redirect to the patient management page or any other desired page
        return redirect(url_for('patient_management'))

    return 'Invalid Request Method'

# Function to update data in the database
def update_patient_data(patient_id, ahccs_id, first_name, last_name, street, city, state, gender):
    connection = get_db_connection()

    colNames = ["ahccs_id", "firstname", "lastname", "street", "city", "state", "gender"]
    colValues = [ahccs_id, first_name, last_name, street, city, state, gender]
    try:
        cursor = connection.cursor()
        for index in range(len(colValues)):
            if colValues[index] != "":
                sqlQuery = "UPDATE CLIENTS SET " + colNames[index] + " = :colValue WHERE CLIENT_ID = :patient_id"
                cursor.execute(sqlQuery, colValue = colValues[index], patient_id = patient_id)

    finally:
        # Close the cursor and connection in a finally block
        connection.commit()
        cursor.close()
        connection.close()


@app.route('/deletePatients', methods=['POST'])
def delete_patient():
    connection = get_db_connection()
    patient_id = request.form.get('PatientId')  
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM  clients WHERE client_id = :clientid", clientid = patient_id)
    finally:
        # Close the cursor and connection in a finally block
        connection.commit()
        cursor.close()
        connection.close()


        # Redirect to the patient management page or any other desired page
    return redirect(url_for('patient_management'))

# =================================================================

# Placeholder function to fetch provider data from the database
def get_providers_data():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("select provider_id, firstname, lastname, email, street, city, state, zipcode, status, startdate, inactivedate from providers order by provider_id")
        clients = cursor.fetchall()
        return clients
    finally:
        cursor.close()
        connection.close()

@app.route('/api/provider_management', methods=['GET'])
def api_get_providers():
    providers_data = get_providers_data()
    return jsonify(providers_data)

@app.route('/provider_management')
def provider_management():
    providers_data = get_providers_data()
    return render_template('provider_management.html', providers=providers_data)

@app.route('/insertProviders', methods=['POST'])
def add_provider():
    if request.method == 'POST':
        # Get the form data from the request
        first_name = request.form.get('insertFNameProvider').strip()
        last_name = request.form.get('insertLNameProvider').strip()
        email = request.form.get('insertEmailProvider').strip()
        street = request.form.get('insertStreetProvider').strip()
        city = request.form.get('insertCityProvider').strip()
        state = request.form.get('insertStateProvider').strip()

        # Insert the data into the database
        insert_provider_data(first_name, last_name, email, street, city, state)

        # Redirect to the patient management page or any other desired page
        return redirect(url_for('provider_management'))
    return 'Invalid Request Method'


# Function to insert data into the database
def insert_provider_data(first_name, last_name, email, street, city, state):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        # Adjust the SQL query based on your table structure
        sqlQuery = "INSERT INTO providers (firstname, lastname, email, street, city, state) VALUES (:firstname, :lastname, :email, :street, :city, :state)"
        cursor.execute(sqlQuery, firstname = first_name, lastname=last_name, email=email, street=street, city = city, state=state)
        connection.commit()
    finally:
        cursor.close()
        connection.close()

@app.route('/updateProviders', methods=['POST'])
def update_provider():
    if request.method == 'POST':
        # Get the form data from the request
        provider_id = request.form.get('updateProviderId')
        first_name = request.form.get('updateFNameProvider')
        last_name = request.form.get('updateLNameProvider')
        email = request.form.get('updateEmailProvider')
        street = request.form.get('updateStreetProvider')
        city = request.form.get('updateCityProvider')
        state = request.form.get('updateStateProvider')


        # Update the data in the database
        update_provider_data(provider_id, first_name, last_name, email, street, city, state)

        # Redirect to the patient management page or any other desired page
        return redirect(url_for('provider_management'))
    return 'Invalid Request Method'

# Function to update data in the database
def update_provider_data(provider_id, first_name, last_name, email, street, city, state):
    connection = get_db_connection()

    colNames = ["firstname", "lastname", "email", "street", "city", "state"]
    colValues = [first_name, last_name, email, street, city, state]
    try:
        cursor = connection.cursor()
        for index in range(len(colValues)):
            if colValues[index] != "":
                sqlQuery = "UPDATE PROVIDERS SET " + colNames[index] + " = :colValue WHERE PROVIDER_ID = :provider_id"
                cursor.execute(sqlQuery, colValue = colValues[index], provider_id = provider_id)
    finally:
        # Close the cursor and connection in a finally block
        connection.commit()
        cursor.close()
        connection.close()

@app.route('/deleteProviders', methods=['POST'])
def delete_provider():
    connection = get_db_connection()
    provider_id = request.form.get('ProviderId')  
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM providers WHERE provider_id = :providerid", providerid = provider_id)
    finally:
        # Close the cursor and connection in a finally block
        connection.commit()
        cursor.close()
        connection.close()


        # Redirect to the patient management page or any other desired page
    return redirect(url_for('provider_management'))

# =========================================================

# Placeholder function to fetch employee data from the database
def get_employees_data():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("select employee_id, firstname, lastname, email, gender, dateofbirth, age, position from employees order by employee_id")
        clients = cursor.fetchall()
        return clients
    finally:
        cursor.close()
        connection.close()

@app.route('/api/employee_management', methods=['GET'])
def api_get_employees():
    employees_data = get_employees_data()
    return jsonify(employees_data)

@app.route('/employee_management')
def employee_management():
    employees_data = get_employees_data()
    return render_template('employee_management.html', employees=employees_data)

@app.route('/index.html')
def dashboard_management():
    return render_template('index.html')

@app.route('/insertEmployees', methods=['POST'])
def add_employees():
        # Get the form data from the request
        first_name = request.form.get('insertEmployeeFName').strip()
        last_name = request.form.get('insertEmployeeLName').strip()
        email = request.form.get('insertEmployeeEmail').strip()
        gender = request.form.get('insertEmployeeGender').strip()
        position = request.form.get('insertEmployeePosition').strip()

        # Insert the data into the database
        insert_employee_data(first_name, last_name, email, gender, position)

        # Redirect to the employee management page
        return redirect(url_for('employee_management'))

# Function to insert data into the database
def insert_employee_data(first_name, last_name, email, gender, position):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        # Adjust the SQL query based on your table structure
        sqlQuery = "INSERT INTO employees (firstname, lastname, email, gender, position) VALUES (:firstname, :lastname, :email, :gender, :position)"
        cursor.execute(sqlQuery, firstname = first_name, lastname=last_name, email=email, gender=gender, position=position)
        connection.commit()
    finally:
        cursor.close()
        connection.close()

@app.route('/updateEmployees', methods=['POST'])
def update_employee():
        # Get the form data from the request
        employee_id = request.form.get('updateEmployeeId')
        first_name = request.form.get('updateEmployeeFName')
        last_name = request.form.get('updateEmployeeLName')
        email = request.form.get('updateEmployeeEmail')
        gender = request.form.get('updateEmployeeGender')
        position = request.form.get('updateEmployeePosition')

        # Update the data in the database
        update_employees_data(employee_id, first_name, last_name, email, gender, position)

        # Redirect to the patient management page or any other desired page
        return redirect(url_for('employee_management'))

# Function to update data in the database
def update_employees_data(employee_id, first_name, last_name, email, gender, position):
    connection = get_db_connection()

    colNames = ["firstname", "lastname", "email", "gender", "position"]
    colValues = [first_name, last_name, email, gender, position]
    try:
        cursor = connection.cursor()
        for index in range(len(colValues)):
            if colValues[index] != "":
                sqlQuery = "UPDATE EMPLOYEES SET " + colNames[index] + " = :colValue WHERE EMPLOYEE_ID = :employee_id"
                cursor.execute(sqlQuery, colValue = colValues[index], employee_id = employee_id)
    finally:
        # Close the cursor and connection in a finally block
        connection.commit()
        cursor.close()
        connection.close()

@app.route('/deleteEmployees', methods=['POST'])
def delete_employee():
    connection = get_db_connection()
    employee_id = request.form.get('EmployeeId')  
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM employees WHERE employee_id = :employeeid", employeeid = employee_id)
    finally:
        # Close the cursor and connection in a finally block
        connection.commit()
        cursor.close()
        connection.close()

        # Redirect to the patient management page or any other desired page
    return redirect(url_for('employee_management'))

# =====================================================================================================+

# Placeholder function to fetch client data from the database
def get_query_one():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
select 
    p.firstname,
    mv.hoursworked,
    mv.hourlyrate,
    (mv.hoursworked * mv.hourlyrate) AmountEarned,
    dense_rank() over(order by (mv.hoursworked * mv.hourlyrate)) ae_rank
from monitor_visits mv
join providers p 
on mv.provider_id = p.provider_id
                       """)
        query_one = cursor.fetchall()
        return query_one
    finally:
        cursor.close()
        connection.close()

@app.route('/api/query_one', methods=['GET'])
def api_get_query_one():
    query_one = get_query_one()
    return jsonify(query_one)

@app.route('/query_one', methods=['GET'])
def query_one():
    query_one = get_query_one()
    return render_template('index.html', query_one=query_one)

# Placeholder function to fetch client data from the database
def get_query_two():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                    SELECT
    Clients.*,
    Insurance.insurance_provider,
    Insurance.policyNumber,
    Payment.paymentDate,
    Payment.amount
FROM
    Clients
LEFT JOIN Insurance ON Clients.insurance_id = Insurance.insurance_id
LEFT JOIN (
    SELECT
        Invoice.client_id,
        MAX(Payment.paymentDate) AS latestPaymentDate
    FROM
        Invoice
    JOIN Payment ON Invoice.invoice_id = Payment.invoice_id
    GROUP BY
        Invoice.client_id
) LatestPayment ON Clients.client_id = LatestPayment.client_id
LEFT JOIN Payment ON LatestPayment.latestPaymentDate = Payment.paymentDate AND Clients.client_id = Payment.client_id
                       """)
        query_two = cursor.fetchall()
        return query_two
    finally:
        cursor.close()
        connection.close()

@app.route('/api/query_two', methods=['GET'])
def api_get_query_two():
    query_two = get_query_two()
    return jsonify(query_two)

@app.route('/query_two', methods=['GET'])
def query_two():
    query_two = get_query_two()
    return render_template('index.html', query_two=query_two)

# Placeholder function to fetch client data from the database
def get_query_three():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                    SELECT c.client_id,
    c.firstname || ' ' || c.lastname as "Client Name",
    p.lastname  || ' ' || p.firstname as "Contact Name",
    Relationship,
    pp.Phonenumber,
    pe.email
FROM clients c
JOIN PERSON_CONTACT P ON p.contact_id = c.contact_id
JOIN PERSON_CONTACT_PHONE pp ON pp.contact_id = p.contact_id 
JOIN PERSON_CONTACT_EMAIL pe ON p.contact_id = pe.contact_id
JOIN EMERGENCY_CONTACTS ec ON ec.contact_id = p.contact_id
                       """)
        query_three = cursor.fetchall()
        return query_three
    finally:
        cursor.close()
        connection.close()

@app.route('/api/query_three', methods=['GET'])
def api_get_query_three():
    query_three = get_query_three()
    return jsonify(query_three)

@app.route('/query_three', methods=['GET'])
def query_three():
    query_three = get_query_three()
    return render_template('index.html', query_three=query_three)

# Placeholder function to fetch client data from the database
def get_query_four():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                    Select e.Employee_id, 
    e.firstname || ' ' || e.lastname as "Employee Name",
    TrainingName as "Training Name",
    STATUS as "Status",
    DATECOMPLETED AS "Date Completed"
From EMPLOYEES e 
JOIN Compliance c ON c.employee_id = e.employee_id""")
        query_four = cursor.fetchall()
        return query_four
    finally:
        cursor.close()
        connection.close()

@app.route('/api/query_four', methods=['GET'])
def api_get_query_four():
    query_four = get_query_four()
    return jsonify(query_four)

@app.route('/query_four', methods=['GET'])
def query_four():
    query_four = get_query_four()
    return render_template('index.html', query_four=query_four)

# Placeholder function to fetch client data from the database
def get_query_five():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                    SELECT p.provider_id, p.Firstname as  "Provider Name", Servicetype as "Services ", S.Startdate as " Service Start Date"
From Providers p 
Join Offer_Services os ON p.provider_id = os.provider_id
JOIN services s ON s.service_Code = OS.service_code
                    """)
        query_five = cursor.fetchall()
        return query_five
    finally:
        cursor.close()
        connection.close()

@app.route('/api/query_five', methods=['GET'])
def api_get_query_five():
    query_five = get_query_five()
    return jsonify(query_five)

@app.route('/query_five', methods=['GET'])
def query_five():
    query_five = get_query_five()
    return render_template('index.html', query_five=query_five)

# Placeholder function to fetch client data from the database
def get_query_six():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                    SELECT e.employee_id,
       e.firstname || ' ' || e.lastname as "Employee Name",
       Position,
       s.schedule_date as "Date",
       shiftname as "Shift Name",
       sh.starttime as "Start Time"
FROM EMPLOYEES e
JOIN SCHEDULE s ON s.employee_id = e.employee_id
JOIN SHIFT sh ON sh.employee_id = e.employee_id
                    """)
        query_six = cursor.fetchall()
        return query_six
    finally:
        cursor.close()
        connection.close()

@app.route('/api/query_six', methods=['GET'])
def api_get_query_six():
    query_six = get_query_six()
    return jsonify(query_six)

@app.route('/query_six', methods=['GET'])
def query_six():
    query_six = get_query_six()
    return render_template('index.html', query_six=query_six)

# Placeholder function to fetch client data from the database
def get_query_seven():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                    SELECT
    clients.Client_id,
    clients.firstname || ' ' || clients.lastname as "Client Name",
    Insurance.insurance_provider,
    Insurance.policyNumber,
    Payment.paymentDate,
    Payment.amount
FROM
    Clients 
LEFT JOIN Insurance ON Clients.insurance_id = Insurance.insurance_id
LEFT JOIN (
    SELECT
        Invoice.client_id,
        MAX(Payment.paymentDate) AS latestPaymentDate
    FROM
        Invoice
    JOIN Payment ON Invoice.invoice_id = Payment.invoice_id
    GROUP BY
        Invoice.client_id
) LatestPayment ON Clients.client_id = LatestPayment.client_id
LEFT JOIN Payment ON LatestPayment.latestPaymentDate = Payment.paymentDate AND Clients.client_id = Payment.client_id
                    """)
        query_seven = cursor.fetchall()
        return query_seven
    finally:
        cursor.close()
        connection.close()

@app.route('/api/query_seven', methods=['GET'])
def api_get_query_seven():
    query_seven = get_query_seven()
    return jsonify(query_seven)

@app.route('/query_seven', methods=['GET'])
def query_seven():
    query_seven = get_query_seven()
    return render_template('index.html', query_seven=query_seven)

# Placeholder function to fetch client data from the database
def get_query_eight():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                    WITH RankedProviders AS (
    SELECT
        p.provider_id,
        p.firstName,
        p.lastName,
        s.serviceType,
        RANK() OVER (PARTITION BY p.provider_id ORDER BY COUNT(mv.client_id) DESC) AS serviceRank
    FROM
        Providers p
    JOIN
        Offer_Services os ON p.provider_id = os.provider_id
    JOIN
        Services s ON os.service_code = s.service_code
    LEFT JOIN
        Monitor_Visits mv ON p.provider_id = mv.provider_id
    GROUP BY
        p.provider_id, p.firstName, p.lastName, s.serviceType
)
SELECT
    rp.provider_id,
    rp.firstName,
    rp.lastName,
    rp.serviceType,
    rp.serviceRank,
    CASE
        WHEN rp.serviceRank = 1 THEN 'Top Service'
        WHEN rp.serviceRank <= 3 THEN 'Highly Ranked'
        ELSE 'Standard'
    END AS serviceRankCategory
FROM
    RankedProviders rp
WHERE
    rp.serviceRank <= 3
                    """)
        query_eight = cursor.fetchall()
        return query_eight
    finally:
        cursor.close()
        connection.close()

@app.route('/api/query_eight', methods=['GET'])
def api_get_query_eight():
    query_eight = get_query_eight()
    return jsonify(query_eight)

@app.route('/query_eight', methods=['GET'])
def query_eight():
    query_eight = get_query_eight()
    return render_template('index.html', query_eight=query_eight)

# Placeholder function to fetch client data from the database
def get_query_nine():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                    WITH ProviderHourlyRates AS (
    SELECT
        p.provider_id,
        p.firstName,
        p.lastName,
        s.serviceType,
        AVG(s.servicecharge) AS averageHourlyRate,
        RANK() OVER (PARTITION BY s.serviceType ORDER BY AVG(s.servicecharge) DESC) AS rankHigh,
        RANK() OVER (PARTITION BY s.serviceType ORDER BY AVG(s.servicecharge) ASC) AS rankLow
    FROM
        Providers p
    JOIN
        Offer_Services os ON p.provider_id = os.provider_id
    JOIN
        Services s ON os.service_code = s.service_code
    GROUP BY
        p.provider_id, p.firstName, p.lastName, s.serviceType
)
SELECT
    phr.provider_id,
    phr.firstName,
    phr.lastName,
    phr.serviceType,
    phr.averageHourlyRate,
    CASE
        WHEN phr.rankHigh = 1 THEN 'Highest Rate'
        WHEN phr.rankLow = 1 THEN 'Lowest Rate'
        ELSE 'Standard Rate'
    END AS rateCategory
FROM
    ProviderHourlyRates phr
WHERE
    phr.rankHigh = 1 OR phr.rankLow = 1
                    """)
        query_nine = cursor.fetchall()
        return query_nine
    finally:
        cursor.close()
        connection.close()

@app.route('/api/query_nine', methods=['GET'])
def api_get_query_nine():
    query_nine = get_query_nine()
    return jsonify(query_nine)

@app.route('/query_nine', methods=['GET'])
def query_nine():
    query_nine = get_query_nine()
    return render_template('index.html', query_nine=query_nine)

# Placeholder function to fetch client data from the database
def get_query_ten():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
                   SELECT C.client_id,
       c.firstname || ' ' || c.lastname as "Client Name", 
       e.firstname || ' ' || e.lastname as "Doctor Name", 
       Diagnosis, 
       Medication, 
       mr.Startdate as "Treatment Start Date", 
       mr.Enddate as "Treatment End date"
FROM Clients c 
JOIN providers p ON c.client_id = p.client_id
JOIN employees e on e.provider_id = p.provider_id
JOIN MEDICAL_RECORD_DIAGNOSIS m ON m.client_id = c.client_id
JOIN MEDICAL_RECORD_MEDICATION rm ON rm.client_id = c.client_id
JOIN MEDICAL_RECORDS mr on mr.client_id = c.client_id
                    """)
        query_ten = cursor.fetchall()
        return query_ten
    finally:
        cursor.close()
        connection.close()

@app.route('/api/query_ten', methods=['GET'])
def api_get_query_ten():
    query_nine = get_query_ten()
    return jsonify(query_nine)

@app.route('/query_ten', methods=['GET'])
def query_ten():
    query_ten = get_query_ten()
    return render_template('index.html', query_ten=query_ten)

# =====================================================================================================+



if __name__ == '__main__':
    app.run(debug=True)