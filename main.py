from colorama import Fore, init
from data import *
status = True

# initialize colorama
init(autoreset=True)

def show_report(data, collection):
  for key in data:
    if key in ["milk", "water"]:
      unit = "ml"
      print(f"{Fore.GREEN}{key}: {data[key]} {unit}")
    else:
      unit = "gms"
      print(f"{Fore.GREEN}{key}: {data[key]} {unit}")
  print(f"{Fore.GREEN}Money: Rs {collection}")

def check_resources(beverage_name):
  if beverage_name not in MENU:
    print(f"{Fore.RED}Sorry! {beverage_name} is not on the menu.")
    return False

  drink = MENU[beverage_name]
  ingredients = drink["ingredients"]

  if "milk" in ingredients:
    if resources["milk"] < drink["ingredients"]["milk"]:
      print(f"{Fore.RED}Sorry there is not enough milk.")
      return False

  if resources["water"] < drink["ingredients"]["water"]:
      print(f"{Fore.RED}Sorry there is not enough water.")
      return False
  elif resources["coffee"] < drink["ingredients"]["coffee"]:
      print(f"{Fore.RED}Sorry there is not enough coffee.")
      return False

  return True

def check_affordability(amount, drink):
  if drink["cost"] > amount:
    return False

  return True

def refill(m, w, c):
  resources["milk"] = resources["milk"] + m
  resources["water"] = resources["water"] + w
  resources["coffee"] = resources["coffee"] + c
  print(f"{Fore.GREEN}Refilling successful!")

def make_coffee(c):
  for key in c["ingredients"]:
    resources[key] = resources[key] - c["ingredients"][key]

capital = 1000
total_collection = capital
print(f"{Fore.CYAN}Welcome to Coffee Mania!")
while status:
  choice = input(f"{Fore.YELLOW}What would you like? \n1 for ESPRESSO (Rs {MENU["espresso"]["cost"]}) \n2 for LATTE (Rs {MENU["latte"]["cost"]}) \n3 for CAPPUCCINO (Rs {MENU["cappuccino"]["cost"]}) \n{Fore.MAGENTA}Your Choice: ").strip()

  if choice == "1":
    choice = 'espresso'
  elif choice == "2":
    choice = 'latte'
  elif choice == "3":
    choice = 'cappuccino'

  if choice == 'off':
    status = False
    continue

  if choice == 'refill':
    print(f"{Fore.CYAN}Milk price: Rs {MILK}/1000 ml")
    milk = int(input(f"{Fore.YELLOW}How much milk (ml) to refill? "))
    print(f"{Fore.CYAN}Water price: Rs {WATER} ml")
    water = int(input(f"{Fore.YELLOW}How much water (ml) to refill? "))
    print(f"{Fore.CYAN}Coffee price: Rs {COFFEE} gms")
    coffee = int(input(f"{Fore.YELLOW}How much coffee (gms) to refill? "))

    refill_cost = milk * MILK + water * WATER + coffee * COFFEE

    if refill_cost > total_collection:
      print(f"{Fore.RED}Sorry! You don't have enough balance.")
      continue

    total_collection -= refill_cost

    refill(milk, water, coffee)
    print(f"{Fore.GREEN}Remaining balance: Rs {total_collection}")
    continue

  if choice == 'report':
    show_report(resources, total_collection)
    continue

  if check_resources(choice) == False:
    continue

  selected_drink = MENU[choice]
  print(f"{Fore.CYAN}Please insert coins...")
  five_hundreds = int(input(f"{Fore.MAGENTA}How many 500s notes? "))
  hundreds = int(input(f"{Fore.MAGENTA}How many 100s notes? "))
  fiftys = int(input(f"{Fore.MAGENTA}How many 50s notes? "))
  twentys = int(input(f"{Fore.MAGENTA}How many 20s notes? "))
  tens = int(input(f"{Fore.MAGENTA}How many 10s notes? "))
  amt = five_hundreds * FIVE_HUNDRED + hundreds * HUNDRED + fiftys * FIFTY + twentys * TWENTY + tens * TEN

  afford_drink = check_affordability(amt, selected_drink)

  if afford_drink == False:
    print(f"{Fore.RED}Sorry that's not enough money. Money refunded")
    continue

  if afford_drink:
    total_collection += selected_drink["cost"]
    if amt > selected_drink["cost"]:
      change = round(amt - selected_drink["cost"], 2)
      print(f"{Fore.BLUE}Here is Rs {change} in change.")
    make_coffee(selected_drink)
    print(f"{Fore.CYAN}Enjoy your {choice}!")

