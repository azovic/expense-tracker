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