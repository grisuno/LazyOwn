import os

def check_files(path):
    for root, dirs, files in os.walk(path):
        if '.git' in root or '.github' in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.islink(filepath):
                continue
            try:
                with open(filepath, 'rb') as f:
                    content = f.read()
                    content.decode('utf-8')
            except UnicodeDecodeError:
                print(f"Non-UTF8 file: {filepath}")
            except Exception as e:
                pass

check_files('.')
