import json
import os
from datetime import datetime
from openpyxl import Workbook

# File to store expense data
Expense_file = "expense_data.json"

# Initialize expense data if the file doesn't exist
if not os.path.exists(Expense_file):
    with open(Expense_file, 'w') as f:
        json.dump({}, f)

# Load expense data from the file
with open(Expense_file, 'r') as f:
    expenses = json.load(f)

# Function to prompt the user for expense input
def expense_input():
    while True:
        try:
            amount = float(input("Enter the amount spent (in Rs.): Rs. "))
            description = input("Enter a brief description: ")
            category = input("Enter the category for the expense: ").lower()

            if category.strip().lower() == 'exit':
                print("Category name cannot be 'exit'. Please choose another category name.")
                continue

            date_string_value = input("Enter the date of the expense (DD/MM/YYYY): ")
            date = datetime.strptime (date_string_value,  "%d/%m/%Y" ).strftime("%d/%m/%Y")

            if category not in expenses:
                expenses[category] = []

            expenses[category].append({ "amount":amount,  "description":  description,  "date":date})
            save_data()
            print("Expense added successfully!")
            break
        except ValueError:
            print("Invalid input. Please enter valid data.")

# Function to save expense data to file
def save_data():
    with open(Expense_file,'w') as f:
        json.dump(expenses,f,indent=4)

# Function to display expense summary by month
def expense_month():
    month = input("Enter the month to view expenses  (MM/YYYY): ")
    total_expense = 0
    print(f"\nExpense Summary for {month}:")
    for category , items in  expenses.items():
        for item in  items:
            if item[ 'date' ].endswith(month):
                print (f"{ category.capitalize()}:Rs. {item['amount']:.2f}-{item['description']} - {item['date']}")
                total_expense +=item['amount']
    print(f"Total Expense for {month}:Rs.{total_expense:.2f}")

# Function to display expense summary by category
def expense_category():
    category = input("Enter the category to view expenses: ").lower()
    total_expense = 0
    if category in expenses:
        print(f"\nExpense Summary for {category.capitalize()}:")
        for item in expenses[category]:
            print(f"Rs.{item['amount']:.2f}-{item['description']} -{item['date']}")
            total_expense += item['amount']
        print(f"Total Expense for {category.capitalize()}:Rs.{total_expense:.2f}")
    else:
        print("No expenses found in the specified category.")

# Function to display all expense summaries
def view_expense():
    total_expense = 0
    print("\nAll Expense Summary:")
    for category, items in expenses.items():
        print(f"{category.capitalize()}:")
        for item in items:
            print(f"Rs.{item['amount']:.2f} -{item['description']}- {item['date']}")
            total_expense+= item['amount']
    print (f"Total Expense: Rs.{total_expense:.2f}")

# Function to export expense data to Excel
def excel_export():
    file_name=  input ("Enter the file name to save (e.g., expenses.xlsx): ")
    wb = Workbook()
    ws = wb.active
    ws.append(["Category", "Amount (Rs.)", "Description", "Date"])
    for category, items in expenses.items():
        for item in items:
            ws.append([category, item['amount'], item['description'], item['date']])
    wb.save(file_name)
    print(f"Expense data exported to {file_name} successfully!")

# Function to delete a particular expense by category
def delete_category():
    category = input("Enter the category of the expense you want to delete: ").lower()
    if category in expenses:
        print(f"Expenses in {category.capitalize()} category:")
        for index,item in enumerate (expenses[ category]):
            print(f"{index+1}.{item['description']} -Rs. {item['amount']}- {item['date']}")
        try:
            choice = input("Enter the number of the expense you want to delete (0 to cancel): ")
            choice = int(choice)
            if 0 < choice <= len(expenses[category]):
                del expenses[category][choice - 1]
                save_data()
                print("Expense deleted successfully!")
            elif choice == 0:
                pass  # Exit the loop and return to the main menu
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    else:
        print("No expenses found in the specified category.")

# Function to delete all expenses
def expense_delete_all():
    confirm = input("Are you sure you want to delete all expenses? (yes/no): ").lower()
    if confirm == "yes":
        expenses.clear()
        save_data()
        print("All expenses deleted successfully!")
    elif confirm == "no":
        print("Operation cancelled.")
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

# Function to delete a particular expense according date
def delete_date():
    date = input("Enter the date of the expenses you want to delete (DD/MM/YYYY): ")
    for category, items in expenses.items():
        for item in items:
            if item['date'] == date:
                print(f"Category:{category.capitalize()} -Rs.{item['amount']} -{item['description']} - {item['date']}")
                try:
                    confirm = input("Delete this expense? (yes/no): ").lower()
                    if confirm == 'yes':
                        expenses[category].remove(item)
                        save_data()
                        print("Expense deleted successfully!")
                except ValueError:
                    print("Invalid input.")

# Function to delete a particular expense
def expense_delete():
    while True:
        print("\nDelete Expense Menu:")
        print("a. Delete Expense by Category")
        print("b. Delete Expense by Date")
        print("c. Delete All Expenses")
        print("d. Exit to Main Menu")

        delete_choice = input("Enter your choice: ").lower()

        if delete_choice == 'a':
            delete_category()
        elif delete_choice == 'b':
            delete_date()
        elif delete_choice == 'c':
            expense_delete_all()
        elif delete_choice == 'd':
            break
        else:
            print("Invalid choice")

# Main function to run the Expense Tracker
def main():
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expense Summary")
        print("3. Export Expense Data to Excel")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            expense_input()
        elif choice == '2':
            print("\nView Expense Summary:")
            print("a. By Month")
            print("b. By Category")
            print("c. View All Expenses")
            view_choice = input("Enter your choice: ").lower()
            if view_choice == 'a':
                expense_month()
            elif view_choice == 'b':
                expense_category()
            elif view_choice == 'c':
                view_expense()
            else:
                print("Invalid choice. Please try again.")
        elif choice == '3':
            excel_export()
        elif choice == '4':
            expense_delete()
        elif choice == '5':
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__==   "__main__" :
    main()

