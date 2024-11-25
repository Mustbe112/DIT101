import datetime
import random

class Store:  #store data
    def __init__(self,date,id,name,phone1,phone,email,loots,from1,to,amount):

        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.date = date
        self.from1 = from1
        self.to = to
        self.amount = amount
        self.phone1 = phone1
        self.loots = loots

        f = open("Project1.csv","a")  #File Open
        f.write(f"{self.date},{self.id},{self.name},{self.phone1},{self.phone},{self.email},"
                    f"{self.loots},{self.from1},{self.to},{self.amount}\n") #Data input
        f.close() #File Close

def calculate_amount(destination, loots): #Calculate Amount

    if destination == "Bangkok":
        return 200 if loots <= 2 else 500
    elif destination == "Chaing Mai":
        return 1000 if loots <= 2 else 1500
    else:
        return 0
    



def Delivery(): #For Delivery Function
    random_number = random.randint(10000,99999) #to create ID Number
    ID = random_number
    Today = datetime.date.today() # to create today date

    Name = input("Enter Your Name : ")
    Phone1 = input("Enter Your Phone Number 1 : ")
    Phone = input("Enter Your Phone Number 2 : ")
    Email = input("Enter Your Email : ")
        
    from1 = "Rangsit"
    Amount = 0
    Loots = 0

    while True: #To loop when it wrongs
         to = input("Enter the City You Deliever (Bangkok and Chaing Mai): ").strip()
         available = ["Bangkok","Chaing Mai"]
         Loots = int(input("Enter Numbers of Loots : "))
         
         if  to not in available:
            print("Error occurs.")
            continue
         Amount = calculate_amount(to,Loots)
         break
        
    Store(Today,ID,Name,Phone1,Phone,Email,Loots,from1,to,Amount) #Use class Store

    print("------- Receipt ------- ")
    print(f"Date: {Today}")
    print(f"ID: {ID}   |   Name: {Name}")
    print(f"From: {from1}   |   To: {to}")
    print(f"Loots: {Loots}")
    print(f"Amount: {Amount}")
    print("*Do Not Lose Your ID Number*")
    print("-----------------------")
    

def Check(): #Check Receipt
    search_name = input("Enter Name: ").strip() 
    search_id = input("Enter ID Number : ").strip()
    found = False


    with open("Project1.csv", "r") as f: #to open file
        lines = f.readlines() #read the sentence 
        
    for line in lines:
        data = line.strip().split(',')
        if data[2].lower() == search_name.lower() and data[1] == search_id:
                found = True
                print(f"\n--- Receipt Found ---")
                print(f"Date: {data[0]}, ID: {data[1]}, Name: {data[2]}, Phone1: {data[3]}, Phone2: {data[4]}, "
                      f"Email: {data[5]}, Loots: {data[6]}, From: {data[7]}, To: {data[8]}, Amount: {data[9]}")
                break

    if not found:
            print(f"No receipt found for Name: {search_name} and ID: {search_id}.")


def main(): #main function
    print(".....Welcome To Delivery Service.....")
    print("Press 1 to Deliever Loots.")
    print("Press 2 to Check Receipt.")
    print("Press 3 to Edit the data .")
    print("Press 4 to cancel Ticket.")

    n = int(input("Enter : "))
    if n == 1:
        Delivery()
    elif n == 2:
        Check()
        
    elif n == 3:
        True    
main()    
        

            
        


 





    

