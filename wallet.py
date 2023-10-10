import pickle
import sys

# Transaction details
# Wallet_name
# Action type (Withdraw or deposit)
# Amount (In the least possible currency ie. paise for ruppee so only integers appear)

CONFOPT = ["Y", "N"]

wallets = {}
def passwd_set():
    print("\nSetting Password")
    new_passwd = input("Enter password: ")
    passwd_confirm = input("Enter password again to confirm:")
    if new_passwd != passwd_confirm:
        return False
    file=open("passwd", "wb")
    pickle.dump(new_passwd,file)
    file.close()
    print("Password set successfully\n")
    return True

def passwd_check():
    # Getting password from saved file
    try:
        file = open("passwd", "rb")
        actual_passwd = pickle.load(file)
        file.close()
        if type(actual_passwd) != type(""):
            print("Password corrupted")
    except:
        print("No password set...")
        while True:
            if not passwd_set():
                continue
            return True
        
    # Checking password
    passwd = input("Enter password: ")
    print()
    return passwd == actual_passwd

def create_wallet():
    wallet_name = input("\nCreating new wallet\nEnter wallet name: ")
    wallets[wallet_name] = 0
    save_wallet()

# Load the wallets from file wallets.dat and append them to wallets, with the amounts associated with it
def load_wallets():
    try:
        f = open("wallets.dat", "rb")
        while True:
            l = pickle.load(f)
            wallets[l[0]] = l[1]
    except FileNotFoundError:
        print("No wallets found")
        create_wallet()
        return
    except EOFError:
        if len(wallets) == 0:
            print("No wallets found")
            create_wallet()
        f.close()

def save_wallet():
    f = open("wallets.dat", "wb")
    for i in wallets:
        pickle.dump((i, wallets[i]), f)
            
def deposit(wallet_name):
    f = open("transaction.dat", "ab")
    try:
        amount = float(input("Enter amount (₹): "))
    except ValueError:
        print("Invalid input")
        return
    if amount < 0:
        print("Invalid amount")
        return
    data = (wallet_name, amount, True)
    pickle.dump(data, f)
    wallets[wallet_name] += amount
    save_wallet()
    print(f"Successfully deposited {amount}₹")
    f.close()

def withdraw(wallet_name):
    f = open("transaction.dat", "ab")
    try:
        amount = float(input("Enter amount (₹): "))
    except ValueError:
        print("Invalid input")
        return
    if amount > wallets[wallet_name] or amount < 0: # Checking balance
        print(f"Withdawing {amount} not feasible")
        return
    if amount < 0:
        print("Invalid amount")
    data = (wallet_name, amount, False)
    pickle.dump(data, f)
    wallets[wallet_name] -= amount
    save_wallet()
    print(f"Successfully withdrawn {amount}₹")
    f.close()

def delete_wallet(wallet_name):
    if len(wallets) <= 1:
        print("You can't delete the only wallet left")
        return
    while True:
        conf = input(f"Are you sure you want to delete {wallet_name}? (Y/n): ").upper()
        if conf in CONFOPT:
            break
        print("Invalid option")
    if conf == "N":
            return
    while True:
        w = wallet_select("Transfer money to:", wallet_name)
        if w == wallet_name:
            print("Invalid Input")
            continue
        break
    wallets[w] += wallets[wallet_name]
    del wallets[wallet_name]
    save_wallet()

def menu():
    print("""
┌───────────────────────────────────┐
│                                   │
│  Menu                             │
│  ====                             │
│                                   │
│  1. Select wallet                 │
│  2. Create wallet                 │
│  3. Show transactions             │
│  4. Total wealth                  │
│  5. Percentage across wallets     │
│  6. Change password               │
│  7. Exit                          │
│                                   │
└───────────────────────────────────┘
""")
    opt = int(input("➜ "))
    if opt == 1:
        w = wallet_select("Select wallet:")
        while True:
            if w in wallets:
                if wallet_menu(w): break
            else:
                return
    elif opt == 2: create_wallet()
    elif opt == 3: show_transactions()
    elif opt == 4: total_wealth()
    elif opt == 5: percentage_wealth()
    elif opt == 6: passwd_set()
    elif opt == 7: return True

def percentage_wealth():
    total = 0
    for i in wallets:
        total += wallets[i]
    if total == 0:
        print("\nPlease add some money before this feature can be used.")
        return
    m = 19
    t = []
    for i in wallets:
        m = len(i) if  len(i) > m else m
        t.append(i)
    m+=6
    print("\n┌──", "─"*(m), "──┐", sep="")
    print("│  Wealth Distribution:", " "*(m-20), "  │", sep="")
    for i in range(len(t)):
        percen = int((wallets[t[i]]/total)*100)
        x = len(str(percen))
        print(f"│  {i+1}. {t[i]}: {percen}%", " "*(m-(len(t[i])+6+x)), "  │", sep="")
    print("└──", "─"*(m), "──┘", sep="")

def show_transactions(wallet_name = ""):
    try:
        f = open("transaction.dat", "rb")
        c = 1
        print()
        while True:
            l = pickle.load(f)
            if wallet_name == "":
                a = "Deposit:  " if l[2] else "Withdraw: "
                print(f"{c}. {a}: {l[1]}")
            elif wallet_name == l[0]:
                a = "Deposit: " if l[2] else "Withdraw: "
                print(f"{c}. {a}: {l[1]}")
            c+=1
    except EOFError:
        f.close()
    except FileNotFoundError:
        print("No transactions...")

def total_wealth():
    total = 0
    for i in wallets:
        total += wallets[i]
    print(f"Total wealth: {total}")

def wallet_select(text, hide = ""):
    m = 14
    t = []
    for i in wallets:
        m = len(i) if  len(i) > m else m
        t.append(i)
        m+=3
    print("\n┌──", "─"*(m), "──┐", sep="")
    print(f"│  {text}", " "*(m-len(text)), "  │", sep="")
    for i in range(len(t)):
        if t[i] == hide: continue
        print(f"│  {i+1}. {t[i]}", " "*(m-(len(t[i])+3)), "  │", sep="")
    print("└──", "─"*(m), "──┘", sep="")
    while True:
        try:
            opt = int(input("➜ "))
        except ValueError:
            print("Invalid input")
            continue
        if 0 >= opt or opt > len(wallets):
            print("Invalid input")
            continue
        break
    return t[opt-1]
            

def wallet_menu(wallet_name):
    print(f"""
Wallet: {wallet_name}
Balance: {wallets[wallet_name]}₹
┌──────────────────────────┐
│                          │
│  Menu                    │
│  ====                    │
│                          │
│  1. Add money            │
│  2. Take money           │
│  3. Show transactions    │
│  4. Delete wallet        │
│  5. Back                 │
│                          │
└──────────────────────────┘
""")
    while True:
        try:
            opt = int(input("➜ "))
        except ValueError:
            print("Invalid input")
            continue
        break
    if opt == 1: deposit(wallet_name)
    elif opt == 2: withdraw(wallet_name)
    elif opt == 3: show_transactions(wallet_name)
    elif opt == 4: delete_wallet(wallet_name)
    elif opt == 5: return True
    
if __name__ == "__main__":
    if not passwd_check():
        print("Wait a minute.... who are you?")
        sys.exit(1)
    print("Welcome Mr Stark")
    load_wallets()
    while True:
        if menu(): break
