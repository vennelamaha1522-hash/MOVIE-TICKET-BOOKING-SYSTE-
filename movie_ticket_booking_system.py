import os
from datetime import datetime

class TicketNotFound(Exception):
    pass


class User:
    def __init__(self, name):
        self.name = name

    def display_role(self):
        print("User")


class Customer(User):
    def display_role(self):
        print("Customer")


class Admin(User):
    def display_role(self):
        print("Admin")


class Ticket:
    ticket_counter = 100  

    def __init__(self, customer_name, movie_name):
        Ticket.ticket_counter += 1
        self.ticket_id = Ticket.ticket_counter
        self.customer_name = customer_name
        self.movie_name = movie_name
        self.__status = "Booked"   
        self.created_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def cancel_ticket(self):
        self.__status = "Cancelled"

    def get_status(self):
        return self.__status

    def display_ticket(self):
        print("\n---------------------------")
        print("Ticket ID:", self.ticket_id)
        print("Customer Name:", self.customer_name)
        print("Movie Name:", self.movie_name)
        print("Status:", self.__status)
        print("Booked On:", self.created_date)
        print("---------------------------")


class TicketManager:
    def __init__(self):
        self.tickets = {}    
        self.ticket_ids = set()  

    def create_ticket(self, customer_name, movie_name):
        ticket = Ticket(customer_name, movie_name)
        self.tickets[ticket.ticket_id] = ticket
        self.ticket_ids.add(ticket.ticket_id)
        print("\nTicket Booked Successfully!")
        ticket.display_ticket()

    def view_all_tickets(self):
        if not self.tickets:
            print("No bookings found.")
            return
        for ticket in self.tickets.values():
            ticket.display_ticket()

    def cancel_ticket(self, ticket_id):
        try:
            if ticket_id not in self.ticket_ids:
                raise TicketNotFound("Ticket ID not found!")
            self.tickets[ticket_id].cancel_ticket()
            print("Ticket Cancelled Successfully!")
        except TicketNotFound as e:
            print("Error:", e)

    def delete_ticket(self, ticket_id):
        try:
            if ticket_id not in self.ticket_ids:
                raise TicketNotFound("Ticket ID not found!")
            del self.tickets[ticket_id]
            self.ticket_ids.remove(ticket_id)
            print(" Booking Deleted Successfully!")
        except TicketNotFound as e:
            print("Error:", e)

    def save_to_file(self):
        with open("movie_tickets.txt", "w") as file:
            for ticket in self.tickets.values():
                file.write(f"{ticket.ticket_id},{ticket.customer_name},{ticket.movie_name},{ticket.get_status()},{ticket.created_date}\n")
        print(" Data Saved to File!")

    def load_from_file(self):
        if not os.path.exists("movie_tickets.txt"):
            return
        with open("movie_tickets.txt", "r") as file:
            for line in file:
                tid, name, movie, status, date = line.strip().split(",")
                ticket = Ticket(name, movie)
                ticket.ticket_id = int(tid)
                ticket.created_date = date
                if status == "Cancelled":
                    ticket.cancel_ticket()
                self.tickets[int(tid)] = ticket
                self.ticket_ids.add(int(tid))


def main():
    manager = TicketManager()
    manager.load_from_file()

    while True:
        print("\n===== MOVIE TICKET BOOKING SYSTEM =====")
        print("1. Book Ticket")
        print("2. View All Bookings")
        print("3. Cancel Ticket")
        print("4. Delete Booking")
        print("5. Save & Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter Customer Name: ")
            movie = input("Enter Movie Name: ")
            manager.create_ticket(name, movie)

        elif choice == "2":
            manager.view_all_tickets()

        elif choice == "3":
            try:
                tid = int(input("Enter Ticket ID to Cancel: "))
                manager.cancel_ticket(tid)
            except ValueError:
                print("Invalid Input!")

        elif choice == "4":
            try:
                tid = int(input("Enter Ticket ID to Delete: "))
                manager.delete_ticket(tid)
            except ValueError:
                print("Invalid Input!")

        elif choice == "5":
            manager.save_to_file()
            print("Exiting Program...")
            break

        else:
            print("Invalid Choice!")


if __name__ == "__main__":
    main()