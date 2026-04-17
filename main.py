from database import (
    create_tables,
    add_category,
    add_payment_method,
    get_categories,
    get_payment_methods,
    add_expense,
    list_expenses,
    get_total_expenses,
    get_expenses_by_category,
    get_expenses_by_payment_method
    
)

from database import delete_expense
from charts import plot_category_expenses


def show_categories():
    categories = get_categories()
    if not categories:
        print("No categories found.")
        return

    print("\nCategories:")
    for category in categories:
        print(f"{category[0]}. {category[1]}")


def show_payment_methods():
    methods = get_payment_methods()
    if not methods:
        print("No payment methods found.")
        return

    print("\nPayment Methods:")
    for method in methods:
        print(f"{method[0]}. {method[1]}")


def expense_add_menu():
    categories = get_categories()
    methods = get_payment_methods()

    if not categories:
        print("Please add a category first.")
        return

    if not methods:
        print("Please add a payment method first.")
        return

    try:
        amount = float(input("Enter amount: "))
        expense_date = input("Enter date (YYYY-MM-DD): ")
        description = input("Enter description: ")

        show_categories()
        category_id = int(input("Choose category ID: "))

        show_payment_methods()
        payment_id = int(input("Choose payment method ID: "))

        add_expense(amount, expense_date, description, category_id, payment_id)

    except ValueError:
        print("Invalid input. Please enter correct values.")


def expense_list_menu():
    expenses = list_expenses()

    if not expenses:
        print("No expenses found.")
        return

    print("\nExpenses:")
    print("-" * 80)
    for expense in expenses:
        print(
            f"ID: {expense[0]} | Amount: {expense[1]} | Date: {expense[2]} | "
            f"Description: {expense[3]} | Category: {expense[4]} | Payment: {expense[5]}"
        )
    print("-" * 80)


def total_expense_menu():
    total = get_total_expenses()
    print(f"\nTotal Expenses: {total:.2f} TL")


def category_report_menu():
    results = get_expenses_by_category()

    print("\nExpenses by Category:")
    for row in results:
        print(f"{row[0]}: {row[1]:.2f} TL")


def payment_report_menu():
    results = get_expenses_by_payment_method()

    print("\nExpenses by Payment Method:")
    for row in results:
        print(f"{row[0]}: {row[1]:.2f} TL")


def delete_expense_menu():
    expenses = list_expenses()

    if not expenses:
        print("No expenses to delete.")
        return

    print("\nExpenses:")
    for expense in expenses:
        print(f"{expense[0]} - {expense[3]} ({expense[1]} TL)")

    try:
        expense_id = int(input("Enter expense ID to delete: "))
        delete_expense(expense_id)
    except ValueError:
        print("Invalid input.")        


def main():
    create_tables()


    while True:
        print("\n===== PERSONAL FINANCE TRACKER =====")
        print("1. Add Category")
        print("2. Add Payment Method")
        print("3. Add Expense")
        print("4. List Expenses")
        print("5. Show Total Expenses")
        print("6. Report by Category")
        print("7. Report by Payment Method")
        print("8. Show Categories")
        print("9. Show Payment Methods")
        print("10. Delete Expense")
        print("11. Show Category Chart")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            category_name = input("Enter category name: ")
            add_category(category_name)

        elif choice == "2":
            payment_name = input("Enter payment method name: ")
            add_payment_method(payment_name)

        elif choice == "3":
            expense_add_menu()

        elif choice == "4":
            expense_list_menu()

        elif choice == "5":
            total_expense_menu()

        elif choice == "6":
            category_report_menu()

        elif choice == "7":
            payment_report_menu()

        elif choice == "8":
            show_categories()

        elif choice == "9":
            show_payment_methods()

        elif choice == "10":
            delete_expense_menu()    

        elif choice == "11":
            plot_category_expenses()
        elif choice == "0":
            print("Exiting program...")

            
            break

        else:
            print("Invalid option. Please try again.")
        
if __name__ == "__main__":

    main()
