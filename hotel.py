import sqlite3
from datetime import datetime, timedelta

# Connect to database
conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY,
    room_number TEXT UNIQUE NOT NULL,
    room_type TEXT NOT NULL,
    price_per_night REAL NOT NULL,
    status TEXT DEFAULT 'available'
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS guests (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    guest_id INTEGER,
    room_id INTEGER,
    check_in DATE,
    check_out DATE,
    total_amount REAL,
    status TEXT DEFAULT 'confirmed',
    FOREIGN KEY (guest_id) REFERENCES guests(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id)
)''')

conn.commit()

def add_room():
    room_number = input("Room Number: ")
    room_type = input("Room Type (Single/Double/Suite): ")
    price = float(input("Price per Night: "))
    cursor.execute("INSERT INTO rooms (room_number, room_type, price_per_night) VALUES (?, ?, ?)",
                   (room_number, room_type, price))
    conn.commit()
    print("✅ Room added!")

def view_rooms():
    cursor.execute("SELECT * FROM rooms")
    print("\n=== Available Rooms ===")
    for r in cursor.fetchall():
        print(f"ID:{r[0]} | Room:{r[1]} | Type:{r[2]} | Price:${r[3]:.2f} | Status:{r[4]}")

def add_guest():
    name = input("Guest Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    cursor.execute("INSERT INTO guests (name, phone, email) VALUES (?, ?, ?)",
                   (name, phone, email))
    conn.commit()
    print("✅ Guest added!")

def view_guests():
    cursor.execute("SELECT * FROM guests")
    for g in cursor.fetchall():
        print(f"ID:{g[0]} | {g[1]} | {g[2]} | {g[3]}")

def book_room():
    view_rooms()
    room_id = int(input("\nEnter Room ID to book: "))
    guest_id = int(input("Enter Guest ID: "))
    check_in = input("Check-in (YYYY-MM-DD): ")
    nights = int(input("Number of nights: "))
    check_out = (datetime.strptime(check_in, "%Y-%m-%d") + timedelta(days=nights)).strftime("%Y-%m-%d")
    
    # Get price
    cursor.execute("SELECT price_per_night FROM rooms WHERE id=?", (room_id,))
    price = cursor.fetchone()
    if not price:
        print("❌ Room not found!")
        return
    total = price[0] * nights
    
    cursor.execute("""INSERT INTO bookings 
        (guest_id, room_id, check_in, check_out, total_amount) 
        VALUES (?, ?, ?, ?, ?)""", 
        (guest_id, room_id, check_in, check_out, total))
    
    # Update room status
    cursor.execute("UPDATE rooms SET status='booked' WHERE id=?", (room_id,))
    conn.commit()
    print(f"✅ Booking successful! Total: ${total:.2f}")

def view_bookings():
    cursor.execute("""SELECT b.id, g.name, r.room_number, b.check_in, b.check_out, b.total_amount, b.status 
                      FROM bookings b
                      JOIN guests g ON b.guest_id = g.id
                      JOIN rooms r ON b.room_id = r.id""")
    print("\n=== Bookings ===")
    for b in cursor.fetchall():
        print(f"Booking ID:{b[0]} | Guest:{b[1]} | Room:{b[2]} | Check-in:{b[3]} | Check-out:{b[4]} | Total:${b[5]:.2f} | Status:{b[6]}")

def main():
    while True:
        print("\n=== Hotel Booking System ===")
        print("1. Add Room")
        print("2. View Rooms")
        print("3. Add Guest")
        print("4. View Guests")
        print("5. Book Room")
        print("6. View Bookings")
        print("7. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_room()
        elif choice == '2':
            view_rooms()
        elif choice == '3':
            add_guest()
        elif choice == '4':
            view_guests()
        elif choice == '5':
            book_room()
        elif choice == '6':
            view_bookings()
        elif choice == '7':
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    print("Welcome to Simple Hotel Booking System!")
    main()
    conn.close()