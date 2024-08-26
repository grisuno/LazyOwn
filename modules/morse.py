import os
MORSE_CODE = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
}

# Special characters dictionary
SPECIAL_CHARACTERS = {
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "'": ".----.",
    "!": "-.-.--",
    "/": "-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    "&": ".-...",
    ":": "---...",
    ";": "-.-.-.",
    "=": "-...-",
    "+": ".-.-.",
    "-": "-....-",
    "_": "..--.-",
    '"': ".-..-.",
    "$": "...-..-",
    "@": ".--.-.",
}

# Reverse Morse code dictionary
MORSE_CODE_REV = {}


def reverseMorseCode():
    for key, value in MORSE_CODE.items():
        MORSE_CODE_REV[value] = key


# Function to convert text to Morse code
def textToMorse(text):
    text = text.upper()
    morseCode = ""
    for char in text:
        if char == " ":
            morseCode += "/"
        elif char in MORSE_CODE:
            morseCode += MORSE_CODE[char] + " "
        elif char in SPECIAL_CHARACTERS:
            morseCode += SPECIAL_CHARACTERS[char] + " "
    return morseCode.strip()


# Function to convert Morse code to text
def morseToText(morseCode):
    reverseMorseCode()
    words = morseCode.split("/")
    text = ""
    for word in words:
        word = word.strip()
        if word != "":
            letters = word.split(" ")
            for letter in letters:
                if letter in MORSE_CODE_REV:
                    text += MORSE_CODE_REV[letter]
                else:
                    for key, value in SPECIAL_CHARACTERS.items():
                        if value == letter:
                            text += key
                            break
            text += " "
    return text.strip()


# Main driver function
if __name__ == "__main__":
    while True:
        # Get user's choice
        os.system("clear")
        value = int(
            input(
                """\n*********************** Welcome to Morse Code Convertor 🔄️ ***********************\n
            \t\tEnter 1️⃣  to convert text to Morse code
            \t\tEnter 2️⃣  to convert Morse code to text
            \t\tEnter 0️⃣  to exit the program\n
            \nEnter your choice: """
            )
        )

        while value != 1 and value != 2 and value != 0:
            os.system("clear")
            print(
                """\n*********************** Welcome to Morse Code Convertor 🔄️ ***********************\n
            \t\tEnter 1️⃣  to convert text to Morse code
            \t\tEnter 2️⃣  to convert Morse code to text
            \t\tEnter 0️⃣  to exit the program\n"""
            )
            print(
                "\n**************** 🚫 Invalid choice. Please enter either 0️⃣ , 1️⃣  or 2️⃣ . ****************\n"
            )
            value = int(input("\nEnter the currect choice: "))

        if value == 0:
            os.system("clear")
            print(
                "\n******************* Thanks for using The Morse Code Convertor 🔄️ Program 👋 *******************\n\n"
            )
            exit(0)

        elif value == 1:
            os.system("clear")
            print(
                "\n*********************** Welcome to Morse Code Convertor 🔄️ ***********************\n"
            )
            print("\nWelcome to the Text ➡️ Morse Code\n")
            text = input("\nEnter the text: ")
            morseCode = textToMorse(text)
            os.system("clear")
            print(f"\n✔️  Morse Code of {text} is: {morseCode}")
            input("\n\nPress 'Enter Key' to continue !\n\n")

        elif value == 2:
            os.system("clear")
            print(
                "\n*********************** Welcome to Morse Code Convertor ***********************\n"
            )
            print("\nWelcome to the Morse Code ➡️ Text\n")
            morseCode = input("\nEnter the Morse code: ")
            text = morseToText(morseCode)
            os.system("clear")
            print(f"\n✔️  Text of {morseCode} is: {text}")
            input("\n\nPress 'Enter Key' to continue !\n\n")