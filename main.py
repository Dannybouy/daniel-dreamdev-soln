import os
# Edit the directory path to the directory containing the sales data on your local machine
directory_path = "C:/Users/danie/OneDrive/Desktop/daniel-dreamdevs-soln/test-case-1"

"""
This is the main file for the Moniepoint Analytics Software.
It contains the functions for processing the transaction files and analyzing the data.
"""

def prepare_file(one_line):
    split_line = one_line.split(",")
    salesStaffId = split_line[0]
    transaction_time = split_line[1]
    products_sold = split_line[2]
    sale_amount = split_line[3]

    # Remove the square brackets from the products_sold string
    products_sold = products_sold.strip("[]")

    # split the products_sold string into a list of products
    products_sold_list = products_sold.split("|")

    # split the products_sold_list into a list of products and quantities
    products_sold_list = [product.split(":") for product in products_sold_list]

    # create a dictionary of products and quantities
    products_sold_dict = {product[0]: int(product[1]) for product in products_sold_list}

    return salesStaffId, transaction_time, products_sold_dict, sale_amount


def combine_transaction_products(transaction_file):
    transaction_daily_products = {}

    for transaction in transaction_file:
        if transaction.strip():
            # Unpack the tuple to get just the products dictionary
            _, _, products_dict, _ = prepare_file(transaction)

            # Combine quantities for each product across transactions
            for product_id, quantity in products_dict.items():
                if product_id in transaction_daily_products:
                    transaction_daily_products[product_id] += quantity
                else:
                    transaction_daily_products[product_id] = quantity

    return transaction_daily_products


def combine_transaction_sales_amt(transaction_file):
    transaction_daily_sales_amt = []  # list to store all sales amounts

    for transaction in transaction_file:
        if transaction.strip():
            # Unpack the tuple to get just the sale amount
            _, _, _, sale_amount = prepare_file(transaction)
            transaction_daily_sales_amt.append(float(sale_amount))  # Add amount to list

    return transaction_daily_sales_amt


def highest_sales_volume(transaction_daily_products):
    # First find the maximum quantity in the products_sold_dict
    max_quantity = max(transaction_daily_products.values())
    # Then find all products that have this quantity
    highest_sales_volumes = [
        (product_id, qty)
        for product_id, qty in transaction_daily_products.items()
        if qty == max_quantity
    ]
    return highest_sales_volumes


def combine_staff_sales(transaction_file):
    """Track sales volume per staff for the month"""
    staff_sales = {}  # {staff_id: total_quantity}

    for transaction in transaction_file:
        if transaction.strip():
            # Get staff ID and products
            staff_id, transaction_time, products_dict, _ = prepare_file(transaction)

            # Calculate total quantity for this transaction
            transaction_quantity = sum(products_dict.values())

            # Add to staff's total
            if staff_id in staff_sales:
                staff_sales[staff_id] += transaction_quantity
            else:
                staff_sales[staff_id] = transaction_quantity
    return staff_sales


def get_highest_staff(staff_sales):
    """Find staff with highest sales volume"""
    if not staff_sales:
        return None
    return max(staff_sales.items(), key=lambda x: x[1])


def process_single_file(filename):
    """Process a single transaction file and return its metrics"""
    with open(filename, "r") as transaction_file:
        # Get daily products and sales
        transaction_daily_products = combine_transaction_products(transaction_file)

        transaction_file.seek(0)
        transaction_daily_sales_amt = combine_transaction_sales_amt(transaction_file)

        transaction_file.seek(0)
        staff_sales = combine_staff_sales(transaction_file)

        # Calculate metrics
        Highest_sales_volume = highest_sales_volume(transaction_daily_products)
        Highest_sale_value = max(transaction_daily_sales_amt)
        Most_sold_product_ID_by_volume = Highest_sales_volume[0][0]
        highest_staff = get_highest_staff(staff_sales)

        # Get month from first transaction in file
        first_line = next(open(filename))
        _, transaction_time, _, _ = prepare_file(first_line)
        month = transaction_time[:7]  # Gets YYYY-MM from transaction time

        return {
            "Highest_sales_volume": Highest_sales_volume,
            "Highest_sale_value": Highest_sale_value,
            "Most_sold_product_ID_by_volume": Most_sold_product_ID_by_volume,
            "month": month,
            "staff_sales": staff_sales,
            "highest_staff": highest_staff,
        }


def analyze_transactions(files_dict):
    all_metrics = {}
    monthly_staff_sales = {}

    for date, filepath in files_dict.items():
        metrics = process_single_file(filepath)
        all_metrics[date] = metrics

        # Aggregate staff sales by month
        month = metrics["month"]
        if month not in monthly_staff_sales:
            monthly_staff_sales[month] = {}

        for staff_id, quantity in metrics["staff_sales"].items():
            if staff_id in monthly_staff_sales[month]:
                monthly_staff_sales[month][staff_id] += quantity
            else:
                monthly_staff_sales[month][staff_id] = quantity

    # Find highest staff for each month
    monthly_highest_staff = {
        month: get_highest_staff(staff_sales)
        for month, staff_sales in monthly_staff_sales.items()
    }

    return all_metrics, monthly_highest_staff


def get_transaction_files(directory_path):
    # Create dictionary of transaction files from directory
    transaction_files = {}

    # Get all files in directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  # Only process .txt files
            filepath = os.path.join(directory_path, filename)

            # Extract date from filename or file content
            date = filename.split(".")[0]  # Remove .txt extension
            transaction_files[date] = filepath

    return transaction_files


def display_menu():
    print("\nWelcome to Daniel's DreamDevs-Hackathon Moniepoint Analytics Software Menu, Let's help you get insights into your business. Pls pick an option from the list below:")
    print("1. Highest sales volume in a day")
    print("2. Highest sales value in a day")
    print("3. Most sold product ID by volume")
    print("4. Highest sales staff ID for each month")
    print("5. Highest hour of the day by average transaction volume")
    print("6. Exit")
    return input("Enter your choice (1-6): ")


def run_analytics():
    transaction_files = get_transaction_files(directory_path)
    metrics, monthly_highest_staff = analyze_transactions(transaction_files)

    while True:
        choice = display_menu()

        if choice == "1":
            for date, daily_metrics in metrics.items():
                print(f"\nDate: {date}")
                print(f"Highest sales volume: {daily_metrics['Highest_sales_volume']}")

        elif choice == "2":
            for date, daily_metrics in metrics.items():
                print(f"\nDate: {date}")
                print(f"Highest sale value: {daily_metrics['Highest_sale_value']}")

        elif choice == "3":
            for date, daily_metrics in metrics.items():
                print(f"\nDate: {date}")
                print(
                    f"Most sold product ID: {daily_metrics['Most_sold_product_ID_by_volume']}"
                )

        elif choice == "4":
            print("\nHighest sales staff ID for each month:")
            for month, (staff_id, quantity) in monthly_highest_staff.items():
                print(f"{month}: Staff ID {staff_id} with {quantity} items sold")

        elif choice == "5":
            print("\nHighest hour of the day by average transaction volume:")
            for date, daily_metrics in metrics.items():
                print(f"\nDate: {date}")
                print("There was not enough time to implement this feature :(")

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


# Replace the existing printing code with:
if __name__ == "__main__":
    run_analytics()
