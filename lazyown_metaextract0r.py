import os
import PyPDF2
import docx
import olefile
import exifread
import signal
import argparse

BANNER = """
██╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██║     ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
██║     ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██║     ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
███████╗██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
[*] Iniciando: LazyMeta extract0r [;,;]
"""
print(BANNER)

def signal_handler(sig, frame):
    global should_exit
    print("\n [<-] Saliendo...")
    should_exit = True

signal.signal(signal.SIGINT, signal_handler)

def extract_pdf_metadata(file_path):
    metadata = {}
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            metadata = reader.metadata
    except Exception as e:
        metadata['error'] = str(e)
    return metadata

def extract_docx_metadata(file_path):
    metadata = {}
    try:
        doc = docx.Document(file_path)
        core_properties = doc.core_properties
        metadata = {prop: getattr(core_properties, prop) for prop in dir(core_properties) if not prop.startswith('_')}
    except Exception as e:
        metadata['error'] = str(e)
    return metadata

def extract_ole_metadata(file_path):
    metadata = {}
    try:
        if olefile.isOleFile(file_path):
            ole = olefile.OleFileIO(file_path)
            meta = ole.get_metadata()
            metadata = {key: meta.get(key) for key in meta.SUMMARY_ATTRIBS}
    except Exception as e:
        metadata['error'] = str(e)
    return metadata

def extract_image_metadata(file_path):
    metadata = {}
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
            metadata = {tag: tags[tag] for tag in tags}
    except Exception as e:
        metadata['error'] = str(e)
    return metadata

def extract_metadata(file_path):
    if file_path.endswith('.pdf'):
        return extract_pdf_metadata(file_path)
    elif file_path.endswith('.docx'):
        return extract_docx_metadata(file_path)
    elif file_path.endswith(('.doc', '.xls')):
        return extract_ole_metadata(file_path)
    elif file_path.endswith(('.jpg', '.jpeg', '.tiff')):
        return extract_image_metadata(file_path)
    else:
        return {}

def find_and_extract_metadata(directory, output_file):
    supported_extensions = ('.pdf', '.docx', '.doc', '.xls', '.jpg', '.jpeg', '.tiff')
    metadata_content = ""
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_extensions):
                file_path = os.path.join(root, file)
                metadata_content += f"\n[x] Extracting metadata from: {file_path}\n"
                print(f"\n[x] Extracting metadata from: {file_path}")
                metadata = extract_metadata(file_path)
                for key, value in metadata.items():
                    metadata_content += "___________________________________________________\n"
                    metadata_content += f"{key}: {value}\n"
                    print("___________________________________________________")
                    print(f"{key}: {value}")
    
    with open(output_file, 'w') as f:
        f.write(metadata_content)

def parse_arguments():
    """
    Parsear los argumentos de la línea de comandos.
    """
    parser = argparse.ArgumentParser(description='Script Meta Extract0r [;,;]')
    parser.add_argument('--path', required=True, help='Path para realizar la búsqueda')
   
    return parser.parse_args()

def main():
    args = parse_arguments()
    directory = args.path
    if not os.path.isdir(directory):
        print(f"[-] The directory {directory} does not exist.")
        return

    output_file = f"LazyOwn_metaextrac0r_metadata_{os.path.basename(directory)}.txt"
    find_and_extract_metadata(directory, output_file)
    print(f"[+] Metadata saved to {output_file}")

if __name__ == "__main__":
    main()
