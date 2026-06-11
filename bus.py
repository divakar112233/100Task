import sqlite3
from datetime import datetime, timedelta

# Connect to database
conn = sqlite3.connect('bus.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS buses (
    id INTEGER PRIMARY KEY,
    bus_number TEXT NOT NULL,
    route_from TEXT NOT NULL,
    route_to TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    total_seats INTEGER NOT NULL,
    price_per_seat REAL NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS passengers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    phone TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    bus_id INTEGER,
    passenger_id INTEGER,
    seat_number INTEGER,
    booking_date TEXT,
    FOREIGN KEY(bus_id) REFERENCES buses(id),
    FOREIGN KEY(passenger_id) REFERENCES passengers(id)
)''')

conn.commit()

def add_bus():
    print("\n--- Add New Bus ---")
    bus_num = input("Bus Number: ")
    from_loc = input("From: ")
    to_loc = input("To: ")
    dep_time = input("Departure Time (HH:MM): ")
    arr_time = input("Arrival Time (HH:MM): ")
    seats = int(input("Total Seats: "))
    price = float(input("Price per Seat: "))
    
    cursor.execute("""INSERT INTO buses 
        (bus_number, route_from, route_to, departure_time, arrival_time, total_seats, price_per_seat)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", 
        (bus_num, from_loc, to_loc, dep_time, arr_time, seats, price))
    conn.commit()
    print("✅ Bus added successfully!")

def view_buses():
    print("\n--- Available Buses ---")
    cursor.execute("SELECT * FROM buses")
    buses = cursor.fetchall()
    if not buses:
        print("No buses available.")
        return
    for bus in buses:
        booked = get_booked_seats(bus[0])
        available = bus[6] - booked
        print(f"ID:{bus[0]} | {bus[1]} | {bus[2]} → {bus[3]} | Dep:{bus[4]} Arr:{bus[5]} | Seats: {available}/{bus[6]} | ₹{bus[7]}")

def get_booked_seats(bus_id):
    cursor.execute("SELECT COUNT(*) FROM bookings WHERE bus_id=?", (bus_id,))
    result = cursor.fetchone()
    return result[0] if result else 0

def add_passenger():
    print("\n--- Add Passenger ---")
    name = input("Name: ")
    age = int(input("Age: "))
    gender = input("Gender (M/F/O): ")
    phone = input("Phone: ")
    
    cursor.execute("INSERT INTO passengers (name, age, gender, phone) VALUES (?, ?, ?, ?)",
                   (name, age, gender, phone))
    conn.commit()
    print("✅ Passenger added! ID:", cursor.lastrowid)

def view_passengers():
    print("\n--- Passengers ---")
    cursor.execute("SELECT * FROM passengers")
    for p in cursor.fetchall():
        print(f"ID:{p[0]} | {p[1]} | Age:{p[2]} | {p[3]} | {p[4]}")

def book_ticket():
    print("\n--- Book Ticket ---")
    view_buses()
    bus_id = int(input("\nEnter Bus ID: "))
    
    # Check bus exists and seats available
    cursor.execute("SELECT total_seats FROM buses WHERE id=?", (bus_id,))
    result = cursor.fetchone()
    if not result:
        print("❌ Invalid Bus ID!")
        return
    
    total_seats = result[0]
    booked = get_booked_seats(bus_id)
    if booked >= total_seats:
        print("❌ No seats available!")
        return
    
    view_passengers()
    passenger_id = int(input("\nEnter Passenger ID: "))
    
    # Get next available seat
    cursor.execute("SELECT seat_number FROM bookings WHERE bus_id=? ORDER BY seat_number", (bus_id,))
    taken = [row[0] for row in cursor.fetchall()]
    seat_num = 1
    while seat_num in taken:
        seat_num += 1
    
    booking_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    cursor.execute("INSERT INTO bookings (bus_id, passenger_id, seat_number, booking_date) VALUES (?, ?, ?, ?)",
                   (bus_id, passenger_id, seat_num, booking_date))
    conn.commit()
    
    # Get price
    cursor.execute("SELECT price_per_seat FROM buses WHERE id=?", (bus_id,))
    price = cursor.fetchone()[0]
    
    print(f"✅ Ticket Booked Successfully!")
    print(f"Seat Number: {seat_num} | Total Amount: ₹{price}")

def view_bookings():
    print("\n--- All Bookings ---")
    cursor.execute("""SELECT b.id, bus.bus_number, bus.route_from, bus.route_to, 
                             p.name, b.seat_number, b.booking_date, bus.price_per_seat
                      FROM bookings b
                      JOIN buses bus ON b.bus_id = bus.id
                      JOIN passengers p ON b.passenger_id = p.id""")
    bookings = cursor.fetchall()
    if not bookings:
        print("No bookings yet.")
        return
    for bk in bookings:
        print(f"Ticket ID:{bk[0]} | Bus:{bk[1]} | {bk[2]}→{bk[3]} | Passenger:{bk[4]} | Seat:{bk[5]} | Date:{bk[6]} | ₹{bk[7]}")

def main():
    while True:
        print("\n" + "="*40)
        print("   🚌 BUS TICKET BOOKING SYSTEM")
        print("="*40)
        print("1. Add Bus")
        print("2. View Buses")
        print("3. Add Passenger")
        print("4. View Passengers")
        print("5. Book Ticket")
        print("6. View Bookings")
        print("7. Exit")
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            add_bus()
        elif choice == '2':
            view_buses()
        elif choice == '3':
            add_passenger()
        elif choice == '4':
            view_passengers()
        elif choice == '5':
            book_ticket()
        elif choice == '6':
            view_bookings()
        elif choice == '7':
            print("Thank you for using Bus Ticket Booking System! 👋")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    print("Welcome to Bus Ticket Booking System!")
    main()
    conn.close()