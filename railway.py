from mysql.connector import connect


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
    print("========================================")
    print("       RAILWAY RESERVATION SYSTEM       ")
    print("========================================")
    print(" 1. List Trains")
    print(" 2. Book Ticket")
    print(" 3. Cancel Ticket")
    print(" 4. Search Ticket")
    print(" 5. My Bookings")
    print(" 6. Search Train")
    print(" 7. Admin Panel")
    print(" 8. Exit")
    print("========================================")
    print()


def calculate_fare(age, fare):
    if age < 5:
        return 0
    elif 5 <= age <= 60:
        return fare
    else:
        return fare * 0.5


def find_train(cur, train_id):
    cur.execute("SELECT * FROM train WHERE train_id = %s", (train_id,))
    return cur.fetchone()


def find_coach(cur, train_id, coach_type=""):
    if not coach_type:
        cur.execute("SELECT * FROM coach WHERE train_id = %s", (train_id,))
        return cur.fetchall()

    cur.execute(
        "SELECT * FROM coach WHERE train_id = %s AND LOWER(coach_type) = %s",
        (train_id, coach_type.lower()),
    )
    return cur.fetchone()


def find_seat(cur, coach_id):
    cur.execute(
        "SELECT * FROM seats WHERE coach_id = %s AND is_booked = 0 LIMIT 1",
        (coach_id,),
    )
    return cur.fetchone()


def create_pnr(con, cur):
    cur.execute("INSERT INTO pnr () VALUES ()")
    con.commit()
    return cur.lastrowid


def fetchone(cur, query, params=()):
    cur.execute(query, params)
    return cur.fetchone()


def get_booking_details(cur, booking_id):
    seat_id = fetchone(
        cur, "SELECT seat_id FROM bookings WHERE booking_id = %s", (booking_id,)
    )[0]
    seat_number = fetchone(
        cur, "SELECT seat_number FROM seats WHERE seat_id = %s", (seat_id,)
    )[0]
    passenger_id = fetchone(
        cur, "SELECT passenger_id FROM bookings WHERE booking_id = %s", (booking_id,)
    )[0]
    passenger = fetchone(
        cur, "SELECT * FROM passenger WHERE passenger_id = %s", (passenger_id,)
    )

    return passenger, seat_number, seat_id


def list_trains(cur):
    print("========================================")
    print("         AVAILABLE TRAINS               ")
    print("========================================")

    cur.execute("SELECT * FROM train")
    trains = cur.fetchall()
    if not trains:
        print("  No trains found")
        print("========================================")
        return

    for i, train in enumerate(trains):
        train_number = train[0]
        name = train[1]
        source = train[2]
        destination = train[3]

        all_coaches = []
        coaches = find_coach(cur, train_number)
        for coach in coaches:
            all_coaches.append(coach[2])

        print("  Train Number:", train_number)
        print("  Name:", name)
        print("  Coaches:", ", ".join(all_coaches))
        print("  Source:", source)
        print("  Destination:", destination)

        if i < len(trains) - 1:
            print("  ----------------------------------------")

    print("========================================")


def book_ticket(con, cur):
    print("========================================")
    print("           BOOK TICKET                  ")
    print("========================================")

    number_of_tickets = get_number("How many ticket(s) you want to book? ")
    train_id = get_number("Enter train number: ")
    train = find_train(cur, train_id)
    if not train:
        print("Error: Train not found")
        return

    coaches = find_coach(cur, train_id)
    if not coaches:
        print("Error: No coaches found in this train")
        return

    all_coaches = []
    for coach in coaches:
        all_coaches.append(coach[2])

    print("Available coaches:", ", ".join(all_coaches))

    while True:
        coach_type = input("Enter coach type: ")
        coach_data = find_coach(cur, train_id, coach_type)
        if coach_data:
            break
        print("Error: Coach not found")

    pnr_id = create_pnr(con, cur)
    coach_id = coach_data[0]
    fare = coach_data[4]
    total_fare = 0

    print("PNR:", pnr_id)
    print("----------------------------------------")

    for i in range(number_of_tickets):
        print("Passenger", i + 1)
        name = input("  Name: ")
        age = get_number("  Age: ")
        gender = get_gender("  Gender (M/F/O): ")

        seat = find_seat(cur, coach_id)
        if seat:
            seat_id = seat[0]
            seat_number = seat[2]
            print("  Seat allocated:", seat_number)

            cur.execute(
                "INSERT INTO passenger (name, age, gender) VALUES (%s, %s, %s)",
                (name, age, gender),
            )
            passenger_id = cur.lastrowid

            cur.execute("UPDATE seats SET is_booked = 1 WHERE seat_id = %s", (seat_id,))
            cur.execute(
                "INSERT INTO bookings (passenger_id, pnr_id, train_id, coach_id, seat_id) VALUES (%s, %s, %s, %s, %s)",
                (passenger_id, pnr_id, train_id, coach_id, seat_id),
            )

            total_fare += calculate_fare(age, fare)
        else:
            print("Error: Sorry, No seats available")
            return

    print("----------------------------------------")
    print("Total fare: Rs.", total_fare)
    print("Booking PNR:", pnr_id)
    print("Ticket(s) booked successfully!")
    print("========================================")

    con.commit()


def cancel_booking(con, cur):
    print("========================================")
    print("           CANCEL TICKET                ")
    print("========================================")

    pnr_id = get_number("Enter PNR number: ")
    cur.execute(
        "SELECT booking_id, passenger_id, train_id, coach_id FROM bookings WHERE pnr_id = %s",
        (pnr_id,),
    )
    bookings = cur.fetchall()
    if not bookings:
        print("Error: Ticket not found")
        return

    total_bookings = len(bookings)
    booking = bookings[0]

    print("Total tickets:", total_bookings)
    print("----------------------------------------")
    print("COMMON DETAILS:")
    print("----------------------------------------")

    train = find_train(cur, booking[2])
    print("  Train:", train[1])
    print("  Route:", train[2], "->", train[3])

    cur.execute("SELECT * FROM coach WHERE coach_id = %s", (booking[3],))
    coach = cur.fetchone()
    print("  Coach:", coach[2])
    print("========================================")

    total_cancelled = 0
    for i, booking in enumerate(bookings):
        booking_id = booking[0]
        passenger, seat_number, seat_id = get_booking_details(cur, booking_id)

        print("Ticket", i + 1)
        print("  Seat:", seat_number)
        print("  Name:", passenger[1])
        print("  Age:", passenger[2])
        print("  Gender:", passenger[3])

        cancel = input("  Cancel this ticket? (Y/N): ")
        if cancel.lower() == "y":
            cur.execute("UPDATE seats SET is_booked = 0 WHERE seat_id = %s", (seat_id,))
            cur.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
            total_cancelled += 1
            print("  Ticket cancelled")
        else:
            print("  Ticket kept")
        print("----------------------------------------")

    if total_cancelled == total_bookings:
        cur.execute("DELETE FROM pnr WHERE pnr_id = %s", (pnr_id,))
        print("ALL tickets cancelled successfully!")

    con.commit()


def search_ticket(cur):
    print("========================================")
    print("           SEARCH TICKET                ")
    print("========================================")

    pnr_id = get_number("Enter PNR number: ")
    cur.execute(
        "SELECT booking_id, passenger_id, train_id, coach_id FROM bookings WHERE pnr_id = %s",
        (pnr_id,),
    )
    bookings = cur.fetchall()
    if not bookings:
        print("Error: Ticket not found")
        return

    print("Total tickets:", len(bookings))
    print("----------------------------------------")
    print("BOOKING DETAILS:")
    print("----------------------------------------")

    train = find_train(cur, bookings[0][2])
    print("  Train:", train[1])
    print("  Route:", train[2], "->", train[3])

    cur.execute("SELECT coach_type FROM coach WHERE coach_id = %s", (bookings[0][3],))
    coach = cur.fetchone()
    print("  Coach:", coach[0])
    print("========================================")

    for i, booking in enumerate(bookings):
        booking_id = booking[0]
        passenger, seat_number, _ = get_booking_details(cur, booking_id)

        print("Passenger", i + 1)
        print("  Seat:", seat_number)
        print("  Name:", passenger[1])
        print("  Age:", passenger[2])
        print("  Gender:", passenger[3])
        print("----------------------------------------")


def my_bookings(cur):
    print("========================================")
    print("            MY BOOKINGS                 ")
    print("========================================")

    cur.execute("SELECT * FROM bookings")
    bookings = cur.fetchall()
    if not bookings:
        print("  No bookings found")
        print("========================================")
        return

    for i, booking in enumerate(bookings):
        pnr_id = booking[1]
        train_id = booking[3]
        coach_id = booking[4]
        booking_datetime = booking[6]

        train = find_train(cur, train_id)
        cur.execute("SELECT coach_type FROM coach WHERE coach_id = %s", (coach_id,))
        coach = cur.fetchone()

        print("Booking", i + 1)
        print("----------------------------------------")
        print("  PNR:", pnr_id)
        print("  Booked on:", booking_datetime)
        print("  Train:", train[1])
        print("  Route:", train[2], "->", train[3])
        print("  Coach:", coach[0])
        print("========================================")


def search_train(cur):
    print("========================================")
    print("           SEARCH TRAIN                 ")
    print("========================================")

    source = input("Enter source: ").lower()
    destination = input("Enter destination: ").lower()
    cur.execute(
        "SELECT * FROM train WHERE LOWER(source) = %s AND LOWER(destination) = %s",
        (source, destination),
    )
    trains = cur.fetchall()
    if not trains:
        print("Error: No trains found for the given route")
        return

    print("Found", len(trains), "train(s):")
    print("========================================")

    for train in trains:
        print("  Train:", train[1])
        print("  Number:", train[0])
        print("  Route:", train[2], "->", train[3])
        print("----------------------------------------")


def add_train(con, cur):
    print("========================================")
    print("             ADD TRAIN                  ")
    print("========================================")

    num_trains = get_number("How many trains you want to add? ")

    for train_count in range(num_trains):
        print("\n----------------------------------------")
        print("Train", train_count + 1, "of", num_trains)
        print("----------------------------------------")

        train_id = get_number("Enter train number: ")
        if find_train(cur, train_id):
            print("Error: Train already exists")
            return

        train_name = input("Enter train name: ")
        source = input("Enter source: ")
        destination = input("Enter destination: ")

        cur.execute(
            "INSERT INTO train (train_id, name, source, destination) VALUES (%s, %s, %s, %s)",
            (train_id, train_name, source, destination),
        )

        add_coach(cur, train_id)
        print("Train details added successfully")

    print("\n========================================")
    print("All trains added successfully")
    print("========================================")

    con.commit()


def add_coach(cur, train_id):
    print("\n  Adding coaches for train", train_id)
    print("  --------------------------------------")

    numbers_of_coaches = get_number("  How many coaches you want to add? ")

    for coach_count in range(numbers_of_coaches):
        print("\n    Coach", coach_count + 1, "of", numbers_of_coaches)
        print("    ----------------------------------")

        coach_type = input("    Enter coach type: ")
        fare = get_number("    Enter fare: ", float)
        total_seats = get_number("    Enter total seats: ")

        cur.execute(
            "INSERT INTO coach (train_id, coach_type, fare, total_seats) VALUES (%s, %s, %s, %s)",
            (train_id, coach_type, fare, total_seats),
        )

        coach_id = cur.lastrowid
        add_seat(cur, coach_id, total_seats)
        print("    Coach added successfully")

    print("\n  --------------------------------------")
    print("  All coaches added for train", train_id)


def add_seat(cur, coach_id, total_seats):
    for seat_number in range(1, total_seats + 1):
        cur.execute(
            "INSERT INTO seats (coach_id, seat_number) VALUES (%s, %s)",
            (coach_id, seat_number),
        )


def remove_train(con, cur):
    print("========================================")
    print("           REMOVE TRAIN                 ")
    print("========================================")

    train_id = get_number("Enter train number: ")
    if not find_train(cur, train_id):
        print("Error: Train not found")
        return

    cur.execute("SELECT * FROM bookings WHERE train_id = %s", (train_id,))
    if cur.fetchall():
        print("Error: Train has active bookings")
        return

    cur.execute("DELETE FROM bookings WHERE train_id = %s", (train_id,))
    cur.execute(
        "DELETE FROM seats WHERE coach_id IN (SELECT coach_id FROM coach WHERE train_id = %s)",
        (train_id,),
    )
    cur.execute("DELETE FROM coach WHERE train_id = %s", (train_id,))
    cur.execute("DELETE FROM train WHERE train_id = %s", (train_id,))

    print("Train removed successfully")
    con.commit()


def admin(con, cur):
    print("========================================")
    print("            ADMIN PANEL                 ")
    print("========================================")

    password = input("Enter the password: ")
    if password != "pass1234":
        print("Error: Access denied")
        return

    print("Logged in to admin panel")

    while True:
        print("\n========================================")
        print("             ADMIN MENU                ")
        print("========================================")
        print(" 1. Add Train")
        print(" 2. Remove Train")
        print(" 3. Logout")
        print("========================================")

        choice = input("Enter choice: ")
        if choice == "1":
            add_train(con, cur)
        elif choice == "2":
            remove_train(con, cur)
        elif choice == "3":
            print("Logged out")
            break
        else:
            print("Error: Invalid choice")


def main(con, cur):
    print("========================================================")
    print("                                                        ")
    print("        WELCOME TO TRAIN RESERVATION SYSTEM            ")
    print("                                                        ")
    print("========================================================")
    print()

    while True:
        menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            list_trains(cur)
        elif choice == "2":
            book_ticket(con, cur)
        elif choice == "3":
            cancel_booking(con, cur)
        elif choice == "4":
            search_ticket(cur)
        elif choice == "5":
            my_bookings(cur)
        elif choice == "6":
            search_train(cur)
        elif choice == "7":
            admin(con, cur)
        elif choice == "8":
            print("\nThank you for using our service!")
            print("Have a safe journey!")
            print()
            break
        else:
            print("Error: Invalid choice")


con = connect(
    host="localhost",
    user="root",
    password="Pass@1234",
    database="railway_reservation_system",
)
cur = con.cursor()

main(con, cur)
