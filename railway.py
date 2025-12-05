from sqlite3 import connect


def create_database(con, cur):
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute(
        """CREATE TABLE IF NOT EXISTS train(
            train_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL
        )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS coach(
            coach_id INTEGER PRIMARY KEY AUTOINCREMENT,
            train_id INTEGER NOT NULL,
            coach_type TEXT NOT NULL,
            total_seats INTEGER NOT NULL,
            fare DECIMAL NOT NULL,
            FOREIGN KEY(train_id) REFERENCES train(train_id)
        )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS seats(
            seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            coach_id INTEGER NOT NULL,
            seat_number INTEGER NOT NULL,
            is_booked BOOLEAN DEFAULT 0,
            FOREIGN KEY(coach_id) REFERENCES coach(coach_id)
        )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS passenger(
            passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            age INTEGER NOT NULL
        )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS pnr(
            pnr_id INTEGER PRIMARY KEY AUTOINCREMENT
        )"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS bookings(
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pnr_id INTEGER NOT NULL,
            passenger_id INTEGER NOT NULL,
            train_id INTEGER NOT NULL,
            coach_id INTEGER NOT NULL,
            seat_id INTEGER NOT NULL,
            booking_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(pnr_id) REFERENCES pnr(pnr_id),
            FOREIGN KEY(train_id) REFERENCES train(train_id),
            FOREIGN KEY(coach_id) REFERENCES coach(coach_id),
            FOREIGN KEY(seat_id) REFERENCES seats(seat_id),
            FOREIGN KEY(passenger_id) REFERENCES passenger(passenger_id)
        )"""
    )

    con.commit()


def get_number(prompt, convert=int):
    while True:
        try:
            value = convert(input(prompt))
            if value < 1:
                print("Error: Only positive number")
                continue
            return value
        except ValueError:
            print("Error: Invalid input")


def get_gender(prompt):
    while True:
        gender = input(prompt)
        if gender.upper() in ["M", "F", "O"]:
            return gender.upper()
        print("Error: Invalid input")


def menu():
    print("1. List trains")
    print("2. Book ticket")
    print("3. Cancel ticket")
    print("4. Search ticket")
    print("5. Search train")
    print("6. Admin panel (testing purposes)")
    print("7. Exit")
    print()


def calculate_fare(age, fare):
    if age < 5:
        return 0
    elif 5 <= age <= 60:
        return fare
    else:
        return fare * 0.5


def find_train(cur, train_id):
    cur.execute("SELECT * FROM train WHERE train_id = ?", (train_id,))
    return cur.fetchone()


def find_coach(cur, train_id, coach_type=""):
    if not coach_type:
        cur.execute("SELECT * FROM coach WHERE train_id = ?", (train_id,))
        return cur.fetchall()

    cur.execute(
        "SELECT * FROM coach WHERE train_id = ? AND LOWER(coach_type) = ?",
        (train_id, coach_type.lower()),
    )
    return cur.fetchone()


def find_seat(cur, coach_id):
    cur.execute(
        "SELECT * FROM seats WHERE coach_id = ? AND is_booked = 0 LIMIT 1",
        (coach_id,),
    )
    return cur.fetchone()


def create_pnr(con, cur):
    cur.execute("INSERT INTO pnr DEFAULT VALUES")
    con.commit()
    return cur.lastrowid


def fetchone(cur, query, params=()):
    cur.execute(query, params)
    return cur.fetchone()


def get_booking_details(cur, booking_id):
    seat_id = fetchone(
        cur, "SELECT seat_id FROM bookings WHERE booking_id = ?", (booking_id,)
    )[0]
    seat_number = fetchone(
        cur, "SELECT seat_number FROM seats WHERE seat_id = ?", (seat_id,)
    )[0]
    passenger_id = fetchone(
        cur, "SELECT passenger_id FROM bookings WHERE booking_id = ?", (booking_id,)
    )[0]
    passenger = fetchone(
        cur, "SELECT * FROM passenger WHERE passenger_id = ?", (passenger_id,)
    )

    return passenger, seat_number, seat_id


def list_trains(cur):
    cur.execute("SELECT * FROM train")
    trains = cur.fetchall()
    if not trains:
        print("Message: No trains found")
        return

    for train in trains:
        print("—————————————————————————————————————————————————————————————")
        train_number = train[0]
        name = train[1]
        source = train[2]
        destination = train[3]

        all_coaches = []

        coaches = find_coach(cur, train_number)
        for coach in coaches:
            all_coaches.append(coach[2])

        print("Train number:", train_number)
        print("Name:", name)
        print("Coaches:", ", ".join(all_coaches))
        print("Source:", source)
        print("Destination:", destination)

    print("———————————————————————————————————————————————————————————————")


def book_ticket(con, cur):
    number_of_tickets = get_number("How many ticket(s) you want to book? ")
    train_id = get_number("Enter train number (integer): ")
    train = find_train(cur, train_id)
    if not train:
        print("Message: Train not found")
        return

    coaches = find_coach(cur, train_id)
    if not coaches:
        print("Message: No coaches found in this train")
        return

    all_coaches = []

    for coach in coaches:
        all_coaches.append(coach[2])

    print("Available coaches:", ", ".join(all_coaches))

    while True:
        coach_type = input("Enter coach (case insensitive): ")
        coach_data = find_coach(cur, train_id, coach_type)
        if coach_data:
            break
        print("Message: Coach not found")

    pnr_id = create_pnr(con, cur)
    coach_id = coach_data[0]
    fare = coach_data[4]
    total_fare = 0

    for _ in range(number_of_tickets):
        name = input("Enter name: ")
        age = get_number("Enter age (integer): ")
        gender = get_gender("Enter gender (M/F/O): ")

        seat = find_seat(cur, coach_id)
        if seat:
            seat_id = seat[0]
            seat_number = seat[2]
            print("Seat number:", seat_number)

            cur.execute(
                "INSERT INTO passenger (name, age, gender) VALUES (?, ?, ?)",
                (name, age, gender),
            )
            passenger_id = cur.lastrowid

            cur.execute("UPDATE seats SET is_booked = 1 WHERE seat_id = ?", (seat_id,))
            cur.execute(
                "INSERT INTO bookings (passenger_id, pnr_id, train_id, coach_id, seat_id) VALUES (?, ?, ?, ?, ?)",
                (passenger_id, pnr_id, train_id, coach_id, seat_id),
            )

            print("Ticket booked successfully")
            total_fare += calculate_fare(age, fare)
        else:
            print("Message: Sorry, No seats available")
            return

    print("PNR:", pnr_id)
    print("Total fare:", total_fare)

    con.commit()


def cancel_booking(con, cur):
    pnr_id = get_number("Enter pnr (integer): ")
    cur.execute(
        "SELECT booking_id, passenger_id, train_id, coach_id FROM bookings WHERE pnr_id = ?",
        (pnr_id,),
    )
    bookings = cur.fetchall()
    if not bookings:
        print("Message: Ticket not found")
        return

    total_bookings = len(bookings)
    booking = bookings[0]
    print("Total number of tickets:", total_bookings)
    print("Common details:")

    train = find_train(cur, booking[2])

    print("Train name:", train[1])
    print("Source:", train[2])
    print("Destination:", train[3])

    cur.execute("SELECT * FROM coach WHERE coach_id = ?", (booking[3],))
    coach = cur.fetchone()

    print("Coach type:", coach[2])
    print("Ticket details:")

    total_cancelled = 0
    for booking in bookings:
        booking_id = booking[0]
        passenger, seat_number, seat_id = get_booking_details(cur, booking_id)

        print("Seat number:", seat_number)
        print("Name:", passenger[1])
        print("Age:", passenger[2])
        print("Gender:", passenger[3])
        print()

        cancel = input("Do you want to cancel this ticket? (Y/N): ")
        if cancel.lower() == "y":
            cur.execute("UPDATE seats SET is_booked = 0 WHERE seat_id = ?", (seat_id,))
            cur.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))
            total_cancelled += 1

    if total_cancelled == total_bookings:
        print("ALL ticket(s) cancelled successfully")
        cur.execute("DELETE FROM pnr WHERE pnr_id = ?", (pnr_id,))

    con.commit()


def search_ticket(cur):
    pnr_id = get_number("Enter pnr (integer): ")
    cur.execute(
        "SELECT booking_id, passenger_id, train_id, coach_id FROM bookings WHERE pnr_id = ?",
        (pnr_id,),
    )
    bookings = cur.fetchall()
    if not bookings:
        print("Message: Ticket not found")
        return

    print("Total number of tickets:", len(bookings))
    print("Common details:")

    train = find_train(cur, bookings[0][2])

    print("Train name:", train[1])
    print("Source:", train[2])
    print("Destination:", train[3])

    cur.execute("SELECT * FROM coach WHERE coach_id = ?", (bookings[0][3],))
    coach = cur.fetchone()

    print("Coach type:", coach[2])

    for booking in bookings:
        booking_id = booking[0]
        passenger, seat_number, seat_id = get_booking_details(cur, booking_id)

        print("Seat number:", seat_number)
        print("Name:", passenger[1])
        print("Age:", passenger[2])
        print("Gender:", passenger[3])
        print()


def search_train(cur):
    source = input("Enter source (case insensitive): ").lower()
    destination = input("Enter destination (case insensitive): ").lower()
    cur.execute(
        "SELECT * FROM train WHERE LOWER(source) = ? AND LOWER(destination) = ?",
        (source, destination),
    )
    trains = cur.fetchall()
    if not trains:
        print("Message: No train(s) found for the given source and destination")
        return

    for train in trains:
        print("—————————————————————————————————————————————————————————————")
        print("Train number:", train[0])
        print("Train name:", train[1])

    print("—————————————————————————————————————————————————————————————")


def add_train(con, cur):
    for _ in range(get_number("How many trains you want to add? ")):
        train_id = get_number("Enter train number (integer): ")
        train_name = input("Enter train name: ")
        source = input("Enter source: ")
        destination = input("Enter destination: ")

        cur.execute(
            "INSERT INTO train (train_id, name, source, destination) VALUES (?, ?, ?, ?)",
            (train_id, train_name, source, destination),
        )

    con.commit()


def add_coach(con, cur):
    train_id = get_number("Enter train number (integer): ")
    numbers_of_coaches = get_number("How many coaches you want to add? ")

    for _ in range(numbers_of_coaches):
        coach_type = input("Enter coach type: ")
        fare = get_number("Enter fare (float): ", float)
        total_seats = get_number("Enter total seats (integer): ")
        cur.execute(
            "INSERT INTO coach (train_id, coach_type, fare, total_seats) VALUES (?, ?, ?, ?)",
            (train_id, coach_type, fare, total_seats),
        )
        coach_id = cur.lastrowid

        for seat_number in range(1, total_seats + 1):
            cur.execute(
                "INSERT INTO seats (coach_id, seat_number) VALUES (?, ?)",
                (coach_id, seat_number),
            )

    con.commit()


def remove_train(con, cur):
    train_id = get_number("Enter train number (integer): ")
    if not find_train(cur, train_id):
        print("Message: Train not found")
        return

    cur.execute("SELECT * FROM bookings WHERE train_id = ?", (train_id,))
    if cur.fetchall():
        print("Message: Train has active bookings")
        return

    cur.execute("DELETE FROM bookings WHERE train_id = ?", (train_id,))
    cur.execute(
        "DELETE FROM seats WHERE coach_id IN (SELECT coach_id FROM coach WHERE train_id = ?)",
        (train_id,),
    )
    cur.execute("DELETE FROM coach WHERE train_id = ?", (train_id,))
    cur.execute("DELETE FROM train WHERE train_id = ?", (train_id,))

    con.commit()


def admin(con, cur):
    password = input("Enter the password: ")
    if password != "pass1234":
        print("Message: Access denied")
        return

    print("You're logged in to admin panel")
    while True:
        print("1. Add train")
        print("2. Add coach")
        print("3. Remove train")
        print("4. Logout")
        print()

        choice = input("Enter choice (integer): ")
        if choice == "1":
            add_train(con, cur)
        elif choice == "2":
            add_coach(con, cur)
        elif choice == "3":
            remove_train(con, cur)
        elif choice == "4":
            print("Logged out")
            break
        else:
            print("Message: Invalid choice")


def main(con, cur):
    print("———————————————————————————————————————")
    print("| WELCOME TO TRAIN RESERVATION SYSTEM |")
    print("———————————————————————————————————————")
    create_database(con, cur)

    while True:
        menu()
        choice = input("Enter choice (integer): ")
        if choice == "1":
            list_trains(cur)
        elif choice == "2":
            book_ticket(con, cur)
        elif choice == "3":
            cancel_booking(con, cur)
        elif choice == "4":
            search_ticket(cur)
        elif choice == "5":
            search_train(cur)
        elif choice == "6":
            admin(con, cur)
        elif choice == "7":
            print("Bye")
            break
        else:
            print("Message: Invalid choice")


con = connect("railway.db")
cur = con.cursor()

try:
    main(con, cur)
except Exception:
    import traceback

    print(traceback.format_exc())
finally:
    con.close()
