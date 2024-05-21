import pandas as pd
import os
import subprocess
import platform

# Lee los CSVs y crea los DataFrames
df1 = pd.read_csv('bin_data.csv')
df2 = pd.read_csv('bin_data_relevant.csv')

# Guarda los DataFrames como Parquet
df1.to_parquet('binarios.parquet')
df2.to_parquet('detalles.parquet')

# Función para realizar la búsqueda y generar el CSV de salida
def buscar_binarios():
    binarios_encontrados = set()
    
    # Detecta el sistema operativo
    sistema_operativo = platform.system()
    
    if sistema_operativo == 'Linux':
        # Ejecuta el comando find para Linux
        result = subprocess.run(['find', '/', '-perm', '4000', '-ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        
        # Extrae los binarios encontrados
        for line in output.split('\n'):
            if line:
                binario = os.path.basename(line.split()[-1])
                binarios_encontrados.add(binario)
    
    elif sistema_operativo == 'Windows':
        # Script de PowerShell para Windows
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
        
        # Ejecuta el script de PowerShell
        result = subprocess.run(['powershell', '-Command', powershell_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        
        # Extrae los binarios encontrados
        for line in output.split('\n'):
            if line:
                binario = os.path.basename(line.strip())
                binarios_encontrados.add(binario)
    
    # Filtra el DataFrame principal con los binarios encontrados
    df_binarios_encontrados = df1[df1['Binary'].isin(binarios_encontrados)]
    
    # Genera un CSV con los detalles de los binarios encontrados
    with open('resultado.csv', 'w') as f:
        for binario in binarios_encontrados:
            detalles = df2[df2['Binary'] == binario]
            if not detalles.empty:
                f.write(detalles.to_csv(index=False, header=False))
                print(detalles.to_csv(index=False, header=False))

# Función para ejecutar opciones basadas en los datos encontrados
def ejecutar_opciones():
    df_resultado = pd.read_csv('resultado.csv', header=None, names=['Binary', 'Function Name', 'Function URL', 'Description', 'Example'])
    
    for binario in df_resultado['Binary'].unique():
        print(f"Binario encontrado: {binario}")
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
            print(f"Ejecutando opción {opcion} para {binario}")
            # Código para ejecutar la opción correspondiente
            print(f"Ejemplo de ejecución:\n{detalles.iloc[opcion-1]['Example']}")
            # Aquí puedes agregar el código para ejecutar el ejemplo si es necesario
        else:
            print("Saliendo")
            break

if __name__ == '__main__':
    buscar_binarios()
    ejecutar_opciones()
