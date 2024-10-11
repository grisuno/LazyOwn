#include "DigiKeyboard.h"
void setup() {
}

void loop() {
    DigiKeyboard.sendKeyStroke(0);
    DigiKeyboard.delay(500);

    DigiKeyboard.sendKeyStroke(KEY_F2, MOD_ALT_LEFT);
    DigiKeyboard.delay(1000);

    DigiKeyboard.print("xterm");
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
    DigiKeyboard.delay(1000);

    DigiKeyboard.print("setxkbmap us");
    DigiKeyboard.sendKeyStroke(KEY_ENTER);

    DigiKeyboard.print("{payload}");
    DigiKeyboard.sendKeyStroke(KEY_ENTER);

    DigiKeyboard.print("setxkbmap es");
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
    DigiKeyboard.delay(1000);
    for (;;) {
        DigiKeyboard.delay(1000);
    }
}