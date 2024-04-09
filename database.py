import mysql.connector
from mysql.connector import connect, Error
def connect_to_database():
   try:
       db = mysql.connector.connect(
           host='localhost',
           database='projectdb',
           user='root',
           password='1201838'
       )
       return db
   except mysql.connector.Error as e:
       print("Database Connection Error:", str(e))  # Handle GUI display in `gui.py`
       return None

def perform_insert(db_connection, customer_data):
   cursor = db_connection.cursor()
   # Check if the CustomerID already exists
   try:
       cursor.execute("SELECT CustomerID FROM Customer WHERE CustomerID = %s", (customer_data['Customer ID'],))
       if cursor.fetchone():
           return False, "Customer ID already exists."
       dob_correct_format = customer_data['Date of Birth']
       cursor.execute("""
           INSERT INTO Customer (CustomerID, Cname, DateOfBirth, ContactNumber, Email)
           VALUES (%s, %s, %s, %s, %s)
       """, (
           customer_data['Customer ID'],
           customer_data['Name'],
           dob_correct_format,
           customer_data['Contact Number'],
           customer_data['Email']
       ))
       db_connection.commit()
       return True, "Customer inserted successfully"
   except mysql.connector.Error as e:
       db_connection.rollback()
       return False, str(e)
   finally:
       cursor.close()


def fetch_all_customers(db_connection):
   cursor = db_connection.cursor()
   try:
       cursor.execute("SELECT * FROM Customer")
       return cursor.fetchall()  # Returns a list of tuples representing customer rows
   except mysql.connector.Error as e:
       print("Error fetching customers:", str(e))
       return []
   finally:
       cursor.close()
def delete_insurancepolicy_id(db_connection, insurancepolicyid):
    cursor = db_connection.cursor()
    try:
        cursor.execute("SELECT * FROM have_insurancepolicy WHERE PolicyNo = %s", (insurancepolicyid,))
        if cursor.fetchone() is None:
            return False, "Insurancepolicy ID does not exist."
        cursor.execute("SELECT CarID FROM have_insurancepolicy WHERE PolicyNo = %s", (insurancepolicyid,))
        car_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute("DELETE FROM coveredperson WHERE PolicyNo = %s", (insurancepolicyid,))
        cursor.execute("DELETE FROM have_insurancepolicy WHERE PolicyNo = %s", (insurancepolicyid,))
        for car_id in car_ids:
            cursor.execute("DELETE FROM pay_payment WHERE CarID = %s", (car_id,))
            cursor.execute("SELECT COUNT(*) FROM own_car WHERE CarID = %s", (car_id,))
            car_count = cursor.fetchone()[0]
            if car_count == 1:
                cursor.execute("DELETE FROM own_car WHERE CarID = %s", (car_id,))
        for car_id in car_ids:
            cursor.execute(
                "SELECT COUNT(*) FROM own_car WHERE CustomerID IN (SELECT CustomerID FROM own_car WHERE CarID = %s)",
                (car_id,))
            car_count = cursor.fetchone()[0]
            if car_count == 0:
                cursor.execute(
                    "DELETE FROM Customer WHERE CustomerID IN (SELECT CustomerID FROM own_car WHERE CarID = %s)",
                    (car_id,))
        db_connection.commit()
        return True, "Insurancepolicy and associated records deleted successfully."
    except mysql.connector.Error as e:
        db_connection.rollback()
        return False, str(e)
    finally:
        cursor.close()
def perform_car_insert(db_connection, car_data):
    cursor = db_connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO own_car (CarID, Model, ManufactureYear, RegistrationNumber, CustomerID)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            car_data['CarID'],
            car_data['Model'],
            car_data['ManufactureYear'],
            car_data['RegistrationNumber'],
            car_data['CustomerID']
        ))

        db_connection.commit()
        return True, "Car inserted successfully"
    except mysql.connector.Error as e:
        db_connection.rollback()
        return False, str(e)
    finally:
        cursor.close()
import mysql.connector


def insurancepolicy_insert(db_connection, insurancepolicy_data):
    cursor = db_connection.cursor()
    try:
        # Check if 'StartDate' is in the insurancepolicy_data dictionary
        if 'StartDate' not in insurancepolicy_data:
            raise ValueError("Start Date is required.")
        cursor.execute("""
            INSERT INTO have_insurancepolicy (StartDate, EndDate, CoverageType, PremiumAmount, CarID)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            insurancepolicy_data['StartDate'],
            insurancepolicy_data['EndDate'],
            insurancepolicy_data['CoverageType'],
            insurancepolicy_data['PremiumAmount'],
            insurancepolicy_data['CarID'],
        ))

        cursor.execute("SELECT LAST_INSERT_ID()")
        policy_no = cursor.fetchone()[0]
        db_connection.commit()

        return True, "Insurance policy inserted successfully", {'policy_no': policy_no}
    except mysql.connector.Error as e:
        db_connection.rollback()
        return False, str(e), None
    except ValueError as ve:
        return False, str(ve), None
    finally:
        cursor.close()


def payment_insert(db_connection, payment_data):
    cursor = db_connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO pay_payment ( Amount, PaymentDate, PaymentMethod,CarID)
            VALUES ( %s, %s, %s , %s)
        """, (
            payment_data['Amount'],
            payment_data['PaymentDate'],
            payment_data['PaymentMethod'],
            payment_data['CarID'],
        ))

        db_connection.commit()
        return True, "payment inserted successfully"
    except mysql.connector.Error as e:
        db_connection.rollback()
        return False, str(e)
    finally:
        cursor.close()

def coveredperson_insert(db_connection, coveredperson_data):
    cursor = db_connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO coveredperson ( CoveredPersonID, coveredName,PolicyNo)
            VALUES ( %s, %s,%s)
        """, (
            coveredperson_data['CoveredPersonID'],
            coveredperson_data['coveredName'],
            coveredperson_data['PolicyNo']
        ))
        db_connection.commit()
        return True, "coveredperson inserted successfully"
    except mysql.connector.Error as e:
        db_connection.rollback()
        return False, str(e)
    finally:
        cursor.close()
def fetch_all_CoveredPerson(db_connection):
   cursor = db_connection.cursor()
   try:
       cursor.execute("SELECT * FROM coveredperson")
       return cursor.fetchall()  # Returns a list of tuples representing customer rows
   except mysql.connector.Error as e:
       print("Error fetching coveredperson:", str(e))
       return []
   finally:
       cursor.close()
def fetch_all_insurancepolicy(db_connection):
   cursor = db_connection.cursor()
   try:
       cursor.execute("SELECT * FROM have_insurancepolicy")
       return cursor.fetchall()  # Returns a list of tuples representing customer rows
   except mysql.connector.Error as e:
       print("Error fetching insurancepolicy:", str(e))
       return []
   finally:
       cursor.close()
def fetch_all_own_car(db_connection):
   cursor = db_connection.cursor()
   try:
       cursor.execute("SELECT * FROM own_car")
       return cursor.fetchall()  # Returns a list of tuples representing customer rows
   except mysql.connector.Error as e:
       print("Error fetching car:", str(e))
       return []
   finally:
       cursor.close()
def fetch_all_own_pay_payment(db_connection):
   cursor = db_connection.cursor()
   try:
       cursor.execute("SELECT * FROM pay_payment")
       return cursor.fetchall()  # Returns a list of tuples representing customer rows
   except mysql.connector.Error as e:
       print("Error fetching payment:", str(e))
       return []
   finally:
       cursor.close()




def search_CAR(car_ID):
    CAR_data = {}
    try:
        with connect(
                host='localhost',
                database='projectdb',
                user='root',
                password='1201838'
        ) as connection:
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM own_car WHERE CarID = %s"
                data = (car_ID,)
                cursor.execute(query, data)
                car = cursor.fetchone()
                #
                if car:
                    CAR_data["CarID"] = car[0]
                    CAR_data["Model"] = car[1]
                    CAR_data["Manu facture Year"] = car[2]
                    CAR_data["Registration Number"] = car[3]
                    cursor1 = connection.cursor()
                    query = "SELECT * FROM customer WHERE CustomerID = %s"
                    datacustomer = (car[4],)
                    cursor1.execute(query, datacustomer)
                    customer = cursor1.fetchone()
                    pay_payment = connection.cursor()
                    query = "SELECT * FROM pay_payment WHERE CarID = %s"
                    pay_payment2 = (car[0],)
                    pay_payment.execute(query, pay_payment2)
                    pay_payment23 = pay_payment.fetchone()
                    if customer:
                        insurancepolicy = connection.cursor()
                        query = "SELECT * FROM have_insurancepolicy WHERE CarID = %s"
                        datahave_insurancepolicy = (car[0],)
                        insurancepolicy.execute(query, datahave_insurancepolicy)
                        have_insurancepolicy = insurancepolicy.fetchone()
                        CAR_data["CustomerID"] = customer[0]
                        CAR_data[" name of customer"] = customer[1]
                        CAR_data["Date Of Birth Customer "] = customer[2]
                        CAR_data["Contact Number"] = customer[3]
                        CAR_data["Email"] = customer[4]
                    else:
                        CAR_data["CustomerID"] = None
                        CAR_data[" name of customer"] = None
                        CAR_data["Date Of Birth Customer "] = None
                        CAR_data["Contact Number"] = None
                        CAR_data["Email"] = None
                    if have_insurancepolicy:
                        CAR_data["Policy No"] = have_insurancepolicy[0]
                        CAR_data["Start Date"] = have_insurancepolicy[1]
                        CAR_data["End Date"] = have_insurancepolicy[2]
                        CAR_data["Coverage Type"] = have_insurancepolicy[3]
                        CAR_data["Premium Amount"] = have_insurancepolicy[4]
                        covered_persons = connection.cursor()
                        cursor.execute(
                            "SELECT * FROM coveredperson WHERE PolicyNo IN (SELECT PolicyNo FROM have_insurancepolicy WHERE PolicyNo = %s)",
                            (have_insurancepolicy[0],))
                        covered_persons = cursor.fetchall()
                        covered_persons_info = ""
                        for person in covered_persons:
                            covered_persons_info += f"\nPerson ID: {person[0]}, Name: {person[1]}\n"
                        CAR_data[f"  \n"] = covered_persons_info.strip()
                    else:
                        CAR_data["Policy No"] = None
                        CAR_data["Start Date"] = None
                        CAR_data["End Date"] = None
                        CAR_data["Coverage Type"] = None
                        CAR_data["Premium Amount"] = None
                    if pay_payment23:
                        CAR_data["Payment No"] = pay_payment23[0]
                        CAR_data["Amount"] = pay_payment23[1]
                        CAR_data["Payment Date"] = pay_payment23[2]
                        CAR_data["Payment Method"] = pay_payment23[3]
                    else:
                        CAR_data["Payment No"] = None
                        CAR_data["Amount"] = None
                        CAR_data["Payment Date"] = None
                        CAR_data["Payment Method"] = None
            else:
                    print(f"No car found with carID {car_ID}")
    except Error as e:
        print(f"Error: {e}")
    return CAR_data
def search_insurancepolicy(insurancepolicy_ID):
    insurancepolicy_data = {}
    try:
        with connect(
                host='localhost',
                database='projectdb',
                user='root',
                password='1201838'
        ) as connection:
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM have_insurancepolicy WHERE PolicyNo = %s"
                data = (insurancepolicy_ID,)
                cursor.execute(query, data)
                have_insurancepolicy = cursor.fetchone()
                if have_insurancepolicy:
                    insurancepolicy_data["Policy No"] = have_insurancepolicy[0]
                    insurancepolicy_data["Start Date"] = have_insurancepolicy[1]
                    insurancepolicy_data["End Date"] = have_insurancepolicy[2]
                    insurancepolicy_data["Coverage Type"] = have_insurancepolicy[3]
                    insurancepolicy_data["Premium Amount"] = have_insurancepolicy[4]
                    covered_persons = connection.cursor()
                    cursor.execute(
                        "SELECT * FROM coveredperson WHERE PolicyNo IN (SELECT PolicyNo FROM have_insurancepolicy WHERE PolicyNo = %s)",
                        (have_insurancepolicy[0],))
                    covered_persons = cursor.fetchall()
                    covered_persons_info = ""
                    for person in covered_persons:
                        covered_persons_info += f"\nPerson ID: {person[0]}, Name: {person[1]}\n"
                    insurancepolicy_data[f"  \n"] = covered_persons_info.strip()
                    insurancepolicy = connection.cursor()
                    query = "SELECT * FROM own_car WHERE CarID = %s"
                    datacar = (have_insurancepolicy[5],)
                    cursor.execute(query, datacar)
                    car = cursor.fetchone()
                    query = "SELECT * FROM customer WHERE CustomerID = %s"
                    customers = (car[4],)
                    insurancepolicy.execute(query, customers)
                    customers = insurancepolicy.fetchone()
                    if customers:
                        query = "SELECT * FROM pay_payment WHERE CarID = %s"
                        pay_payment23 = (have_insurancepolicy[5],)
                        insurancepolicy.execute(query, pay_payment23)
                        pay_payment23 = insurancepolicy.fetchone()
                        insurancepolicy_data["CustomerID"] = customers[0]
                        insurancepolicy_data[" name of customer"] = customers[1]
                        insurancepolicy_data["Date Of Birth Customer "] = customers[2]
                        insurancepolicy_data["Contact Number"] = customers[3]
                        insurancepolicy_data["Email"] = customers[4]
                        if car:
                            insurancepolicy_data["CarID"] = car[0]
                            insurancepolicy_data["Model"] = car[1]
                            insurancepolicy_data["Manu facture Year"] = car[2]
                            insurancepolicy_data["Registration Number"] = car[3]
                        else:
                            insurancepolicy_data["CarID"] = None
                            insurancepolicy_data["Model"] = None
                            insurancepolicy_data["Manu facture Year"] = None
                            insurancepolicy_data["Registration Number"] = None
                    else:
                        insurancepolicy_data["CustomerID"] = None
                        insurancepolicy_data[" name of customer"] = None
                        insurancepolicy_data["Date Of Birth Customer "] = None
                        insurancepolicy_data["Contact Number"] = None
                        insurancepolicy_data["Email"] = None
                    if pay_payment23:
                        insurancepolicy_data["Payment No"] = pay_payment23[0]
                        insurancepolicy_data["Amount"] = pay_payment23[1]
                        insurancepolicy_data["Payment Date"] = pay_payment23[2]
                        insurancepolicy_data["Payment Method"] = pay_payment23[3]
                    else:
                        insurancepolicy_data["Payment No"] = None
                        insurancepolicy_data["Amount"] = None
                        insurancepolicy_data["Payment Date"] = None
                        insurancepolicy_data["Payment Method"] = None
                else:
                    insurancepolicy_data = None  # No insurance policy found
            else:
                print(f"No insurancepolicy found with insurancepolicyID {insurancepolicy_ID}")
    except Error as e:
        print(f"Error: {e}")
    return insurancepolicy_data
def update_customer(Customer_ID):
    customer_data = {}
    try:
        with connect(
                host='localhost',
                database='projectdb',
                user='root',
                password='1201838'
        ) as connection:
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM customer WHERE CustomerID = %s"
                data = (Customer_ID,)
                cursor.execute(query, data)
                customer = cursor.fetchone()
                #
                if customer:
                    customer_data["Customer ID"] = customer[0]
                    customer_data["Name"] = customer[1]
                    customer_data["Date Of Birth"] = customer[2]
                    customer_data["Contact Number"] = customer[3]
                    customer_data["Email"] = customer[4]
                    cursor = connection.cursor()
                    query = "SELECT * FROM own_car WHERE CustomerID = %s"
                    datacar = (Customer_ID,)
                    cursor.execute(query, datacar)
                    car = cursor.fetchone()
                    if car:
                        insurancepolicy = connection.cursor()
                        query = "SELECT * FROM have_insurancepolicy WHERE CarID = %s"
                        datahave_insurancepolicy = (car[0],)
                        insurancepolicy.execute(query, datahave_insurancepolicy)
                        have_insurancepolicy = insurancepolicy.fetchone()
                        #
                        customer_data["CarID"] = car[0]
                        customer_data["Model"] = car[1]
                        customer_data["Manu facture Year"] = car[2]
                        customer_data["Registration Number"] = car[3]
                    else:
                        customer_data["CarID"] = None
                        customer_data["Model"] = None
                        customer_data["Manu facture Year"] = None
                        customer_data["Registration Number"] = None

                    if have_insurancepolicy:
                        pay_payment = connection.cursor()
                        query = "SELECT * FROM pay_payment WHERE CarID = %s"
                        pay_payment2 = (car[0],)
                        pay_payment.execute(query, pay_payment2)
                        pay_payment23 = pay_payment.fetchone()

                        customer_data["Policy No"] = have_insurancepolicy[0]
                        customer_data["Start Date"] = have_insurancepolicy[1]
                        customer_data["End Date"] = have_insurancepolicy[2]
                        customer_data["Coverage Type"] = have_insurancepolicy[3]
                        customer_data["Premium Amount"] = have_insurancepolicy[4]
                    else:

                        customer_data["Policy No"] = None
                        customer_data["Start Date"] = None
                        customer_data["End Date"] = None
                        customer_data["Coverage Type"] = None
                        customer_data["Premium Amount"] = None

                    if pay_payment23:
                        customer_data["Payment No"] = pay_payment23[0]
                        customer_data["Amount"] = pay_payment23[1]
                        customer_data["Payment Date"] = pay_payment23[2]
                        customer_data["Payment Method"] = pay_payment23[3]
                    else:
                        customer_data["Payment No"] = None
                        customer_data["Amount"] = None
                        customer_data["Payment Date"] = None
                        customer_data["Payment Method"] = None
            else:
                    print(f"No customer found with CustomerID {Customer_ID}")
    except Error as e:
        print(f"Error: {e}")
    return customer_data
def get_insurance_policy_info(CarID):
    insurance_data = {}
    try:
        with connect(
                host='localhost',
                database='projectdb',
                user='root',
                password='1201838'
        ) as connection:
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM own_car WHERE CarID = %s"
                data = (CarID,)
                cursor.execute(query, data)
                customer = cursor.fetchone()
                #
                if customer:
                        insurancepolicy = connection.cursor()
                        query = "SELECT * FROM have_insurancepolicy WHERE CarID = %s"
                        datahave_insurancepolicy = (CarID,)
                        insurancepolicy.execute(query, datahave_insurancepolicy)
                        have_insurancepolicy = insurancepolicy.fetchone()
                        if have_insurancepolicy:
                            insurance_data["StartDate"] = have_insurancepolicy[1]
                            insurance_data["EndDate"] = have_insurancepolicy[2]
                            insurance_data["CoverageType"] = have_insurancepolicy[3]
                            insurance_data["PremiumAmount"] = have_insurancepolicy[4]
                        else:
                            insurance_data["StartDate"] = None
                            insurance_data["EndDate"] = None
                            insurance_data["CoverageType"] = None
                            insurance_data["PremiumAmount"] = None
            else:
                    print(f"No car found with CarID {CarID}")
    except Error as e:
        print(f"Error: {e}")
    return insurance_data


def update_customer_coveredperson(carID):
    have_insurancepolicy = None
    try:
        with connect(
                host='localhost',
                database='projectdb',
                user='root',
                password='1201838'
        ) as connection:
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM own_car WHERE CarID = %s"
                data = (carID,)
                cursor.execute(query, data)
                CAR = cursor.fetchone()

                if CAR:
                    insurancepolicy = connection.cursor()
                    query = "SELECT * FROM have_insurancepolicy WHERE CarID = %s"
                    datahave_insurancepolicy = (carID,)
                    insurancepolicy.execute(query, datahave_insurancepolicy)
                    have_insurancepolicy = insurancepolicy.fetchone()
                    if have_insurancepolicy:
                        return have_insurancepolicy[0]
                else:
                    print(f"No CAR found with CARID {carID}")
            else:
                print("Connection not established.")
    except Error as e:
        print(f"Error: {e}")
    return have_insurancepolicy


def update_insurance_policy(insurance_data, db_connection,CARID):
    cursor = db_connection.cursor()
    try:
        cursor.execute("""
            UPDATE have_insurancepolicy
            SET StartDate = %s, EndDate = %s, CoverageType = %s, PremiumAmount = %s
            WHERE CarID = %s
        """, (
            insurance_data['StartDate'],
            insurance_data['EndDate'],
            insurance_data['CoverageType'],
            insurance_data['PremiumAmount'],
            CARID
        ))
        db_connection.commit()
        return True, "Insurance policy updated successfully"
    except mysql.connector.Error as e:
        db_connection.rollback()
        return False, str(e)
    finally:
        cursor.close()

def get_pay_payment_data_info(CarID):
    pay_payment_data = {}
    try:
        with connect(
                host='localhost',
                database='projectdb',
                user='root',
                password='1201838'
        ) as connection:
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM pay_payment WHERE CarID = %s"
                data = (CarID,)
                cursor.execute(query, data)
                pay_payment = cursor.fetchone()
                if pay_payment:
                    pay_payment_data["Amount"] = pay_payment[1]
                    pay_payment_data["PaymentDate"] = pay_payment[2]
                    pay_payment_data["PaymentMethod"] = pay_payment[3]  # Corrected field name
                else:
                    pay_payment_data["Amount"] = None
                    pay_payment_data["PaymentDate"] = None
                    pay_payment_data["PaymentMethod"] = None  # Corrected field name
            else:
                print(f"No CAR found with CARID {CarID}")
    except Error as e:
        print(f"Error: {e}")
    return pay_payment_data


def update_pay_payment_policy(pay_payment_data, db_connection,CARID):
    cursor = db_connection.cursor()
    try:
        cursor.execute("""
            UPDATE pay_payment
            SET Amount = %s, PaymentDate = %s, PaymentMethod = %s
            WHERE CarID = %s
        """, (
            pay_payment_data['Amount'],
            pay_payment_data['PaymentDate'],
            pay_payment_data['PaymentMethod'],
            CARID
        ))
        db_connection.commit()
        return True, "Pay payment updated successfully"
    except mysql.connector.Error as e:
        db_connection.rollback()
        return False, str(e)
    finally:
        cursor.close()


def get_own_car_data_info(customer_id):
    own_car_data = {}
    try:
        with connect(
                host='localhost',
                database='projectdb',
                user='root',
                password='1201838'
        ) as connection:
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM customer WHERE CustomerID = %s"
                data = (customer_id,)
                cursor.execute(query, data)
                customer = cursor.fetchone()
                if customer:
                        own_car2 = connection.cursor()
                        query = "SELECT * FROM own_car WHERE CustomerID = %s"
                        datahave_pay_payment = (customer_id,)
                        own_car2.execute(query, datahave_pay_payment)
                        own_car = own_car2.fetchone()
                        if own_car:
                            own_car_data["Model"] = own_car[1]
                            own_car_data["ManufactureYear"] = own_car[2]
                            own_car_data["RegistrationNumber"] = own_car[3]
                        else:
                            own_car_data["Model"] = None
                            own_car_data["ManufactureYear"] = None
                            own_car_data["RegistrationNumber"] = None
            else:
                    print(f"No customer found with CustomerID {customer_id}")
    except Error as e:
        print(f"Error: {e}")
    return own_car_data
def update_own_car_policy(own_car_data, db_connection, customer_id):
    cursor = db_connection.cursor()
    try:
        cursor.execute("""
            UPDATE own_car
            SET Model = %s, ManufactureYear = %s, RegistrationNumber = %s
            WHERE CustomerID = %s
        """, (
            own_car_data['Model'],
            own_car_data['ManufactureYear'],
            own_car_data['RegistrationNumber'],
            customer_id
        ))
        db_connection.commit()
        return True, "car updated successfully"
    except mysql.connector.Error as e:
        db_connection.rollback()
        return False, str(e)
    finally:
        cursor.close()
def get_customer_info(customer_id):
    customer_data = {}
    try:
        with connect(
                host='localhost',
                database='projectdb',
                user='root',
                password='1201838'
        ) as connection:
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM customer WHERE CustomerID = %s"
                data = (customer_id,)
                cursor.execute(query, data)
                customer = cursor.fetchone()
                if customer:
                            customer_data["Cname"] = customer[1]
                            customer_data["DateOfBirth"] = customer[2]
                            customer_data["ContactNumber"] = customer[3]
                            customer_data["Email"] = customer[4]

            else:
                    print(f"No customer found with CustomerID {customer_id}")
    except Error as e:
        print(f"Error: {e}")
    return customer_data
def update_customer_info(customer_data, db_connection,customer_id):
    cursor = db_connection.cursor()
    try:
        cursor.execute("""
            UPDATE customer
            SET Cname = %s,  DateOfBirth = STR_TO_DATE(%s, '%Y-%m-%d'), ContactNumber = %s , Email = %s
            WHERE CustomerID = %s 
        """, (
            customer_data['Cname'],
            customer_data['DateOfBirth'],
            customer_data['ContactNumber'],
            customer_data['Email'],
            customer_id
        ))
        db_connection.commit()
        return True, "customer updated successfully"
    except mysql.connector.Error as e:
        db_connection.rollback()
        return False, str(e)
    finally:
        cursor.close()


def fetch_policies_expiring_soon(db_connection):
    """Fetch insurance policies expiring in the next 30 days."""
    cursor = db_connection.cursor()
    try:
        cursor.execute("""
            SELECT * FROM have_insurancepolicy
            WHERE EndDate BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
        """)
        return cursor.fetchall()  # Returns a list of tuples representing the policy rows
    except mysql.connector.Error as e:
        print("Error fetching policies expiring soon:", str(e))
        return []
    finally:
        cursor.close()
def fetch_policies_expiring_in_3_days(db_connection, today_date, end_date_range):
    cursor = db_connection.cursor()
    try:
        cursor.execute("""
                 SELECT CU.Cname, CU.ContactNumber
                FROM have_insurancepolicy AS H, own_car AS C, customer AS CU
                WHERE H.CarID = C.CarID AND C.CustomerID = CU.CustomerID AND H.EndDate BETWEEN %s AND %s
        """, (today_date, end_date_range))
        print("Today's date:", today_date)
        print("End date range:", end_date_range)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        print("Error fetching policies expiring in 3 days:", str(e))
        return []
    finally:
        cursor.close()

def fetch_birth_customer(db_connection, today_date):
    cursor = db_connection.cursor()
    try:
        cursor.execute("""
                    SELECT C.Cname, C.ContactNumber
                    FROM customer AS C
                    WHERE DATE_FORMAT(C.DateOfBirth, '%m-%d') = DATE_FORMAT(%s, '%m-%d')
                """, (today_date,))
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        print("Error fetching:", str(e))
        return []
    finally:
        cursor.close()
def fetch_payment_methods(db_connection):
    cursor = db_connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT PaymentMethod, COUNT(*) AS PaymentCount
            FROM pay_payment
            GROUP BY PaymentMethod
            ORDER BY PaymentCount DESC
            LIMIT 1;
        """)
        results = cursor.fetchall()
        if results:
            # Format the output to be more readable and informative
            most_used_payment_method = results[0]['PaymentMethod']
            count = results[0]['PaymentCount']
            return f"The most frequently used payment method is '{most_used_payment_method}' with {count} uses."
        else:
            return "No payment methods found."
    except mysql.connector.Error as e:
        print("Error fetching:", str(e))
        return "An error occurred while fetching payment methods."
    finally:
        cursor.close()

def get_customer_cars(customer_id):
    car_ids = []
    try:
        with connect(
                host='localhost',
                database='projectdb',
                user='root',
                password='1201838'
        ) as connection:
            if connection.is_connected():
                cursor = connection.cursor()
                query_own_car = "SELECT CarID FROM own_car WHERE CustomerID = %s"
                cursor.execute(query_own_car, (customer_id,))
                car_ids = [row[0] for row in cursor.fetchall()]
            else:
                print(f"No customer found with CustomerID {customer_id}")
    except Error as e:
        print(f"Error: {e}")
    return car_ids
def delete_coveredperson_id(db_connection, CoveredPersonID):
    cursor = db_connection.cursor()
    try:
        cursor.execute("SELECT * FROM coveredperson WHERE CoveredPersonID = %s", (CoveredPersonID,))
        if cursor.fetchone() is None:
            return False, "CoveredPersonID  does not exist."
        cursor.execute("DELETE FROM coveredperson WHERE CoveredPersonID = %s", (CoveredPersonID,))
        db_connection.commit()
        return True, "CoveredPersonID and associated records deleted successfully."
    except mysql.connector.Error as e:
        db_connection.rollback()
        return False, str(e)
    finally:
        cursor.close()
def search_customer(Customer_ID):
    customer_data = {}
    try:
        with connect(
                host='localhost',
                database='projectdb',
                user='root',
                password='1201838'
        ) as connection:
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM customer WHERE CustomerID = %s"
                data = (Customer_ID,)
                cursor.execute(query, data)
                customer = cursor.fetchone()
                #
                if customer:
                    customer_data["Customer ID"] = customer[0]
                    customer_data["Name"] = customer[1]
                    customer_data["Date Of Birth"] = customer[2]
                    customer_data["Contact Number"] = customer[3]
                    customer_data["Email"] = customer[4]
                    cursor = connection.cursor()
            else:
                    print(f"No customer found with CustomerID {Customer_ID}")
    except Error as e:
        print(f"Error: {e}")
    return customer_data

#The function only executes if there is a customer who has made it because the customer has more than one car and is insured with more than one policy.
def search_CAR77(car_ID):
    CAR_data = {}
    try:
        with connect(
                host='localhost',
                database='projectdb',
                user='root',
                password='1201838'
        ) as connection:
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM own_car WHERE CarID = %s"
                data = (car_ID,)
                cursor.execute(query, data)
                car = cursor.fetchone()
                if car:
                    CAR_data["CarID"] = car[0]
                    CAR_data["Model"] = car[1]
                    CAR_data["Manu facture Year"] = car[2]
                    CAR_data["Registration Number"] = car[3]
                    cursor.execute("SELECT * FROM have_insurancepolicy WHERE CarID = %s", (car_ID,))
                    ins_info = cursor.fetchone()
                    if ins_info:
                        CAR_data["PolicyNo"] = ins_info[0]
                        CAR_data["StartDate"] = ins_info[1]
                        CAR_data["EndDate"] = ins_info[2]
                        CAR_data["CoverageType"] = ins_info[3]
                        CAR_data["PremiumAmount"] = ins_info[4]
                    else:
                        CAR_data["PolicyNo"] = None
                        CAR_data["StartDate"] = None
                        CAR_data["EndDate"] = None
                        CAR_data["CoverageType"] = None
                        CAR_data["PremiumAmount"] = None
                    cursor.execute(
                        "SELECT * FROM coveredperson WHERE PolicyNo IN (SELECT PolicyNo FROM have_insurancepolicy WHERE CarID = %s)",
                        (car_ID,))
                    covered_persons = cursor.fetchall()
                    covered_persons_info = ""
                    for person in covered_persons:
                        covered_persons_info += f"\nCovered Person ID: {person[0]}, Name: {person[1]}\n"
                    CAR_data[f" \n"] = covered_persons_info.strip()
                    cursor.execute("SELECT * FROM pay_payment WHERE CarID = %s", (car_ID,))
                    payment_info = cursor.fetchone()
                    if payment_info:
                        CAR_data["Payment No"] = payment_info[0]
                        CAR_data["Amount"] = payment_info[1]
                        CAR_data["Payment Date"] = payment_info[2]
                        CAR_data["Payment Method"] = payment_info[3]
                    else:
                        CAR_data["Payment No"] = None
                        CAR_data["Amount"] = None
                        CAR_data["Payment Date"] = None
                        CAR_data["Payment Method"] = None
                else:
                    print(f"No car found with carID {car_ID}")
            else:
                print("Database connection is not established.")
    except Error as e:
        print(f"Error: {e}")
    return CAR_data


