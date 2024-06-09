#!/bin/bash
pip install pyinstaller
pyinstaller --onefile app.py
mv app.spec.dist app.spec
pyinstaller app.spec
