import pandas as pd
import markdown

def search_database(term, data_path="tests.parquet"):
    """
    Search a term in a DataFrame

    Args:
        term (str): the term to search.
        data_path (str, optional): path to parquet.

    Returns:
        str: Retrun merkdown of results
    """
    try:
        df = pd.read_parquet(data_path)
    except FileNotFoundError:
        return f"Error: file not found {data_path}"
    except ValueError as e:
        return f"Error reading Parquet: {e}"

    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():
            df[col] = df[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

    struct_cols_to_drop = []
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, dict)).any():
            struct_cols_to_drop.append(col)
            df = pd.concat([df.drop(columns=[col]), df[col].apply(pd.Series).add_prefix(f"{col}.")], axis=1)

    term_lower = term.lower()
    results = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(term_lower).any(), axis=1)]

    md_content = ""
    if not results.empty:
        for _, row in results.iterrows():
            md_content += "## Resultado\n"
            for key, value in row.items():
                md_content += f"- **{key}**: {value}\n"
            md_content += "\n"
    else:
        md_content = f"No se encontraron resultados para: '{term}'\n"

    return md_content

def main():
    term = input("Buscar >_ ")
    md_content = search_database(term)

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content)

    # Save HTML content to a file
    try:
        with open("templates/search_results.html", "w") as file:
            file.write(html_content)
        print("    [OK] 'search_results.html'.")
    except OSError as e:
        print(f"Error saving HTML file: {e}")

if __name__ == "__main__":
    main()
