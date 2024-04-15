class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, destination_category):
        if self.withdraw(amount, f"Transfer to {destination_category.name}"):
            destination_category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def __str__(self):
        # Format the title
        title = f"{self.name.center(30, '*')}\n"
        # Format each ledger item
        items = ''
        for entry in self.ledger:
            description = entry['description'][:23].ljust(23)
            amount = f"{entry['amount']:.2f}".rjust(7)
            items += f"{description}{amount}\n"
        # Calculate total balance
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    # Calculate total spent in each category and overall total spent
    total_spent = 0
    spent_per_category = []
    
    for category in categories:
        spent = sum(-item["amount"] for item in category.ledger if item["amount"] < 0)
        spent_per_category.append(spent)
        total_spent += spent
    
    # Calculate percentage spent in each category
    percentages = [(spent / total_spent) * 100 for spent in spent_per_category]
    
    # Create the bar chart
    chart = "Percentage spent by category\n"
    for i in range(100, -10, -10):
        chart += f"{str(i).rjust(3)}| "
        for percentage in percentages:
            if percentage >= i: chart += "o  "
            else: chart += "   "
        chart += "\n"
    chart += "    " + '-' * (3 * len(categories) + 1) + "\n"
    
    # Add category names at the bottom
    max_length = max(len(category.name) for category in categories)
    for i in range(max_length):
        chart += "     "
        for category in categories:
            if i < len(category.name): chart += category.name[i] + "  "
            else: chart += "   "
        end = '\n' if i < max_length-1 else ''
        chart += end
    
    return chart

# Example usage

food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")    
food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")

food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)

print(create_spend_chart([business, food, entertainment]))