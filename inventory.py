from tabulate import tabulate


# Class to display some text in colour
class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
# Shoe class which has constructor based on 'country', 'code', 'product', 'cost', 'quantity'.

class Shoe:
    
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
    
# Displays str to terminal

    def __str__(self):
        return f"""-----------
Country: {self.country} 
Code: {self.code} 
Product: {self.product}
Cost(ZAR): {self.cost}
Quantity: {self.quantity}
------------"""

# Str format to be used to write to file and also to display to terminal in tabular format

    def to_file(self):
        return (f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}")
        

#=============Shoe list===========
# The list will be used to store a list of objects of shoes.
shoe_list = []

#==========Functions outside the class==============

# Reads from 'inventory.txt', creates shoe objects and appends to 'shoe_list'
# It accounts for 'File not found' error

def read_shoes_data():
    try:
        file = open("inventory.txt", "r", encoding = "utf-8-sig")
        content = file.readlines()
        for line in content [1:]:
            country, code, product, cost, quantity = line.strip("\n").split(",")
            shoe_obj = Shoe(country, code, product, cost, quantity)
            shoe_list.append(shoe_obj)
    except FileNotFoundError:
        print (bcolors.FAIL + "File 'inventory.txt' not found. Please double check it is saved in the same location as this programme." + bcolors.ENDC)

# The following takes inputs from the user creates & appends shoe object to 'shoe_list' and updates 'inventory.txt' file. 
# Value checks have been built in to ensure that user enters at least 2 characters for 'Country', 'Code', 'Product' and numbers for 'Cost' and 'Quantity'
# At each input stage it gives user an option to abort entry by entering '0'
# NOTE: before user adds 'quantity' user's entry is checked for a DUPLICATE based on entries entered so far 
# ('Country', 'Code', 'Product' and 'Cost' --> all have to be EXACT matches for duplicate to flag)

def capture_shoes():
    print("You are now adding new product. If need to cancel this entry please enter '0' at any time.")
    while True:
        country_inp = input("Please enter COUNTRY: ")
        if country_inp == "0":
            print(bcolors.WARNING + "Adding new product was aborted. No changes made to the record."+ bcolors.ENDC)
            return
        elif len(country_inp) >= 2:
            break
        else:
            print(bcolors.FAIL + "Error: 'Country' has to have at least 2 characters. Please try again."+ bcolors.ENDC)
    while True: 
        code_inp = input("Please enter CODE (ex. SKU44386): ")
        if code_inp == "0":
            print(bcolors.WARNING + "Adding new product was aborted. No changes made to the record."+bcolors.ENDC)
            return
        if len(code_inp) >= 2:
            break
        else:
            print(bcolors.FAIL + "Error: 'Code' has to have at least 2 characters. Please try again." + bcolors.ENDC)
    while True: 
        product_inp = input("Please enter PRODUCT (ex. Air Max): ")
        if product_inp == "0":
            print("Adding new product was aborted. No changes made to the record.")
            return
        if len(product_inp) >= 2:
            break
        else:
            print(bcolors.FAIL + "Error: 'Product' has to have at least 2 characters. Please try again.")
    while True:
        try:
            cost_inp = round(float(input("Please enter COST in ZAR (ex. 3400): ")),2)
            if cost_inp == 0:
                print(bcolors.WARNING + "Adding new product was aborted. No changes made to the record."+bcolors.ENDC)
                return
            break
        except ValueError:
            print(bcolors.FAIL + "Error: The entry was not a number.Please try again.")
    for i, line in enumerate(shoe_list):  # this is duplicate check
        if country_inp == line.country and code_inp == line.code and product_inp == line.product and cost_inp == round(float(line.cost),2):
            print(bcolors.FAIL + f"""Error: Entry canceled, because DUPLICATE entry found:\n {shoe_list[i]} \n 
            If need to update quantity please choose '5 - SEARCH/UPDATE' from menu.""" + bcolors.ENDC)
            return
    while True:
        try:        
            quantity_inp = int(input("Please enter QUANTITY: "))
            if quantity_inp == 0:
                print(bcolors.WARNING + "Adding new product was aborted. No changes made to the record." + bcolors.ENDC)
                return
            new_product = (Shoe(country_inp, code_inp, product_inp, cost_inp, quantity_inp))
            shoe_list.append(new_product)
            file_update()
            print(bcolors.OKGREEN + f"{new_product}\nHas been added to inventory records."+ bcolors.ENDC)
            break
        except ValueError:
            print(bcolors.FAIL + "Error: The entry was not a number. Please try again."+ bcolors.ENDC)


# Displays all 'shoe_list' data in a tabular grid format

def view_all():
    list_all = []
    for line in shoe_list:
        split_line= line.to_file().split(",")
        list_all.append(split_line)
    print(tabulate(list_all, headers = ["Index","Country","Code","Product","Cost","Quantity"], showindex = "always", tablefmt = "grid"))

# Writes 'shoe_list' data to 'inventory.txt' file. 

def file_update():
    inventory_file = open("inventory.txt","w",encoding = "utf-8-sig")
    inventory_file.write("Country,Code,Product,Cost,Quantity") 
    for line in shoe_list:
        str_data = line.to_file()
        inventory_file.write(f"\n{str_data}")
    inventory_file.close()

# Finds the minimum stock quantity and asks user to input how many to be re-stocked/added. 
# It then adds user's entry to current stock and updates stock quantity in the 'shoe_list' and 'inventory.txt' file.
# Check is added in case user enter's non-number. Also, user has an option to enter '0' to return to the menu.

def re_stock():
    index = 0
    lowest_qty = shoe_list[index]
    for i, qty in enumerate(shoe_list):
        if int(lowest_qty.quantity) > int(qty.quantity):
            index = i
            lowest_qty = qty
    print(f"The lowest stock is for:\n{lowest_qty}")
    while True:
        try:
            add_qty = int(input("Please add RE-STOCKING quantity or '0' to return to the menu: "))
            shoe_list[index].quantity= int(lowest_qty.quantity) + add_qty
            file_update()
            print(bcolors.OKGREEN + f"Updated record:\n{lowest_qty}" + bcolors.ENDC)
            break
        except ValueError:
            print(bcolors.FAIL + "Error: The entry was not a number. Please try again." + bcolors.ENDC)

# Searches for a shoe from the list using the shoe code and displays it to the user. 
# If not found, displays an error message with suggestion either to re-enter or to return to main menu to add new item. 
# User has an option to enter '0' to end search and to return to main menu. 

def search_shoe():
    global code_inp
    found = False
    while True:
        code_inp = input("Please enter shoe code (ex. SKU899990): ")
        if code_inp == "0":
            print("You chose '0' and are being returned to main menu.")
            break
        for line in shoe_list:
            if code_inp == line.code:
                print(line)
                found = True
        if found == True:
            break
        elif found == False:
            print(bcolors.FAIL + f"Unfortunately, '{code_inp}' not found. Please double check and try again or enter '0' to go back to the menu and choose '4 - add NEW product'" + bcolors.ENDC)  

# The following takes in 3 parameters: 'code_inp (product code), 'position' (what needs updating for SKU, ex. country, etc), 'new_input' (new value)
# It displays updated item to the user and updates file. 

def update_item(code_inp, position, new_input):
    for line in shoe_list:
        if code_inp == line.code:
            if position == "country":
                line.country = new_input
            elif position == "code":
                line.code = new_input
            elif position == "product":
                line.product = new_input
            elif position == "cost":
                line.cost = new_input
            elif position == "quantity": 
                line.quantity = new_input
            print(line)
    file_update()
    print(bcolors.OKGREEN + "Record updated." + bcolors.ENDC)
    
# Calculates total value of each item (value = cost*quantity) 
# Displays all items in tabular grid format with 'Value' column added to the far right and total inventory value appended to the bottom of the table. 

def value_per_item():
    list_all = []
    inventory_total = 0
    for line in shoe_list:
        value = float(line.cost) * int(line.quantity)
        split_line = line.to_file().split(",")
        split_line.append(value)
        list_all.append(split_line)
        inventory_total += int(value)
    print(tabulate(list_all,headers = ["Index","Country","Code","Product","Cost","Quantity","Value"],showindex="always",tablefmt="grid"))
    print(bcolors.OKBLUE + f"\t\t\t\t\t\t\tTotal inventory value: {inventory_total:,} ZAR" + bcolors.ENDC)

# Finds max quantity item and offers user to mark it for sale. If user selects 'Y' then it is displayed that item has been marked for sale. 

def highest_qty():
    index = 0
    max_qty = shoe_list [index]
    for i, line in enumerate(shoe_list):
        if int(max_qty.quantity) < int(line.quantity):
            index = i
            max_qty = shoe_list[index]
    print(f"\nThe following item has the highest quantity: \n{max_qty} \n ")
    while True: 
        sale = input("Please enter 'Y' or 'N' if to mark the item for sale: ") 
        if sale.lower() == "n":
            print("\nYou chose not to mark it for sale and are being returned to main menu.")
            break
        elif sale.lower() == "y":
            print (bcolors.OKGREEN + "This item has now been marked as 'FOR SALE'."+ bcolors.ENDC)
            break
        else: 
            print(bcolors.FAIL + "Error: incorrect choice. Please try again" + bcolors.ENDC)

#==========Main Menu=============

menu = ("""\n\tInventory Menu: 
1 - view ALL inventory
2 - view LOWEST stock / RE-STOCK
3 - view HIGHEST stock / mark for SALE
4 - add NEW product
5 - SEARCH product (by SKU) / UPDATE
6 - exit
""")

# User is presented with the menu and has to enter option between 1 and 6. Error is displayed if choice is out of bounds or non-numeric value is entered.
while True: 
    try:
        shoe_list = []
        print(menu)
        user_choice = int(input("To proceed please enter a corresponding number from the menu (ex. 1): "))
        read_shoes_data()
        if user_choice < 1 or user_choice > 6:
            print(bcolors.FAIL + "Error: Entry does not correspond with any menu options. Please try again." + bcolors.ENDC)

# Menu option 1 - displays ALL inventory in grid table and asks user if want to see 'Value' column added to the grid. Adds 'Value' in case user chooses 'Y'.
# if 'N' returns to menu. Displays error if neither 'Y' or 'N' was entered. 
        elif user_choice == 1: 
            print("\nHere is the summary table of current inventory: ")
            view_all()
            while True:
                add_value = input("Please enter 'Y' or 'N' if would like to add and see 'Value' column: ").lower() 
                if add_value =="y":
                    print("\nNow here is summary along with VALUE column: ")
                    value_per_item()
                    break
                elif add_value == "n":
                    break
                else:
                    print(bcolors.FAIL + "Error: incorrect entry. Please try again." + bcolors.ENDC)
# Menu option 2 - finds lowest quantity item and offers user to enter re-stocking quantity, adds it to current and updates records. 
# There are error checks, but please see 're_stock()' function comments for more details
        elif user_choice == 2:
            re_stock()
# Menu option 3 - finds maximum quantity item and offers user to mark it for sale
# Please see 'highest_qty()' function comments for more details.
        elif user_choice == 3:
            highest_qty()
# Menu option 4 - takes user input to add new item. There are error checks, duplicate entry check and options for user to abort entry.
# Please see 'capture_shoes()' function comments for more details.
        elif user_choice == 4:
            capture_shoes()
# Menu option 5 - takes product code from user to search for item. Also, if item not found user has an option to exit search by entering '0'.
# If item found offers to update and allows user to enter what to update and with what value, then list and file are updated with new value. 
# User can enter 'done' once user is done updating item's attributes. 
# There are checks for errors: 
# - if update entry by user was something other than 'Y' or 'N'
# - if non-number entered as new value for 'cost' or 'quantity'.
        elif user_choice == 5:
            search_shoe()
            while True:
                if code_inp == "0":
                    break
                update = input("Please enter 'Y' or 'N' if would like to update: ")
                if update.lower() == "n":
                    break
                elif update.lower() == "y":
                    while True:
                        update_opt = input(f"Please enter what would like to update for {code_inp} (ex. 'Cost') or 'Done' if done updating: ").lower()
                        if update_opt == "done":
                            break
                        elif update_opt == "country" or update_opt =="code" or update_opt =="product":
                            new_input = input(f"Please enter new {update_opt} for {code_inp}: ")
                            update_item(code_inp,update_opt,new_input)
                        elif update_opt == "cost" or update_opt =="quantity":
                            while True: 
                                try: 
                                    new_input = input(f"Please enter new {update_opt} for {code_inp}: ")
                                    if update_opt == "cost":
                                        new_input =float(new_input)
                                    elif update_opt =="quantity":
                                        new_input = int(new_input)
                                    break
                                except ValueError: 
                                    print(bcolors.FAIL + f"Error: entry was not a number. '{update_opt}' has to be a number." +bcolors.ENDC)
                            update_item(code_inp,update_opt,new_input)
                        else:
                            print(bcolors.FAIL + "Error: incorrect choice. Please try again." + bcolors.ENDC)
                            continue
                    break
                else:
                    print(bcolors.FAIL + "Error: incorrect entry. Please try again." + bcolors.ENDC)
# Menu option 6 - Displays exit message to user and exits.
        elif user_choice == 6:
            print("Thank you for your hard work! Goodbye for now. Hope to see you soon :)")
            exit()
    except ValueError:
        print(bcolors.FAIL + "Error: Entry was not a number. Please try again." + bcolors.ENDC)    