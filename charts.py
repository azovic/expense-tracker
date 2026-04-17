import matplotlib.pyplot as plt
from database import get_expenses_by_category



def plot_category_expenses():
    data = get_expenses_by_category()

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    if all(amount == 0 for amount in amounts):
        print("No expense data to plot.")
        return


    plt.figure(figsize=(8, 5))
    plt.bar(categories, amounts)
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (TL)")

    plt.savefig("category_chart.png")
    plt.close()

    print("Chart saved as category_chart.png")

def plot_category_pie_chart():
    data = get_expenses_by_category()

    categories = [row[0] for row in data if row[1] > 0]
    amounts = [row[1] for row in data if row[1] > 0]

    if not amounts:
        print("No expense data to plot.")
        return

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%")
    plt.title("Expense Distribution by Category")

    plt.savefig("category_pie_chart.png")
    plt.close()

    print("Pie chart saved as category_pie_chart.png")    