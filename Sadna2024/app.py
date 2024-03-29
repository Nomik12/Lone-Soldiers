from flask import Flask, request, jsonify, render_template
from flask import session

import mysql.connector
import base64
import requests
app = Flask(__name__)
from flask import Flask, redirect, url_for
app.secret_key = 'your_secret_key'


def connect_to_mysql():
    # MySQL configuration
    db_config = {
        'host': "127.0.0.1",
        'user': "root",
        'password': "XXX",
        'database': "lone_soldiers",
    }

    # Create MySQL connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    return conn, cursor

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def Login():
    return render_template('Login.html')

@app.route('/FamilyRegistration', methods=['GET'])
def family_page():
    return render_template('FamilyRegistration.html')

@app.route('/SoldierRegistration', methods=['GET'])
def soldier_page():
    return render_template('SoldierRegistration.html')

@app.route('/SoldierHomePage', methods=['GET'])
def soldier_home_page():
    first_name = session.get('first_name')
    return render_template('SoldierHomePage.html', first_name=first_name)

@app.route('/FamilyHomePage', methods=['GET'])
def family_home_page():
    first_name = session.get('first_name')
    return render_template('FamilyHomePage.html',  first_name=first_name)

@app.route('/UploadItem', methods=['GET'])
def GetUploadItem():
    return render_template('UploadItem.html')

@app.route('/CreateDonationGroup', methods=['GET'])
def GetCreateDonationGroup():
    return render_template('CreateDonationGroup.html')

@app.route('/ValidDonationGroup', methods=['GET'])
def success_page_donation():
    return render_template('ValidDonationGroup.html')

@app.route('/ValidUploadItem', methods=['GET'])
def success_page_item():
    return render_template('ValidUploadItem.html')

@app.route('/ValidFamilyRegistration', methods=['GET'])
def success_page_family_reg():
    return render_template('ValidFamilyRegistration.html')

@app.route('/ValidSoldierRegistration', methods=['GET'])
def success_page_soldier_reg():
    return render_template('ValidSoldierRegistration.html')



# API endpoint for user login
@app.route('/login', methods=['POST'])
def check_credentials():
    try:
        # Get user credentials from request
        username = request.form.get('email')
        password = request.form.get('password')

        conn, cursor = connect_to_mysql()

        # Query to check user credentials in the soldiers table
        soldiers_query = "SELECT * FROM soldiers WHERE email=%s AND password=%s"
        cursor.execute(soldiers_query, (username, password))
        soldier = cursor.fetchone()

        # Query to check user credentials in the families table
        families_query = "SELECT * FROM families WHERE email=%s AND password=%s"
        cursor.execute(families_query, (username, password))
        family = cursor.fetchone()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Check if the user is found in either soldiers or families table
        if soldier:
            session['user_id'] = soldier[0]
            session['first_name'] = soldier[1]

            # Redirect to soldier homepage
            return redirect(url_for('soldier_home_page'))

        elif family:
            session['user_id'] = family[0]
            session['first_name'] = family[1]
            
            # Redirect to family homepage
            return redirect(url_for('family_home_page'))
        else:
            # Invalid credentials
            error_message = 'Invalid username or password'
            return render_template('Login.html', error_message=error_message)
        
    except Exception as e:
        # Handle exceptions
        response = {'error': str(e)}
        return jsonify(response), 500
    
    
@app.route('/registration', methods=['POST'])
def direct_to_registration():
    try:
        user_option = request.form['userOption']
        if user_option == 'soldier':
            return redirect(url_for('soldier_page'))
        elif user_option == 'family':
            return redirect(url_for('family_page'))
        else:
            return "Invalid choice"
    except KeyError:
        return "Invalid choice"


# API endpoint for family sign-up
@app.route('/FamilyRegistration', methods=['POST'])
def FamilyRegistration():
    try:
        # Get family details from request
        id = request.form.get('id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        city = request.form.get('city')
        street = request.form.get('street')
        house_num = int(request.form.get('house_num'))
        family_hobby = request.form.get('family_hobby')
        f = request.files['picture']
        f_name = f.filename
        f.save(f"static/images/{f_name}")
        password = request.form.get('password')

        conn, cursor = connect_to_mysql()
        # Query to insert new family into the families table
        query = "INSERT INTO families (id, first_name, last_name, email, city, street, house_num, family_hobby, picture, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (id, first_name, last_name, email, city, street, house_num, family_hobby, f_name, password))
        conn.commit()  # Commit the changes to the database
        # Close cursor and connection
        cursor.close()
        conn.close()

        # Successful sign-up
        response = {'message': 'Sign-up successful'}
        return redirect(url_for('success_page_family_reg'))

    except Exception as e:
        # Handle exceptions
        response = {'error': str(e)}
        return jsonify(response), 500
    

# API endpoint for Soldier sign-up
@app.route('/SoldierRegistration', methods=['POST'])
def SoldierRegistration():
    try:
        # Get soldier details from request
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birth_date = request.form.get('birth_date')
        email = request.form.get('email')
        city = request.form.get('city')
        street = request.form.get('street')
        house_num = int(request.form.get('house_num'))
        hobby = request.form.get('hobby')
        f = request.files['picture']
        f_name = f.filename
        f.save(f"static/images/{f_name}")
        personal_num = request.form.get('personal_num')
        role = request.form.get('role')
        army_force = request.form.get('army_force')
        army_rank = request.form.get('army_rank')
        release_date = request.form.get('release_date')
        password = request.form.get('password')
        
        conn, cursor = connect_to_mysql()
        # Query to insert new soldier into the soldiers table
        query = "INSERT INTO soldiers (first_name, last_name, birth_date, email, city, street, house_num, hobby, picture, personal_num, role, army_force, army_rank, release_date, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (first_name, last_name, birth_date, email, city, street, house_num, hobby, f_name, personal_num, role, army_force, army_rank, release_date, password))
        conn.commit()  # Commit the changes to the database
        # Close cursor and connection
        cursor.close()
        conn.close()

        # Successful sign-up
        response = {'message': 'Sign-up successful'}
        return redirect(url_for('success_page_soldier_reg'))

    except Exception as e:
        # Handle exceptions
        response = {'error': str(e)}
        return jsonify(response), 500
    


# API endpoint for inserting an item into the inventory table
@app.route('/UploadItem', methods=['POST'])
def add_to_inventory():
    try:
        # Get item details from request
        item_name = request.form.get('item_name')
        category = request.form.get('category')
        manufacturer = request.form.get('manufacturer')
        shelf_years = int(request.form.get('shelf_years'))
        collecting_point = request.form.get('collecting_point')
        phone = request.form.get('phone')
        f = request.files['picture']
        f_name = f.filename
        f.save(f"static/images/{f_name}")
        
        conn, cursor = connect_to_mysql()
        # Query to insert new item into the inventory
        query = "INSERT INTO inventory (item_name, category, manufacturer, shelf_years, collecting_point, phone, picture) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (item_name, category, manufacturer, shelf_years, collecting_point, phone, f_name))
        conn.commit()  # Commit the changes to the database
        # Close cursor and connection
        cursor.close()
        conn.close()

        # Successful insertion
        response = {'message': 'Item added to inventory successfully'}
        return redirect(url_for('success_page_item'))  # Redirect to success page

    except Exception as e:
        # Handle exceptions
        response = {'error': str(e)}
        return jsonify(response), 500


    

# API endpoint for inserting an item into the donation_groups table
@app.route('/CreateDonationGroup', methods=['POST'])
def add_to_donation_groups():
    try:
        # Get donation group details from request
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        purpose = request.form.get('purpose')
        target = int(request.form.get('target'))
        description = request.form.get('description')
        account_number = int(request.form.get('account_number'))
        bank = request.form.get('bank')
        branch = int(request.form.get('branch'))

        conn, cursor = connect_to_mysql()
        # Query to insert new donation group
        query = "INSERT INTO donation_groups (purpose, target, description, account_number, bank, branch, first_name, last_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (purpose, target, description, account_number, bank, branch, first_name, last_name))
        conn.commit()  # Commit the changes to the database
        # Close cursor and connection
        cursor.close()
        conn.close()

        # Successful insertion
        response = {'message': 'Donation group added successfully'}
        return redirect(url_for('success_page_donation'))  # Redirect to success page

    except Exception as e:
        # Handle exceptions
        response = {'error': str(e)}
        return jsonify(response), 500

@app.route('/MoneyDonation', methods=['GET'])
def show_donation_groups():
    try:
        conn, cursor = connect_to_mysql()
        # Query to retrieve all records from the inventory table
        query = "SELECT * FROM donation_groups"
        cursor.execute(query)
        groups_records = cursor.fetchall()
        # Close cursor and connection
        cursor.close()
        conn.close()

        return render_template('MoneyDonation.html', groups_records=groups_records)

    except Exception as e:
        # Handle exceptions
        response = {'error': str(e)}
        return jsonify(response), 500

# Add a new route to fetch inventory records and render the HTML template
@app.route('/GetInventory', methods=['GET'])
def show_inventory():
    try:
        return render_template('SearchItem.html')

    except Exception as e:
        # Handle exceptions
        response = {'error': str(e)}
        return jsonify(response), 500



# Add a new route to fetch inventory records and render the HTML template
@app.route('/GetInventory', methods=['POST'])
def show_filtered_inventory():
    try:

        # Extracting the category value from the form data
        category = request.form.get('category')

        conn, cursor = connect_to_mysql()
        # Query to retrieve records from the inventory table based on the category
        query = "SELECT * FROM inventory WHERE category = %s and taken = false"
        cursor.execute(query, (category,))
        inventory_records = cursor.fetchall()
        # Close cursor and connection
        cursor.close()
        conn.close()

        for i, record in enumerate(inventory_records):
            dest_address = record[5] 
            origin_address = request.form.get('origin')
            
            origin_address = origin_address.replace(" ", "%")
            dest_address = dest_address.replace(" ", "%")

            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?destinations={dest_address}&origins={origin_address}&units=metric&key=XXX"
            r = requests.get(url)
            data = r.json()

            distance_value = data["rows"][0]["elements"][0]["distance"]["text"]
            duration_value = data["rows"][0]["elements"][0]["duration"]["text"]

            # Convert the tuple to a list so that we can modify it
            record_list = list(record)
            
            # Append the new value to the list
            record_list.append(distance_value)
            record_list.append(duration_value)
            
            # Convert the list back to a tuple
            updated_record = tuple(record_list)
            
            # Update the inventory_records list with the updated record
            inventory_records[i] = updated_record
        
        # Sort inventory_records by distance_value in ascending order
        inventory_records = sorted(inventory_records, key=lambda  x: float(x[-2].split()[0]))  # Assuming distance_value is appended at the second last position

        # Render the HTML template with the inventory records
        return render_template('SearchItem.html', inventory_records=inventory_records)

    except Exception as e:
        # Handle exceptions
        response = {'error': str(e)}
        return jsonify(response), 500
    
@app.route('/mark-as-taken', methods=['POST'])
def update_mysql_field_taken():
    try:
        # Get ID from the request form data
        img_id = request.form.get('id')
        user_id = session.get('user_id')
        
        conn, cursor = connect_to_mysql()
        # Update the MySQL field
        cursor.execute("UPDATE inventory SET taken = true, taken_by = %s WHERE id = %s", (user_id, img_id,))
        # cursor.execute("UPDATE inventory SET taken = true WHERE id = %s", (img_id,))
        conn.commit()
        # Close cursor and connection
        cursor.close()
        conn.close()

        return jsonify({'message': 'הפריט שוריין עבורך בהצלחה'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Add a new route to fetch inventory records and render the HTML template
@app.route('/ViewSoldierItems', methods=['GET'])
def ViewSoldierItems():
    try:
        soldier_id = session.get('user_id')

        conn, cursor = connect_to_mysql()
        # Query to retrieve all records from the inventory table
        query = "SELECT * FROM inventory WHERE taken_by = %s"
        cursor.execute(query, (soldier_id,))
        inventory_records = cursor.fetchall()
        # Close cursor and connection
        cursor.close()
        conn.close()

        return render_template('ViewSoldierItems.html', inventory_records=inventory_records)

    except Exception as e:
        # Handle exceptions
        response = {'error': str(e)}
        return jsonify(response), 500
    
# Run the Flask app 
if __name__ == '__main__':
    app.run(debug=True)
