import os
import platform
import subprocess
import pandas as pd
import argparse
from colorama import Fore, Style, init
from tabulate import tabulate

# Initialize colorama
init(autoreset=True)

def highlight_term(text, term):
    """Highlight the search term in the given text."""
    return text.replace(term, f"{Fore.GREEN}{term}{Style.RESET_ALL}")

def search_in_parquet(term, parquet_files):
    """Search for a term in the given Parquet files and return matching rows."""
    # Read the Parquet files into DataFrames
    dataframes = [pd.read_parquet(file) for file in parquet_files]

    # Concatenate DataFrames into a single DataFrame
    df = pd.concat(dataframes, ignore_index=True)

    # Filter rows containing the search term
    result = df[df.apply(lambda row: row.astype(str).str.contains(term, case=False).any(), axis=1)]

    return result

def buscar_binarios(args):
    """Search for binaries with special permissions and generate a results CSV."""
    binarios_encontrados = set()
    
    # Detect the operating system
    sistema_operativo = platform.system()
    print(f"[+] Sistema operativo detectado: {sistema_operativo}")
    
    if sistema_operativo == 'Linux':
        print("[+] Ejecutando búsqueda de binarios con permisos especiales en Linux...")
        try:
            # Execute the find command for Linux
            result = subprocess.run(['find', '/', '-perm', '4000', '-ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout
            
            # Extract found binaries
            for line in output.split('\n'):
                if line:
                    parts = line.split()
                    if parts:
                        binario = os.path.basename(parts[-1])
                        binarios_encontrados.add(binario)
        except Exception as e:
            print(f"[-] Error ejecutando el comando find: {e}")
                
    elif sistema_operativo == 'Windows':
        print("[+] Ejecutando búsqueda de binarios con permisos especiales en Windows...")
        try:
            # PowerShell script for Windows
            powershell_script = """
            $directories = @("C:\\Windows\\System32", "C:\\", "C:\\Program Files", "C:\\Program Files (x86)")
            foreach ($dir in $directories) {
                Get-ChildItem -Path $dir -Recurse -Filter *.exe -ErrorAction SilentlyContinue | 
                ForEach-Object {
                    $acl = Get-Acl $_.FullName
                    $privileges = $acl.Access | Where-Object { $_.FileSystemRights -match "FullControl" }
                    if ($privileges) {
                        Write-Output "$($_.FullName)"
                    }
                }
            }
            """
            
            # Execute the PowerShell script
            result = subprocess.run(['powershell', '-Command', powershell_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout
            
            # Extract found binaries
            for line in output.split('\n'):
                if line:
                    binario = os.path.basename(line.strip())
                    binarios_encontrados.add(binario)
        except Exception as e:
            print(f"[-] Error ejecutando el script de PowerShell: {e}")
    
    if binarios_encontrados:
        print(f"[+] Binarios encontrados: {binarios_encontrados}")
        
        # Filter the main DataFrame with the found binaries
        df_binarios_encontrados = df1[df1['Binary'].isin(binarios_encontrados)]
        
        # Generate a CSV with details of the found binaries
        with open('csv/resultado.csv', 'w') as f:
            for binario in binarios_encontrados:
                result = search_in_parquet(binario, args.parquet_files)
                print(f"[**] Buscando resultados para '{binario}'")
                if not result.empty:
                    result_str = result.astype(str)
                    highlighted_result = result_str.applymap(lambda x: highlight_term(x, binario))
    
                    print(f"Resultados encontrados para '{binario}':")
                    print(tabulate(highlighted_result, headers='keys', tablefmt='psql', showindex=False))
                else:
                    print(f"No se encontraron resultados para '{binario}'")
                detalles = df2[df2['Binary'] == binario]
                if not detalles.empty:
                    f.write(detalles.to_csv(index=False, header=False))
                    print(f"[+] Detalles del binario '{binario}':")
                    print(detalles.to_csv(index=False, header=False))
    else:
        print("[-] No se encontraron binarios con permisos especiales.")

def ejecutar_opciones():
    """Execute options based on the found data."""
    if not os.path.exists('csv/resultado.csv'):
        print("[-] No se encontró el archivo 'resultado.csv'. Asegúrese de que la búsqueda de binarios se haya realizado correctamente.")
        return
    
    print("[+] Leyendo resultado de búsqueda de binarios...")
    df_resultado = pd.read_csv('csv/resultado.csv', header=None, names=['Binary', 'Function Name', 'Function URL', 'Description', 'Example'])
    
    for binario in df_resultado['Binary'].unique():
        print(f"[*] Binario encontrado: {binario}")
        detalles = df_resultado[df_resultado['Binary'] == binario]

        print("Opciones:")
        for i, (_, row) in enumerate(detalles.iterrows(), start=1):
            print(f"{i}. {row['Function Name']} - {row['Description']}")
        print(f"{i+1}. No hacer nada y salir")
        
        while True:
            opcion = input("Seleccione una opción: ")
            if opcion.isdigit() and 1 <= int(opcion) <= len(detalles) + 1:
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")
        
        opcion = int(opcion)
        
        if opcion <= len(detalles):
            print(f"[+] Ejecutando opción {opcion} para {binario}")
            # Execute the corresponding option
            print(f"[*] Ejemplo de ejecución:\n{detalles.iloc[opcion-1]['Example']}")
            # Add code to execute the example if necessary
        else:
            print("[+] Saliendo")
            break

if __name__ == '__main__':
    # Banner
    print("██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗")
    print("██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║")
    print("██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║")
    print("██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║")
    print("███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║")
    print("╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝")
    print(f"[*] Iniciando: LazyOwn [;,;]")

    parser = argparse.ArgumentParser(description="Buscar en archivos Parquet")
    parser.add_argument("--parquet_files", nargs='+', default=["binarios.parquet", "detalles.parquet"], help="Lista de archivos Parquet a buscar")
    args = parser.parse_args()

    # Read CSVs and create DataFrames
    df1 = pd.read_csv('csv/bin_data.csv')
    df2 = pd.read_csv('csv/bin_data_relevant.csv')

    # Save DataFrames as Parquet
    df1.to_parquet('parquets/binarios.parquet')
    df2.to_parquet('parquets/detalles.parquet')

    buscar_binarios(args)
    ejecutar_opciones()
