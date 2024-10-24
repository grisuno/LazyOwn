#include "DigiKeyboard.h"
void setup() {
    DigiKeyboard.delay(1000);
}

void loop() {
    DigiKeyboard.sendKeyStroke(0);
    DigiKeyboard.delay(1000);
    DigiKeyboard.sendKeyStroke(KEY_B, MOD_GUI_LEFT);
    DigiKeyboard.delay(2000);
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
    DigiKeyboard.delay(1000);
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
    DigiKeyboard.delay(1000);
    DigiKeyboard.sendKeyStroke(KEY_L, MOD_CONTROL_LEFT);
    DigiKeyboard.delay(2000);
    DigiKeyboard.print("{payload}");
    DigiKeyboard.delay(1000);
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
    DigiKeyboard.delay(1000);
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
    for (;;) {
        DigiKeyboard.delay(1000);
    }
}
