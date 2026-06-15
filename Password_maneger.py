# Imports-------------
from cryptography.fernet import Fernet
from colorama import Fore, Style, init
import time
import bcrypt
import json
import os
import subprocess
import sys
import pyperclip

# Initialize colorama
init(autoreset=True)

# ==============================
# PATH CONSTANTS
# ==============================

BASE_DIR = "Password_Manegar"
KEY_FILE = os.path.join(BASE_DIR, "secret.key")
PIN_FILE = os.path.join(BASE_DIR, "PWord_maneg.key")
DATA_FILE = os.path.join(BASE_DIR, "SAVE_PASSWORD.json")

# Create folder automatically
os.makedirs(BASE_DIR, exist_ok=True)

# ==============================
# INSTALL MISSING MODULES
# ==============================

def install(package):
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", package]
    )

try:
    from cryptography.fernet import Fernet
    import bcrypt
    from colorama import Fore, Style, init

except ImportError:

    print("Installing missing dependencies...")

    install("cryptography")
    install("bcrypt")
    install("colorama")

    print("Restart the program.")
    exit()

# ==============================
# UI FUNCTIONS
# ==============================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def loading():
    print(Fore.CYAN + "\nLoading", end="")

    for i in range(3):
        time.sleep(0.5)
        print(".", end="")

    print("\n")

def banner():
    clear()
    print(Fore.GREEN + r"""
██████╗  █████╗ ███████╗███████╗
██╔══██╗██╔══██╗██╔════╝██╔════╝
██████╔╝███████║███████╗███████╗
██╔═══╝ ██╔══██║╚════██║╚════██║
██║     ██║  ██║███████║███████║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝

        PASSWORD MANAGER 🔐
""")

# ==============================
# KEY INITIALIZATION
# ==============================

if not os.path.exists(KEY_FILE):

    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as f:
        f.write(key)

else:

    with open(KEY_FILE, "rb") as f:
        key = f.read()

cipher = Fernet(key)

# ==============================
# PIN SYSTEM
# ==============================

def pin() -> bool:

    # Create master password
    if not os.path.exists(PIN_FILE):

        print(Fore.YELLOW + "Create Your Master Password 🔐\n")

        maneg_key = str(input("Create Password: "))

        hashed = bcrypt.hashpw(
            maneg_key.encode(),
            bcrypt.gensalt()
        )

        with open(PIN_FILE, "wb") as f:
            f.write(hashed)

        print(Fore.GREEN + "\nPassword Saved Successfully ✅")
        print(Fore.CYAN + "Restart the Program.\n")

        return False

    # Login
    with open(PIN_FILE, "rb") as f:
        read_key = f.read()

    for i in range(3):

        ask_pin = str(input(
            Fore.YELLOW + "🔐 Enter Master Password --> "
        ))

        if bcrypt.checkpw(
            ask_pin.encode(),
            read_key
        ):

            print(Fore.GREEN + "\n✅ Login Successful!\n")

            loading()

            return True

        else:

            print(
                Fore.RED +
                f"❌ Wrong Password! Attempts Left: {2-i}\n"
            )

    print(Fore.RED + "🚫 Too Many Attempts.\n")

    return False

# ==============================
# JSON FUNCTIONS
# ==============================

def load_data():

    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as f:

        try:
            return json.load(f)

        except json.JSONDecodeError:
            return {}

def save_data(data):

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ==============================
# SAVE PASSWORD
# ==============================

def P_save():

    clear()

    print(Fore.CYAN + "\n=== SAVE PASSWORD ===\n")

    site_name = input("Site/File Name ('e' to exit): ")

    if site_name.lower() == "e":
        return

    password = str(input("Password: "))

    encrypted = cipher.encrypt(
        password.encode()
    ).decode()

    data = load_data()

    data[site_name] = encrypted

    save_data(data)

    print(
        Fore.GREEN +
        "\n---- Saved Successfully ✅ ----\n"
    )

# ==============================
# VIEW PASSWORD
# ==============================

def P_view():

    clear()

    data = load_data()

    if not data:

        print(Fore.RED + "No Passwords Saved Yet.\n")

        return

    print(Fore.CYAN + "\n=== SAVED PASSWORDS ===\n")

    for name in data:
        print(Fore.YELLOW + f"-> {name}")

    val = input(
        Fore.CYAN +
        "\nEnter Name to View ('e' to exit): "
    )

    if val.lower() == "e":
        return

    if val in data:

        decrypted = cipher.decrypt(
            data[val].encode()
        ).decode()

        print(
            Fore.GREEN +
            f"\n🔑 Password for {val}: {decrypted}\n"
        )
        
        try :
            inp_for_copy = int(input("Press (1) to copy name.\nPress (2) to copy Password\nPress (0) to Exit.\n-->"))

            if 0 == inp_for_copy:
                pass
            elif 1 == inp_for_copy:
                pyperclip.copy(val)
            elif 2 == inp_for_copy:
                pyperclip.copy(decrypted)
            else:
                print(f"({inp_for_copy}) didn't target any process/function...")
        except Exception as e : print(e)

    else:

        print(Fore.RED + "\nItem Not Found.\n")

# ==============================
# DELETE PASSWORD
# ==============================

def P_delet():

    clear()

    data = load_data()

    if not data:

        print(Fore.RED + "No Passwords Saved Yet.\n")

        return

    print(Fore.CYAN + "\n=== DELETE PASSWORD ===\n")

    for name in data:
        print(Fore.YELLOW + f"-> {name}")

    file_del = input(
        "\nType Name to Delete ('e' to exit): "
    )

    if file_del.lower() == "e":
        return

    if data.pop(file_del, None):

        save_data(data)

        print(Fore.GREEN + "\nDeleted Successfully ✅\n")

    else:

        print(Fore.RED + "\nItem Not Found.\n")

# ==============================
# RENAME PASSWORD
# ==============================

def P_Reanme():

    clear()

    data = load_data()

    if not data:

        print(Fore.RED + "No Passwords Saved Yet.\n")

        return

    print(Fore.CYAN + "\n=== RENAME PASSWORD ===\n")

    for name in data:
        print(Fore.YELLOW + f"-> {name}")

    old_name = input(
        "\nType Name to Rename ('e' to exit): "
    )

    if old_name.lower() == "e":
        return

    if old_name in data:

        del data[old_name]

        new_name = input("New Site Name: ")

        new_pass = str(input("New Password: "))

        encrypted = cipher.encrypt(
            new_pass.encode()
        ).decode()

        data[new_name] = encrypted

        save_data(data)

        print(
            Fore.GREEN +
            "\nRenamed Successfully ✅\n"
        )

    else:

        print(Fore.RED + "\nItem Not Found.\n")

# ==============================
# MENU
# ==============================

def menu_bar():

    while True:

        clear()

        print(Fore.CYAN + """
╔══════════════════════════════╗
║      🔐PASSWORD MANAGER✅   ║
╠══════════════════════════════╣
║ 1. Save Password             ║
║ 2. View Password             ║
║ 3. Delete Password           ║
║ 4. Rename Password           ║
║ 5. Exit                      ║
╚══════════════════════════════╝
""")

        choice = input(
            Fore.YELLOW + "Enter Choice ➜ "
        )

        if choice == '1':

            P_save()

        elif choice == '2':

            P_view()

        elif choice == '3':

            P_delet()

        elif choice == '4':

            P_Reanme()

        elif choice == '5':

            print(Fore.RED + "\nExiting Program...\n")

            time.sleep(1)

            break

        else:

            print(Fore.RED + "\nInvalid Option ❌\n")

            time.sleep(1)

        input(Fore.CYAN + "\nPress Enter To Continue...")

# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    banner()
    if pin():
        menu_bar()
        