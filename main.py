"""Passenger Module

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
import os

# Import database at start
os.system('mysql -u root -proot trainreservation < custom_database.sql')

import mysql.connector as m

con = m.connection(host="localhost",user="root",password="root",database="trainreservation")
con_cursor = con.cursor()
#user handling

def register():
    from random import randint as rint
    con = m.connection(host="localhost",user="root",password="root",database="trainreservation") 
    con_cursor =con.cursor()
    sys_ID = rint(0, 1000)*10
    
    print("\n to register as a new user enter your details below")
    user_id = input("Enter user name (user id ) for the reservation. == ")
    print("\n\n")
    ph_no = int(input("enter your phone nummber to be used for reservation. == "))
    print("\n\n")
    pwd = input("enter password to be used for your ID. == ")
    con_cursor.execute("insert into user_details values(%s,%s,%s,%s)",(sys_ID,user_id,ph_no,pwd))
    print(f"User ID {user_id} registered successfully with system ID {sys_ID}.")
    
    con.commit()
    
def login():
    con = m.connection(host="localhost",user="root",password="root",database="trainreservation")
    con_cursor = con.cursor()
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
        
        return None
    
    
    print("if you are a new user please register first")
    
    

# Export database at end
os.system('mysqldump -u root -proot trainreservation > custom_database.sql')