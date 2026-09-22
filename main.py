import os, json
import random

spacesItem = 40 * " "
spacesInput = '\n' + 20 * " "
red = '\033[0;31m'
reset = '\033[0;0m'
print('\033[?25l')

with open('items.json', 'w', encoding='utf-16') as f:
    try:
        data = json.load(f)
    except:
        f.write('[]')
        
def help():
    banner('help')
    print(f"""{35 * ' '} Need help? Contact me at
{30 * " "}GitHub: https://github.com/kernixDev/
{30 * " "}Email: kernix@proton.me""")
    input(f"{spacesInput}{red}Press enter to go back...{reset}")

def encrypt(password):
    scrambled = []
    alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789!/;.:?,*$^)([]#~")
    random.shuffle(alphabet)
    shuffled = "".join(alphabet)

    shift = random.randint(1, 100)

    for char in password:
        index = alphabet.index(char)
        char = alphabet[(index - shift) % len(alphabet)]
        scrambled.append(char)

    publicKey = f'{shuffled}|{shift}'
    password = f'{"".join(scrambled)}|{publicKey}'
    return password

def decrypt(password):
    password, alphabet, shift = password.split('|')
    decryptedPw = []
    shift = int(shift)

    for char in password:
        index = alphabet.index(char)
        char = alphabet[(index + shift) % len(alphabet)]
        decryptedPw.append(char)
    
    return "".join(decryptedPw)

def banner(text):
    os.system('cls' if os.name=='nt' else 'clear')
    spaces = 27
    print(f"""{red}
                        ______ _    _______  ___  ___                                  
                        | ___ \ |  | |  _  \ |  \/  |                                  
                        | |_/ / |  | | | | | | .  . | __ _ _ __   __ _  __ _  ___ _ __ 
                        |  __/| |/\| | | | | | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
                        | |   \  /\  / |/ /  | |  | | (_| | | | | (_| | (_| |  __/ |   
                        \_|    \/  \/|___/   \_|  |_/\__,_|_| |_|\__,_|\__, |\___|_|   
                                                                        __/ |          
                                            {text}{(spaces - len(text)) * ' '}|___/  {reset}
                                                                       """)

def addEntry():
    valid = False
    while not valid:
        banner('Add an entry')
        name = input('                                        Item Name: ').lower().replace(' ', '')
        username = input('                                        Username: ').lower()
        password = input('                                        Password: ')
        website = input('                                        Website: ').lower()
        if not website.startswith('http://') or not website.startswith('https://'):
            website = f'https://{website}'

        if name and username and password and website:
            valid = True
        else:
            input(f"{red}{spacesInput}Your entry isn't valid, press enter try again...{reset}")
        
        password = encrypt(password)

    inputData = {
        "name": name,
        "username": username,
        "password": password,
        "website": website
    }

    with open('items.json', 'r', errors='ignore', encoding='utf-8') as f:
        data = json.load(f)
        
    data.append(inputData)

    with open('items.json', 'w', errors='ignore', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def getEntry():
    found = False
    banner('Get an entry')
    name = input('                                        Item Name or ID: ').lower()
    with open('items.json', 'r', errors='ignore', encoding='utf-8') as f:
        data = json.load(f)

    isInteger = True
    for chars in name:
        if not chars in "0123456789":
            isInteger = False

    if not isInteger:
        for dicts in data:
            if str(name).lower() == str(dicts.get('name')).lower().replace('\n', ''):
                found = True
                banner('Here is your entry')
                for entry in dicts:
                    print(True if entry=="password" else False)
                    if entry == "password":
                        print(f"""{spacesItem}{entry}: {decrypt(dicts[entry])}""")
                    else:
                        print(f"""{spacesItem}{entry}: {dicts[entry]}""")
            if found:
                break

    else:
        banner('Here is your entry')
        for u in data[int(name) - 1]:
            if u == "password":
                print(f'{spacesItem}{u}: {decrypt(data[int(name) - 1][u])}')
            else:
                print(f'{spacesItem}{u}: {data[int(name) - 1][u]}')
            found = True

    if not found:
        banner('Your entry was not found')

    input(f'{red}{spacesItem}Press enter to go back...{reset}')

def viewEntries():
    i = 1
    banner('Here are your entries')
    with open('items.json', 'r', errors='ignore', encoding='utf-8') as f:
        data = json.load(f)
    
    for dicts in data:
        print(f'{spacesItem}{i}: {dicts['name']}')
        i += 1
    input(f'{red}{spacesInput}Press enter to go back...{reset}')

def home():
    os.system('cls' if os.name=='nt' else 'clear')
    print(f"""{red}
                        ______ _    _______  ___  ___                                  
                        | ___ \ |  | |  _  \ |  \/  |                                  
                        | |_/ / |  | | | | | | .  . | __ _ _ __   __ _  __ _  ___ _ __ 
                        |  __/| |/\| | | | | | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
                        | |   \  /\  / |/ /  | |  | | (_| | | | | (_| | (_| |  __/ |   
                        \_|    \/  \/|___/   \_|  |_/\__,_|_| |_|\__,_|\__, |\___|_|   
                                                                        __/ |          
                                            {reset}by {red}kernix                  |___/  {reset}   

                                        [1] Add an entry
                                        [2] Get an entry
                                        [3] View entries
                                        [?] Help
    """)
    userInput = input(f"                          {red}user{reset}@{red}pwdmng{reset}: ")

    match userInput:
        case '1': addEntry()
        case '2': getEntry()
        case '3': viewEntries()
        case '?': help()

while True:
    home()