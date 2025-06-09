#Passenger Module
"""
>PAX_ID
>name
>age
______________

-login()
-searchtrain()
-modifyform()
-paycharges()
-bookTicket()
-cancelTicket()

"""

import subprocess
import mysql.connector as m


# Import database at start
with open('custom_database.sql', 'r') as f:
    subprocess.run(['mysql', '-u', 'root', '-proot', 'trainreservation'], stdin=f)

connector= m.connection(host="localhost", user="root", password="root", database="trainreservation")
con_cursor = connector.cursor()
#user handling

def register():
    from random import randint as rint
    connector= m.connection(host="localhost",user="root",password="root",database="trainreservation") 
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
    
def login():
    connector= m.connection(host="localhost",user="root",password="root",database="trainreservation")
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
        wrong_pwd = 1
        
        return None
    if wrong_pwd == 1:
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
    
    
# Export database at end
with open('custom_database.sql', 'w') as f:
    subprocess.run(['mysqldump', '-u', 'root', '-proot', 'trainreservation'], stdout=f)