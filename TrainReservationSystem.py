import mysql.connector as m
import random
from getpass import getpass  # For secure password input

# Database connection setup
def get_db_connection():
    """Establish and return a database connection"""
    try:
        return m.connect(
            host="localhost",
            user="root",
            password="root",
            database="trainreservation"
        )
    except m.Error as err:
        print(f"Database connection error: {err}")
        exit()

connector = get_db_connection()
current_user = None

# Weekdays dictionary
week_days = {
    "m": "Monday", 
    "t": "Tuesday", 
    "w": "Wednesday", 
    "th": "Thursday", 
    "f": "Friday", 
    "s": "Saturday", 
    "su": "Sunday"
}

def register():
    """Register a new user"""
    try:
        con_cursor = connector.cursor()
        sys_id = random.randint(0, 1000) * 10
        
        print("\n=== Register New User ===")
        user_id = input("Enter username: ")
        
        # Validate phone number
        while True:
            try:
                ph_no = int(input("Enter your phone number: "))
                if len(str(ph_no)) != 10:
                    print("Phone number must be 10 digits")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter numbers only.")
        
        # Password confirmation
        while True:
            pwd = getpass("Enter password: ")
            confirm_pwd = getpass("Confirm password: ")
            if pwd == confirm_pwd:
                break
            print("Passwords don't match. Try again.")
        
        # Check if username exists
        con_cursor.execute("SELECT * FROM user_details WHERE user_id = %s", (user_id,))
        if con_cursor.fetchone():
            print("Username already exists. Please choose another.")
            return
        
        con_cursor.execute(
            "INSERT INTO user_details VALUES (%s, %s, %s, %s)",
            (sys_id, user_id, ph_no, pwd)
        )
        connector.commit()
        
        print(f"\nUser {user_id} registered successfully with System ID: {sys_id}")
        return user_id
        
    except m.Error as err:
        print(f"Database error during registration: {err}")
        return None

def login():
    """Authenticate user login"""
    global current_user
    try:
        con_cursor = connector.cursor()
        
        print("\n=== Login ===")
        user_id = input("Enter your user ID: ")
        pwd = getpass("Enter your password: ")
        
        con_cursor.execute(
            "SELECT * FROM user_details WHERE user_id = %s AND password = %s",
            (user_id, pwd)
        )
        
        if con_cursor.fetchone():
            print(f"\nWelcome {user_id}!")
            current_user = user_id
            return user_id
        else:
            print("\nInvalid credentials.")
            return None
            
    except m.Error as err:
        print(f"Database error during login: {err}")
        return None

def search_train():
    """Search for available trains"""
    try:
        con_cursor = connector.cursor()
        
        print("\n=== Search Trains ===")
        start_station = input("Enter starting station: ").strip()
        dest_station = input("Enter destination station: ").strip()
        
        print("\nAvailable days:", ", ".join(week_days.values()))
        travel_day = input("Enter day of travel: ").lower()
        
        # Convert day abbreviation to full name if needed
        day_name = week_days.get(travel_day, travel_day)
        
        con_cursor.execute(
            """SELECT train_no, train_name, start_station, dest_station, 
               departure_time, arrival_time, ac1_fare, sl_fare, gen_fare 
               FROM train_details 
               WHERE start_station = %s AND dest_station = %s AND running_days LIKE %s""",
            (start_station, dest_station, f"%{day_name}%")
        )
        
        trains = con_cursor.fetchall()
        
        if not trains:
            print("\nNo trains available for this route.")
            return
        
        print("\n=== Available Trains ===")
        print("Train No | Train Name         | From      | To        | Departure | Arrival  | AC Fare | SL Fare | GEN Fare")
        print("-" * 90)
        for train in trains:
            print(f"{train[0]:8} | {train[1]:18} | {train[2]:9} | {train[3]:9} | {train[4]:9} | {train[5]:8} | {train[6]:7} | {train[7]:7} | {train[8]:8}")
        
        return trains
        
    except m.Error as err:
        print(f"Database error during train search: {err}")
        return None

def book_ticket():
    """Book train tickets"""
    global current_user
    if not current_user:
        print("Please login first.")
        return
    
    try:
        con_cursor = connector.cursor()
        
        # First show available trains
        available_trains = search_train()
        if not available_trains:
            return
        
        # Get train number from user
        while True:
            try:
                train_no = int(input("\nEnter train number to book: "))
                # Verify train exists
                selected_train = None
                for train in available_trains:
                    if train[0] == train_no:
                        selected_train = train
                        break
                
                if selected_train:
                    break
                else:
                    print("Invalid train number. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Get ticket class
        print("\nTicket Classes:")
        print("1. AC (Rs. {})".format(selected_train[6]))
        print("2. SL (Rs. {})".format(selected_train[7]))
        print("3. GEN (Rs. {})".format(selected_train[8]))
        
        while True:
            try:
                class_choice = int(input("Enter class choice (1-3): "))
                if 1 <= class_choice <= 3:
                    break
                print("Please enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Get number of tickets
        while True:
            try:
                num_tickets = int(input("Enter number of tickets: "))
                if num_tickets > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Get passenger details
        passengers = []
        for i in range(num_tickets):
            print(f"\nPassenger {i+1} details:")
            name = input("Full name: ")
            
            while True:
                try:
                    age = int(input("Age: "))
                    if age > 0:
                        break
                    print("Please enter a valid age.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            gender = input("Gender (M/F/O): ").upper()
            while gender not in ['M', 'F', 'O']:
                print("Please enter M, F, or O.")
                gender = input("Gender (M/F/O): ").upper()
            
            passengers.append({
                'name': name,
                'age': age,
                'gender': gender
            })
        
        # Calculate fare
        fare_types = [selected_train[6], selected_train[7], selected_train[8]]
        fare = fare_types[class_choice-1] * num_tickets
        
        # Confirm booking
        print(f"\nTotal fare: Rs. {fare}")
        confirm = input("Confirm booking? (yes/no): ").lower()
        if confirm != 'yes':
            print("Booking cancelled.")
            return
        
        # Generate PNR and book tickets
        pnr = random.randint(100000, 999999)
        class_names = ['AC', 'SL', 'GEN']
        
        for passenger in passengers:
            con_cursor.execute(
                """INSERT INTO booked_tickets 
                (user_id, PNR, train_no, passenger_name, age, gender, fare, class, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Confirmed')""",
                (current_user, pnr, train_no, passenger['name'], 
                 passenger['age'], passenger['gender'], 
                 fare_types[class_choice-1], class_names[class_choice-1])
            )
        
        connector.commit()
        print(f"\nBooking successful! Your PNR number is: {pnr}")
        print(f"Total amount paid: Rs. {fare}")
        
    except m.Error as err:
        print(f"Database error during booking: {err}")
        connector.rollback()

def cancel_ticket():
    """Cancel a booked ticket"""
    global current_user
    if not current_user:
        print("Please login first.")
        return
    
    try:
        con_cursor = connector.cursor()
        
        print("\n=== Cancel Ticket ===")
        pnr = input("Enter PNR number to cancel: ")
        
        # Verify ticket exists and belongs to user
        con_cursor.execute(
            """SELECT * FROM booked_tickets 
            WHERE PNR = %s AND user_id = %s""",
            (pnr, current_user)
        )
        tickets = con_cursor.fetchall()
        
        if not tickets:
            print("No tickets found with this PNR number.")
            return
        
        # Display ticket details
        print("\nTicket Details:")
        print(f"PNR: {tickets[0][1]}")
        print(f"Train No: {tickets[0][2]}")
        print(f"Passengers: {len(tickets)}")
        print(f"Total Fare: Rs. {sum(ticket[6] for ticket in tickets)}")
        
        confirm = input("\nAre you sure you want to cancel? (yes/no): ").lower()
        if confirm != 'yes':
            print("Cancellation aborted.")
            return
        
        # Process cancellation
        con_cursor.execute(
            "DELETE FROM booked_tickets WHERE PNR = %s",
            (pnr,)
        )
        connector.commit()
        
        print("\nCancellation successful. Refund will be processed shortly.")
        
    except m.Error as err:
        print(f"Database error during cancellation: {err}")
        connector.rollback()

def view_bookings():
    """View all bookings for current user"""
    global current_user
    if not current_user:
        print("Please login first.")
        return
    
    try:
        con_cursor = connector.cursor()
        
        print("\n=== Your Bookings ===")
        con_cursor.execute(
            """SELECT PNR, train_no, passenger_name, age, gender, class, fare, status 
            FROM booked_tickets 
            WHERE user_id = %s 
            ORDER BY PNR""",
            (current_user,)
        )
        bookings = con_cursor.fetchall()
        
        if not bookings:
            print("You have no bookings yet.")
            return
        
        current_pnr = None
        total_amount = 0
        
        for booking in bookings:
            if booking[0] != current_pnr:
                if current_pnr is not None:
                    print(f"Total for PNR {current_pnr}: Rs. {total_amount}")
                    print("-" * 60)
                    total_amount = 0
                
                current_pnr = booking[0]
                print(f"\nPNR: {current_pnr} | Train No: {booking[1]}")
                print("Passenger Name   | Age | Gender | Class   | Fare    | Status")
                print("-" * 60)
            
            print(f"{booking[2]:16} | {booking[3]:3} | {booking[4]:6} | {booking[5]:7} | {booking[6]:7} | {booking[7]}")
            total_amount += booking[6]
        
        print(f"\nTotal for PNR {current_pnr}: Rs. {total_amount}")
        
    except m.Error as err:
        print(f"Database error while fetching bookings: {err}")

def user_menu():
    """Main menu for logged in users"""
    global current_user
    while True:
        print("\n=== User Menu ===")
        print("1. Search Trains")
        print("2. Book Ticket")
        print("3. View Bookings")
        print("4. Cancel Ticket")
        print("5. Logout")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            search_train()
        elif choice == '2':
            book_ticket()
        elif choice == '3':
            view_bookings()
        elif choice == '4':
            cancel_ticket()
        elif choice == '5':
            print(f"Logging out {current_user}...")
            current_user = None
            break
        else:
            print("Invalid choice. Please try again.")

def main_menu():
    """Main program menu"""
    while True:
        print("\n=== Train Reservation System ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            if login():
                user_menu()
        elif choice == '2':
            register()
        elif choice == '3':
            print("Thank you for using our system. Goodbye!")
            connector.close()
            exit()
        else:
            print("Invalid choice. Please try again.")

# Start the program
if __name__ == "__main__":
    main_menu()