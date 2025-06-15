#Passenger Module
"""
>PAX_ID
>name
>age
______________
essential
-login()
-searchtrain()
-bookTicket()
-cancelTicket()


low importance
-modifyform()
-paycharges()
"""


import mysql.connector as m

connector= m.connect(host="localhost", user="root", password="root", database="trainreservation")
con_cursor = connector.cursor()
#user handling

def register():
    from random import randint as rint
    connector= m.connect(host="localhost",user="root",password="root",database="trainreservation") 
    con_cursor =connector.cursor()
    sys_ID = rint(0, 1000)*10
    
    print("\n to register as a new user enter your details below")
    user_id = input("Enter user name (user id ) for the reservation. == ")
    print("\n\n")
    
    ph_no = int(input("enter your phone nummber to be used for reservation. == "))
    print("\n\n")
    
    pwd = input("enter password to be used for your ID. == ")
    con_cursor.execute("insert into user_details values(%s,%s,%s,%s)",(sys_ID,user_id,ph_no,pwd))
    
    print(f"User ID {user_id} registered successfully with system ID {sys_ID}.")
    
    connector.commit()


#Login function to authenticate user  
def login():
    connector= m.connect(host="localhost",user="root",password="root",database="trainreservation")
    con_cursor = connector.cursor()
    
    print("\n\n")
    print("Enter your user ID and password to login")
    print(".\n.\n.\n.\n")
    
    user_id = input("Enter your user ID: ")
    pwd = input("Enter your password: ")
    con_cursor.execute("select * from user_details where user_id = %s and password = %s", (user_id, pwd))   
    
    if con_cursor.fetchone():
        print(f"Welcome {user_id} to the Train Reservation System!")
        
        return user_id
    
    elif con_cursor.fetchone() is None:
        print("Invalid user ID or password. Please try again.")
        print("If you are a new user, please register first.")
        print("if you have forgotten your pwd or user ID please forget password or user ID option")
        print("\n\n")
    
        
        return None
    #if login is unsuccessful, try again
    if con_cursor.fetchone() is None:

        print("1. Register as a new user")
        print("2. Login with existing user ID")
        print("3. forgot password or user ID")
        choice = input("Enter your choice: ")
        
        if choice == '1':   
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            find = int(input("Enter your phone number or system ID to retrive the user ID and password:  "))
            con_cursor.execute("select * from user_details where phone_no = %s or sys_id = %s", (find, find))
            result = con_cursor.fetchone()
            if result:
                print(f"Your user ID is {result[1]} and your password is {result[3]}.")
            else:
                print("No user found with the given phone number or system ID.")
                print("Please try again or register as a new user.")
                ask = input("Do you want to register as a new user? (yes/no): ")
                if ask.lower() == 'yes':
                    register()
                else:
                    print("Thank you for using the Train Reservation System. Goodbye!")



 
def searchtrain():
    connector= m.connect(host="localhost",user="root",password="root",database="trainreservation")
    con_cursor = connector.cursor()
    
    #dict contianing weekdays
    week_days = {"m": "monday", "t": "tuesday", "w": "wednesday", "th":"thrushday", "f" : "friday", "s": "saturday", "su":"Sunday"}
    # Function to search for trains based on user input
    print("Search for trains")
    print("enter starting station")
    start_station = input("Enter starting station: ")
    print("enter destination station")
    dest_station = input("Enter destination station: ") 
    print("enter day of travel")
    
    travel_day = input(f"Enter day of travel \n{week_days}\n: ")  
    con_cursor.execute("SELECT * FROM train_details WHERE start_station = %s AND dest_station = %s AND travel_date = %s", (start_station, dest_station, travel_day))
    trains = con_cursor.fetchall()
    print("_____Available trains_____")
    print(trains)  

def Book_Ticket(uid):
    import random
    PNR = random.randint(100000, 999999)  # Generate a random PNR number
    connector = m.connect(host="localhost", user="root", password="root", database="trainreservation")
    con_cursor = connector.cursor()

    print("\n================= Train Reservation System =================\n")
    print("Available Trains:")
    print("-----------------------------------------------------------")
    # Instead of calling searchtrain (which does its own DB calls and fetchall),
    # directly query and display available trains for efficiency
    con_cursor.execute("SELECT train_no, train_name, start_station, dest_station, running_days, status FROM train_details")
    trains = con_cursor.fetchall()
    print("Train No | Name               | From     | To       | Days                  | Status")
    print("-------------------------------------------------------------------------------------")
    for t in trains:
        print(f"{t[0]:7} | {t[1]:18} | {t[2]:8} | {t[3]:8} | {t[4]:22} | {t[5]}")
    print("-------------------------------------------------------------------------------------\n")

    train_no = int(input("Enter your Train no: "))
    tcktno = int(input("Enter number of seats you want to book: "))
    print("\nTicket Classes:")
    print("1. AC TICKET   | 2. SL TICKET   | 3. GEN TICKET")
    
    typ = int(input("Enter your choice of class (1/2/3): "))
    fare_query = {1: 'ac1_fare', 2: 'sl_fare', 3: 'gen_fare'}
    fare_type = fare_query.get(typ, 'gen_fare')
    con_cursor.execute(f"SELECT {fare_type} FROM train_details WHERE train_no = %s", (train_no,))
    fare_result = con_cursor.fetchone()
    
    if not fare_result:
        print("Invalid train number or class selected.")
        return
    p = fare_result[0]
    class_names = {1: 'AC', 2: 'SL', 3: 'GEN'}
    print(f"\nSelected Class: {class_names.get(typ, 'GEN')} | Fare per ticket: Rs. {p}")
    for i in range(tcktno):
        print(f"\n--- Ticket {i+1} Details ---")
        customer = input("Enter customer name: ")
        age = int(input("Enter your age: "))
        print("For gender: M = Male, F = Female, O = Other")
        gender = input("Enter your gender: ")
        print(f"Your PNR no is: {PNR}")
        cnf = "Confirmed"
        con_cursor.execute(
            "INSERT INTO booked_tickets VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (uid, PNR, train_no, customer, age, gender, p, cnf)
        )
    amt = tcktno * p
    print("\n===========================================================")
    print(f"Your total ticket price is: Rs. {amt}")
    print("===========================================================\n")
    connector.commit()

#User panel
def user_panel():
    print("_________ Welcome to the Train Reservation System _________")
        
    print("1. Login to your account")
    print("2. Register as a new user")
    print("3. Exit")
    op = int(input("Enter your choice: "))
    if op == 1:
        login()
    elif op == 2:
        register()
    elif op == 3:
        print("Thank you for using the Train Reservation System. Goodbye!")
        exit()
    else:
        print("Invalid choice. Please try again.")
        user_panel()
def cancel_ticket():
    connector= m.connect(host="localhost", user="root", password="root", database="trainreservation")
    con_cursor = connector.cursor()
    cancel_PNR = int(input("Enter the PNR number of the ticket you want to cancel: "))
    con_cursor.execute("SELECT * FROM booked_tickets WHERE PNR = %s", (cancel_PNR,))
    con_cursor.Commit()
    
    
 
def user_panel():
    print("\n--- User Panel ---")
    login()
    
    if login != 0:
        return 0
    
    
    
def admin_panel():
    print("\n--- Admin Panel ---")
    print("Admin Panel is not implemented yet.")
    # You can add admin functionality here in the future

def start_menu():
    print("Welcome! Please choose your panel:")
    print("1. User Panel")
    print("2. Admin Panel")
    choice = input("Enter 1 or 2: ")
    if choice == '1':
        user_panel()
    elif choice == '2':
        admin_panel()
    else:
        print("Invalid choice. Please restart the program.")

start_menu()