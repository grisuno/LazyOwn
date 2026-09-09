"""Morse code conversion service with interactive driver.

Contract:
    Single self-contained module providing text to Morse code conversion,
    Morse code to text conversion, and an interactive selection driver.
    No placeholders, no simplifications, production grade input handling.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class MorseConfig:
    """Centralized configuration for the Morse module."""

    word_separator: str = "/"
    letter_separator: str = " "
    screen_reset_command: tuple[str, ...] = ("tput", "reset")
    subprocess_timeout_seconds: int = 5
    exit_choice: int = 0
    encode_choice: int = 1
    decode_choice: int = 2
    continue_prompt: str = "\n\nPress Enter to continue.\n\n"
    text_prompt: str = "\nEnter the text: "
    morse_prompt: str = "\nEnter the Morse code: "
    choice_prompt: str = "\nEnter your choice: "
    retry_prompt: str = "\nEnter the correct choice: "


CONFIG = MorseConfig()

MORSE_CODE: dict[str, str] = {
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

SPECIAL_CHARACTERS: dict[str, str] = {
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

MORSE_CODE_REV: dict[str, str] = {value: key for key, value in MORSE_CODE.items()}


def reverse_morse_code() -> dict[str, str]:
    """Build the reverse lookup table from Morse code to characters.

    Returns:
        Mapping of Morse code sequences to uppercase characters.
    """
    reverse = {value: key for key, value in MORSE_CODE.items()}
    MORSE_CODE_REV.update(reverse)
    return dict(MORSE_CODE_REV)


def text_to_morse(text: str, config: MorseConfig = CONFIG) -> str:
    """Convert plain text to Morse code.

    Args:
        text: Source text to encode.
        config: Module configuration.

    Returns:
        Morse code representation with word and letter separators.
    """
    encoded_parts: list[str] = []
    for char in text.upper():
        if char == " ":
            encoded_parts.append(config.word_separator)
        elif char in MORSE_CODE:
            encoded_parts.append(MORSE_CODE[char])
        elif char in SPECIAL_CHARACTERS:
            encoded_parts.append(SPECIAL_CHARACTERS[char])
    return config.letter_separator.join(encoded_parts).strip()


def morse_to_text(morse_code: str, config: MorseConfig = CONFIG) -> str:
    """Convert Morse code back to plain text.

    Args:
        morse_code: Morse code string using configured separators.
        config: Module configuration.

    Returns:
        Decoded uppercase text.
    """
    reverse_morse_code()
    special_reverse = {value: key for key, value in SPECIAL_CHARACTERS.items()}
    decoded_words: list[str] = []
    for word in morse_code.split(config.word_separator):
        stripped = word.strip()
        if not stripped:
            continue
        decoded_letters: list[str] = []
        for letter in stripped.split(config.letter_separator):
            if letter in MORSE_CODE_REV:
                decoded_letters.append(MORSE_CODE_REV[letter])
            elif letter in special_reverse:
                decoded_letters.append(special_reverse[letter])
        decoded_words.append("".join(decoded_letters))
    return " ".join(decoded_words).strip()


def clear_screen(config: MorseConfig = CONFIG) -> None:
    """Reset the terminal screen using a bounded subprocess call.

    Args:
        config: Module configuration.
    """
    subprocess.run(
        list(config.screen_reset_command),
        capture_output=True,
        timeout=config.subprocess_timeout_seconds,
        check=False,
    )


def read_choice(config: MorseConfig = CONFIG) -> int | None:
    """Read and validate the menu choice from standard input.

    Args:
        config: Module configuration.

    Returns:
        Valid menu choice, or None when input is not a number.
    """
    try:
        return int(input(config.choice_prompt))
    except ValueError:
        return None


def run_driver(config: MorseConfig = CONFIG) -> None:
    """Run the interactive Morse code conversion loop.

    Args:
        config: Module configuration.

    Raises:
        EOFError: Propagated when standard input closes.
    """
    valid_choices = {config.exit_choice, config.encode_choice, config.decode_choice}
    while True:
        clear_screen(config)
        print("Morse Code Converter")
        print("1: convert text to Morse code")
        print("2: convert Morse code to text")
        print("0: exit the program")
        value = read_choice(config)
        while value not in valid_choices:
            clear_screen(config)
            print("Invalid choice. Enter 0, 1 or 2.")
            try:
                value = int(input(config.retry_prompt))
            except ValueError:
                value = None
        if value == config.exit_choice:
            clear_screen(config)
            print("Thanks for using the Morse Code Converter.")
            raise SystemExit(0)
        if value == config.encode_choice:
            clear_screen(config)
            text = input(config.text_prompt)
            encoded = text_to_morse(text, config)
            clear_screen(config)
            print(f"Morse code of {text} is: {encoded}")
            input(config.continue_prompt)
        elif value == config.decode_choice:
            clear_screen(config)
            code = input(config.morse_prompt)
            decoded = morse_to_text(code, config)
            clear_screen(config)
            print(f"Text of {code} is: {decoded}")
            input(config.continue_prompt)


textToMorse = text_to_morse
morseToText = morse_to_text
reverseMorseCode = reverse_morse_code


if __name__ == "__main__":
    run_driver()
