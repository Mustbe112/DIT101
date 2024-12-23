import datetime
import random
import csv
import os
import re

class DeliveryService:  # Initialize the service with a CSV file and ensure it exists.
    def __init__(self, file_name):
        self.file_name = file_name
        self.initialize_csv()

    def initialize_csv(self): # Create the CSV file with headers if it doesn't exist.
        if not os.path.exists(self.file_name):
            with open(self.file_name, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "ID", "Name", "Phone1", "Phone2", "Email", "Weight", 
                "From", "To", "Amount", "Status"])

    @staticmethod
    def is_valid_thai_phone(phone):  # Validate if the phone number is a valid Thai phone number.
        return re.fullmatch(r"^0[689]\d{8}$", phone) is not None

    @staticmethod
    def is_valid_email(email): # Validate if the email address is in a valid format.
        return re.fullmatch(r"^[\w.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None

    @staticmethod
    def is_valid_thai_city(city): # Check if the city is in the predefined list of Thai cities.
        thai_cities = ["Bangkok", "Chiang Mai", "Phuket", "Pattaya", "Hua Hin", "Ayutthaya", 
        "Chiang Rai", "Krabi", "Nakhon Ratchasima", "Samut Prakan", "Nonthaburi", "Pathum Thani"]
        return city in thai_cities

    @staticmethod
    def show_available_cities(): # Display the list of available cities for delivery.
        thai_cities = ["Bangkok", "Chiang Mai", "Phuket", "Pattaya", "Hua Hin", "Ayutthaya", 
        "Chiang Rai", "Krabi", "Nakhon Ratchasima", "Samut Prakan", "Nonthaburi", "Pathum Thani"]
        print("\nAvailable cities in Thailand:")
        print(", ".join(thai_cities))

    @staticmethod
    def calculate_amount(destination, weight): # Calculate the delivery cost based on weight and destination.
        base_rate = 50  # Base rate per kg
        return base_rate * weight if DeliveryService.is_valid_thai_city(destination) else 0
 
    def read_csv(self): # Read the content of the CSV file.
        try:
            with open(self.file_name, "r") as file:
                return list(csv.reader(file))
        except FileNotFoundError:
            return []

    def write_csv(self, rows): # Write rows to the CSV file, overwriting existing content.
        with open(self.file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def append_to_csv(self, row): # Append a new row to the CSV file.
        with open(self.file_name, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)

    def display_all_information(self): # Display all records from the CSV file.
        rows = self.read_csv()
        if len(rows) > 1:
            print("\n--- All Information ---")
            for row in rows:
                print(", ".join(row))
        else:
            print("No data available.")

    def display_total_count(self): # Display the total number of entries in the CSV file.
        rows = self.read_csv()
        count = len(rows) - 1  # Exclude header row
        print(f"\nTotal Entries: {count}")

    def search_information(self): # Search for entries based on ID or Name.
        search_term = input("Enter ID or Name to search: ").strip()
        rows = self.read_csv()
        found = False

        print("\n--- Search Results ---")
        for row in rows:
            if search_term.lower() in row[1].lower() or search_term.lower() in row[2].lower():
                found = True
                print(", ".join(row))

        if not found:
            print("No matching entries found.")

    def delete_information(self): # Delete an entry based on the given ID.
        delete_id = input("Enter the ID to delete: ").strip()
        rows = self.read_csv()
        updated_rows = [rows[0]]  # Keep the header row
        deleted = False

        for row in rows[1:]:
            if row[1] != delete_id:
                updated_rows.append(row)
            else:
                deleted = True

        self.write_csv(updated_rows)

        if deleted:
            print(f"Entry with ID {delete_id} has been deleted.")
        else:
            print(f"No entry found with ID {delete_id}.")

    def check_receipt(self):  # Check and display receipt details based on Name and ID.
        search_name = input("Enter Name: ").strip()
        search_id = input("Enter ID Number: ").strip()
        rows = self.read_csv()

        found = False
        for row in rows:
            if row[2].lower() == search_name.lower() and row[1] == search_id:
                found = True
                print("\n--- Receipt Found ---")
                print(f"Date: {row[0]}, ID: {row[1]}, Name: {row[2]}")
                print(f"Phone1: {row[3]}, Phone2: {row[4]}, Email: {row[5]}")
                print(f"Weight: {row[6]} kg")
                print(f"From: {row[7]} | To: {row[8]}")
                print(f"Amount: {row[9]} THB | Status: {row[10]}")
                break

        if not found:
            print(f"No receipt found for Name: {search_name} and ID: {search_id}.")

    def delivery(self): # Handle the delivery process and record details.
        random_id = random.randint(10000, 99999)
        today_date = datetime.date.today()

        print("\n--- Enter Delivery Details ---")
        name = input("Enter Your Name: ").strip()
        phone1 = self.prompt_valid_phone("Enter Your Primary Phone Number (0XXXXXXXXX): ")
        phone2 = self.prompt_valid_phone("Enter Your Secondary Phone Number (0XXXXXXXXX): ")
        email = self.prompt_valid_email("Enter Your Email: ")
        while True:
            try:
                weight = float(input("Enter Product Weight (kg): "))
                if weight <= 0:
                    print("Weight must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid weight. Please enter a valid number.")

        while True:
            print("\nChoose a 'From' location:")
            self.show_available_cities()
            from_location = input("Enter the From Location: ").strip()
            if not self.is_valid_thai_city(from_location):
                print("Invalid city. Please select a valid 'From' location.")
                continue
            break

        while True:
            print("\nChoose a 'To' location:")
            self.show_available_cities()
            to_location = input("Enter the To Location: ").strip()
            if not self.is_valid_thai_city(to_location):
                print("Delivery not available for this city. Please enter a valid city in Thailand.")
                continue
            if to_location == from_location:
                print("From and To locations cannot be the same.")
                continue
            break

        amount = self.calculate_amount(to_location, weight)

        self.append_to_csv([today_date, random_id, name, phone1, phone2, email, weight, from_location, to_location, amount, "Pending"])

        print("\n--- Receipt ---")
        print(f"Date: {today_date}")
        print(f"ID: {random_id}   |   Name: {name}")
        print(f"Email: {email}")
        print(f"Weight: {weight} kg")
        print(f"From: {from_location}   |   To: {to_location}")
        print(f"Amount: {amount} THB")
        print("Status: Pending")
        print("*Do Not Lose Your ID Number*")
        print("-----------------------")

    @staticmethod
    def prompt_valid_phone(prompt): # Prompt for and validate a phone number.
        while True:
            phone = input(prompt).strip()
            if not phone or DeliveryService.is_valid_thai_phone(phone):
                return phone
            print("Invalid phone number. Please enter a valid Thai phone number.")

    @staticmethod
    def prompt_valid_email(prompt): # Prompt for and validate an email address.
        while True:
            email = input(prompt).strip()
            if not email or DeliveryService.is_valid_email(email):
                return email
            print("Invalid email address. Please enter a valid email.")
    
    def checkout(self):
        rows = self.read_csv()
        if len(rows) <= 1:
            print("No data avaialable for checkout.")
            return
        
        checkout_id = input("Enter ID to Check Out product: ").strip()
        checkout_name = input("Enter Name: ").strip()
        update_row = []
        found = False

        for row in rows:
            if row[1] == checkout_id and row[2].lower() == checkout_name.lower():
                found = True
                if row[10].lower() == "delivered":
                    print(f"Delivery ID {checkout_id} is already marked as 'Delivered'.")
                else:
                    row[10] = "Delivered"  # Correct the assignment operator and status
                    print(f"Delivery ID {checkout_id} has been successfully updated to 'Delivered'.")
            update_row.append(row)
        if not found:
           print(f"No delivery found with ID {checkout_id}.")
           return 

        self.write_csv(update_row)  

    def edit_information(self):
     rows = self.read_csv()
     if len(rows) <= 1:
        print("No data available to edit.")
        return

     edit_id = input("Enter ID to edit: ").strip()
     edit_name = input("Enter Name: ").strip()
     found = False

     for row in rows[1:]:
        if row[1] == edit_id and row[2].lower() == edit_name.lower():
            found = True
            print("Editing record:", ", ".join(row))
            row[3] = self.prompt_valid_phone(f"Enter new Primary Phone (current: {row[3]}): ") or row[3]
            row[4] = self.prompt_valid_phone(f"Enter new Secondary Phone (current: {row[4]}): ") or row[4]
            row[5] = self.prompt_valid_email(f"Enter new Email (current: {row[5]}): ") or row[5]
            while True:
             try:
                row[6] = float(input(f"Enter new Weight (current: {row[6]}): ")) or row[6]
                if row[6] <= 0:
                    print("Weight must be positive.")
                    continue
                break
             except ValueError:
                print("Invalid weight. Please enter a valid number.")

            while True:
             print("\nChoose a 'From' location:")
             self.show_available_cities()
             row[7] = input(f"Enter new From (current: {row[7]}): ").strip() or row[7]
             if not self.is_valid_thai_city(row[7]):
                print("Invalid city. Please select a valid 'From' location.")
                continue
             break

            while True:
             print("\nChoose a 'To' location:")
             self.show_available_cities()
             row[8] = input(f"Enter new To (current: {row[8]}): ").strip() or row[8]
             if not self.is_valid_thai_city(row[8]):
                print("Delivery not available for this city. Please enter a valid city in Thailand.")
                continue
             if row[7] == row[8]:
                print("From and To locations cannot be the same.")
                continue
             break

            amount = self.calculate_amount(row[8], row[6])
            row[9] = amount
            row[10] = row[10]
            break
     if not found:
        print("No matching record found to edit.")
        return
     self.write_csv(rows)
     print("Record updated successfully.")

def main(): # Main program loop to navigate delivery service options.
    service = DeliveryService("Project1.csv")

    while True:
        print("\n..... Welcome To Delivery Service .....")
        print("1. Deliver Product")
        print("2. Check Receipt")
        print("3. Display All Information")
        print("4. Display Total Count")
        print("5. Search Information")
        print("6. Delete Information")
        print("7. Check Out Product.")
        print("8. Edit Information")
        print("9. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            service.delivery()
        elif choice == 2:
            service.check_receipt()
        elif choice == 3:
            service.display_all_information()
        elif choice == 4:
            service.display_total_count()
        elif choice == 5:
            service.search_information()
        elif choice == 6:
            service.delete_information()
        elif choice == 7:
            service.checkout()
        elif choice == 8:
            service.edit_information()
        elif choice == 9:
            print("Thank you for using the Delivery Service. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

main()
