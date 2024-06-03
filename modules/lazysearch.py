import pandas as pd
import argparse
from colorama import Fore, Style, init
from tabulate import tabulate

# Inicializa colorama
init(autoreset=True)

def highlight_term(text, term):
    return text.replace(term, f"{Fore.GREEN}{term}{Style.RESET_ALL}")

def search_in_parquet(term, parquet_files):
    # Leer los archivos Parquet
    dataframes = [pd.read_parquet(file) for file in parquet_files]

    # Concatenar los DataFrames en uno solo
    df = pd.concat(dataframes, ignore_index=True)

    # Filtrar las filas que contienen el término de búsqueda
    result = df[df.apply(lambda row: row.astype(str).str.contains(term, case=False).any(), axis=1)]

    return result

def main():
    parser = argparse.ArgumentParser(description="Buscar en archivos Parquet")
    parser.add_argument("term", help="Término de búsqueda")
    parser.add_argument("--parquet_files", nargs='+', default=["parquets/binarios.parquet", "parquets/detalles.parquet"], help="Lista de archivos Parquet a buscar")
    args = parser.parse_args()

    result = search_in_parquet(args.term, args.parquet_files)

    if not result.empty:
        result_str = result.astype(str)
        highlighted_result = result_str.applymap(lambda x: highlight_term(x, args.term))

        print(f"Resultados encontrados para '{args.term}':")
        print(tabulate(highlighted_result, headers='keys', tablefmt='psql', showindex=False))
    else:
        print(f"No se encontraron resultados para '{args.term}'")

if __name__ == "__main__":
    main()
