import json
def save_data():
    data = {
        "resources": resources,
        "fellows": fellows,
        "borrow_records": borrow_records
    }

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

def load_data():
    global resources, fellows, borrow_records

    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        resources = data["resources"]
        fellows = data["fellows"]
        borrow_records = data["borrow_records"]

    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass        
resources = [
    {
        "id": "R001",
        "name": "Laptop",
        "category": "Electronics",
        "total": 10,
        "available": 10
    },
    {
        "id": "R002",
        "name": "Keyboard",
        "category": "Accessories",
        "total": 5,
        "available": 5
    },
    {
        "id": "R003",
        "name": "Headset",
        "category": "Accessories",
        "total": 3,
        "available": 3
    }
]

fellows = {
    "F001": "Ada",
    "F002": "John",
    "F003": "Grace"
}

borrow_records = []

{
    "id": "R001",
    "name": "Laptop",
    "category": "Electronics",
    "total": 10,
    "available": 10
}

fellows = {
    "F001": "Ada",
    "F002": "John",
    "F003": "Grace"
}

{
    "fellow_id": "F001",
    "resource_id": "R001",
    "quantity": 2
}

def find_resource(resource_id):
    for resource in resources:
        if resource["id"].upper() == resource_id.upper():
            return resource

    return None

def add_resource(resource_id, name, category, total):
    if find_resource(resource_id) is not None:
        print("Error: Resource ID already exists.")
        return False

    if not resource_id.strip():
        print("Error: Resource ID cannot be empty.")
        return False

    if not name.strip():
        print("Error: Resource name cannot be empty.")
        return False

    if not category.strip():
        print("Error: Category cannot be empty.")
        return False

    if not isinstance(total, int) or total <= 0:
        print("Error: Total units must be a positive integer.")
        return False

    resources.append({
        "id": resource_id.upper(),
        "name": name,
        "category": category,
        "total": total,
        "available": total
    })

    print(f"Resource '{name}' added successfully.")
    return True

def list_resources():
    if not resources:
        print("No resources available.")
        return

    print("\n--- Resource Inventory ---")

    for resource in resources:
        borrowed = resource["total"] - resource["available"]

        print(
            f'{resource["id"]} | '
            f'{resource["name"]} | '
            f'{resource["category"]} | '
            f'Total: {resource["total"]} | '
            f'Available: {resource["available"]} | '
            f'Borrowed: {borrowed}'
        )

def get_positive_integer(prompt):
    while True:
        value = input(prompt).strip()

        try:
            number = int(value)

            if number <= 0:
                print("Error: Quantity must be greater than zero.")
                continue

            return number

        except ValueError:
            print("Error: Please enter a valid positive integer.")

def borrow_resource(fellow_id, resource_id, quantity):
    fellow_id = fellow_id.upper()
    resource_id = resource_id.upper()

    if fellow_id not in fellows:
        print("Error: Fellow ID does not exist.")
        return False

    resource = find_resource(resource_id)

    if resource is None:
        print("Error: Resource ID does not exist.")
        return False

    if not isinstance(quantity, int) or quantity <= 0:
        print("Error: Quantity must be a positive integer.")
        return False

    if quantity > resource["available"]:
        print(
            f'Error: Only {resource["available"]} '
            f'{resource["name"]}(s) available.'
        )
        return False

    resource["available"] -= quantity

    borrow_records.append({
        "fellow_id": fellow_id,
        "resource_id": resource_id,
        "quantity": quantity
    })

    print(
        f'{fellows[fellow_id]} successfully borrowed '
        f'{quantity} {resource["name"]}(s).'
    )

    return True

def find_borrow_record(fellow_id, resource_id):
    for record in borrow_records:
        if (
            record["fellow_id"] == fellow_id
            and record["resource_id"] == resource_id
        ):
            return record

    return None

def return_resource(fellow_id, resource_id, quantity):
    fellow_id = fellow_id.upper()
    resource_id = resource_id.upper()

    if fellow_id not in fellows:
        print("Error: Fellow ID does not exist.")
        return False

    resource = find_resource(resource_id)

    if resource is None:
        print("Error: Resource ID does not exist.")
        return False

    if not isinstance(quantity, int) or quantity <= 0:
        print("Error: Quantity must be a positive integer.")
        return False

    record = find_borrow_record(fellow_id, resource_id)

    if record is None:
        print("Error: This fellow has no loan for this resource.")
        return False

    if quantity > record["quantity"]:
        print(
            f'Error: {fellows[fellow_id]} only has '
            f'{record["quantity"]} unit(s) on loan.'
        )
        return False

    resource["available"] += quantity
    record["quantity"] -= quantity

    if record["quantity"] == 0:
        borrow_records.remove(record)

    print(
        f'{fellows[fellow_id]} successfully returned '
        f'{quantity} {resource["name"]}(s).'
    )

    return True

def search_resources(name):
    search_term = name.strip().lower()

    results = [
        resource
        for resource in resources
        if search_term in resource["name"].lower()
    ]

    if not results:
        print("No resources found.")
        return

    print("\n--- Search Results ---")

    for resource in results:
        print(
            f'{resource["id"]} | '
            f'{resource["name"]} | '
            f'{resource["category"]} | '
            f'Available: {resource["available"]}'
        )

def filter_by_category(category):
    search_category = category.strip().lower()

    results = [
        resource
        for resource in resources
        if resource["category"].lower() == search_category
    ]

    if not results:
        print("No resources found in that category.")
        return

    print("\n--- Category Results ---")

    for resource in results:
        print(
            f'{resource["id"]} | '
            f'{resource["name"]} | '
            f'{resource["category"]} | '
            f'Available: {resource["available"]}'
        )

def generate_report():
    total_units = sum(resource["total"] for resource in resources)
    available_units = sum(resource["available"] for resource in resources)
    borrowed_units = total_units - available_units

    low_stock = [
        resource
        for resource in resources
        if resource["available"] < 3
    ]

    borrowed_counts = {
        resource["id"]: resource["total"] - resource["available"]
        for resource in resources
    }

    max_borrowed = max(borrowed_counts.values(), default=0)

    most_borrowed = [
        resource
        for resource in resources
        if borrowed_counts[resource["id"]] == max_borrowed
        and max_borrowed > 0
    ]

    print("\n========== INVENTORY REPORT ==========")
    print(f"Total units: {total_units}")
    print(f"Available units: {available_units}")
    print(f"Units currently borrowed: {borrowed_units}")

    print("\nResources with fewer than 3 available units:")

    if low_stock:
        for resource in low_stock:
            print(
                f'- {resource["name"]}: '
                f'{resource["available"]} available'
            )
    else:
        print("None")

    print("\nResource(s) with most units currently borrowed:")

    if most_borrowed:
        for resource in most_borrowed:
            borrowed = borrowed_counts[resource["id"]]

            print(
                f'- {resource["name"]}: '
                f'{borrowed} borrowed'
            )
    else:
        print("None")

    print("======================================")

def display_menu():
    print("""
========== Learn2Earn Equipment System ==========

1. Add resource
2. List resources
3. Borrow resource
4. Return resource
5. Search resources
6. Filter by category
7. Generate report
8. Exit

===================================================
""")

def main():
    load_data()
    
    while True:
        display_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            resource_id = input("Resource ID: ").strip()
            name = input("Resource name: ").strip()
            category = input("Category: ").strip()
            total = get_positive_integer("Total units: ")

            add_resource(
                resource_id,
                name,
                category,
                total
            )

        elif choice == "2":
            list_resources()

        elif choice == "3":
            fellow_id = input("Fellow ID: ").strip()
            resource_id = input("Resource ID: ").strip()
            quantity = get_positive_integer("Quantity: ")

            borrow_resource(
                fellow_id,
                resource_id,
                quantity
            )

        elif choice == "4":
            fellow_id = input("Fellow ID: ").strip()
            resource_id = input("Resource ID: ").strip()
            quantity = get_positive_integer("Quantity: ")

            return_resource(
                fellow_id,
                resource_id,
                quantity
            )

        elif choice == "5":
            name = input("Search name: ").strip()
            search_resources(name)

        elif choice == "6":
            category = input("Category: ").strip()
            filter_by_category(category)

        elif choice == "7":
            generate_report()

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Error: Invalid menu option.")

if __name__ == "__main__":
    main()            