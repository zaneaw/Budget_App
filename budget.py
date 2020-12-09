class Category:
    def __init__(self, name):
        self.ledger = []
        self.name = name
        self.total = 0

    def deposit(self, amount, description=None):
        self.total += amount
        if description == None:
            self.description = ""
        else:
            self.description = description
        self.ledger.append({"amount": amount, "description": self.description})

    def withdraw(self, amount, description=None):
        if amount > self.total:
            return False
        else:
            self.total -= amount
            if description == None:
                self.description = ""
            else:
                self.description = description
            self.ledger.append(
                {"amount": -amount, "description": self.description}
            )
            return True

    def get_balance(self):
        return self.total

    def transfer(self, amount, other_cat):
        if amount > self.total:
            return False
        else:
            self.total -= amount
            other_cat.total += amount
            print(other_cat)
            self.ledger.append(
                {
                    "amount": -amount,
                    "description": f"Transfer to {other_cat.name}",
                }
            )
            other_cat.ledger.append(
                {"amount": amount, "description": f"Transfer from {self.name}"}
            )
            return True

    def check_funds(self, amount):
        if amount > self.total:
            return False
        else:
            return True

    def __str__(self):
        title = self.name
        count = 0

        lines_list = []

        while len(title) < 30:
            title = "*" + title + "*"

        # Iterate through the list of dictionary key/value pairs
        # Grab the amount value and the description value
        for amount in self.ledger:
            amount = self.ledger[count]["amount"]
            amount = format(amount, ".2f")
            desc = self.ledger[count]["description"]
            # Set the standard length of amount to 7
            while len(amount) < 7:
                amount = " " + amount
            # Set the standard length of desc to 23
            while len(desc) < 23:
                desc += " "
            # If the length of desc is > 23, only grab the first 23
            else:
                desc = desc[:23]
            # Append the values to a new list
            lines_list.append(desc + amount)
            count += 1
        # .join the values together with a new line for each
        lines_print = "\n".join(lines_list)

        # Format the total to be 2 decimals if need be
        total = format(self.total, ".2f")
        total = f"Total: {self.total}"
        count = 0
        display = title + "\n" + lines_print + "\n" + total

        return display


def create_spend_chart(categories):
    # Variables
    title = "Percentage spent by category"
    chart = ""
    cats = []
    withdraws = []
    withdraw_percentage = []
    vertical_cats = ""
    # Iterate through list of category objects, add to 'cats' list
    for category in categories:
        cats.append(category.name)
        # Store withdrawn amount as 0 for each category
        withdrawn_amount = 0
        # Each action in the ledger of that speicific cat will be evaluated
        # and if action is less than 0, it's a withdraw, append action
        # negatively to reverse the -
        for action in category.ledger:
            if action["amount"] < 0:
                withdrawn_amount -= action["amount"]
        # Append the total amount of withdraws to the list of withdraws
        withdraws.append(withdrawn_amount)
    # Math for the percentage for each number in the range of the length of
    # the withdraws list. i.e. - 3 withdraws, ranging 1 - 2 - 3
    for number in range(len(withdraws)):
        withdraw_percentage.append(withdraws[number] / sum(withdraws) * 100)
    # For each number in the range of 100 to -10, taking 10 off each time
    # calc the amount of "o" to add to each category. i.e. - 100| 90| 80| etc
    for number in range(100, -10, -10):
        # This builds the Y-Axis of the chart
        chart += str(number).rjust(3, " ") + "|"
        # For the nums stored in withdraw_percentage
        # if the num is greater than the current number in the range,
        # it will add an "o", otherwise, it's left blank for that column
        for num in withdraw_percentage:
            if num >= number:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"
    # This builds the X-Axis of the chart based on the number of cats
    # and multiplies each - by 3
    chart += "    " + "-" * len(cats) * 3 + "-" + "\n"
    # Determine the longest category name by iterating through the
    # list of objects passed through the function
    longest = max(len(name.name) for name in categories)
    # The range of the longest is going to be the tallest column
    # i.e. - adding the most amount of rows
    for level in range(longest):
        # Add spaces to the beggining of the first column from side of page
        vertical_cats += "    "
        # For each category in the categories list
        # if the level number is less than the length of the current name
        # then the current letter is added to the row, otherwise, just add
        # space for the next vertical category logic
        for name in categories:
            if level < len(name.name):
                vertical_cats += " " + name.name[level] + " "
            else:
                vertical_cats += "   "
        vertical_cats += " \n"
    # Strip the whitespace from the right side and add back in the 2 leftover
    # spaces that are included in the example for whatever reason
    chart += vertical_cats.rstrip() + "  "
    # Finalize the string!
    display = title + "\n" + chart
    return display