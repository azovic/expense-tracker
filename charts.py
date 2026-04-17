import matplotlib.pyplot as plt
from database import get_expenses_by_category
from charts import plot_category_expenses


def plot_category_expenses():
    data = get_expenses_by_category()

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure()
    plt.bar(categories, amounts)
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (TL)")

    plt.savefig("category_chart.png")
    plt.close()

    print("Chart saved as category_chart.png")