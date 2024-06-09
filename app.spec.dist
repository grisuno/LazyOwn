# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('modules/*.py', 'modules'),    # Incluir todos los archivos .py en modules
        ('modules/*.sh', 'modules'),    # Incluir todos los archivos .sh en modules
        ('csv/*.csv', 'csv'),           # Incluir todos los archivos .csv en csv
        ('parquets/*.parquet', 'parquets'), # Incluir todos los archivos .parquet en parquets
        ('payload.json', '.')           # Incluir el archivo payload.json en el directorio raíz si es necesario
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)
