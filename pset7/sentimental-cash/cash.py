from cs50 import get_float


def get_coins(coin_value, change):
    # Determine coins and return coin count.
    num_coins = 0
    if change >= coin_value:
        running_total = change - (change % coin_value)
        num_coins = running_total / coin_value
        return num_coins


# Ask user how much change is owed
change = 0.00
while change <= 0.00:
    change = get_float("How much change is owed?")

# Determine coins, take from running total and add to coin count
total_coin_count = 0
coins = [0.25, 0.1, 0.05, 0.01]
for i in coins:
    current_coin_count = get_coins(i, change)
    if current_coin_count != None:
        change -= (i * current_coin_count)
        change = float("{:.2f}".format(change))
        total_coin_count += current_coin_count

# Return final coin count
print(int(total_coin_count))