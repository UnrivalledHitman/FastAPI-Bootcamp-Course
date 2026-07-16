"""
Write a Python program that can do the following:
1.You have $50
2. You buy an item that is $15, that has a 3% tax
3. Using the print()  Print how much money you have left, after purchasing the item.
"""

# SourceCode

initial_money = 50
bought_item_price = 15
tax_percent = 3

item_price = 15 * 1.03
money_left = initial_money - item_price

print(f"Initial money: {initial_money}")
print(f"Item price with tax: {item_price:.2f}")
print(f"Money left: {money_left}")
