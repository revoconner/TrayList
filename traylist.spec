# File: traylist.spec

# -*- mode: python ; coding: utf-8 -*-
block_cipher = None

a = Analysis(
    ['todo.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Monoton-Regular.ttf', '.'),  # Include the font file
        ('image.png', '.'),  # Include the tray icon image
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
        'customtkinter',
        'pystray',
        'PIL',
        'pyglet.font',
        'pyglet.font.win32',
        'pyglet.gl',
        'tkinter',
        'tkinter.ttk',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

# Remove duplicate DLLs and binaries
def remove_duplicates(list_of_tuples):
    seen = set()
    return [item for item in list_of_tuples if item[0] not in seen and not seen.add(item[0])]

a.binaries = remove_duplicates(a.binaries)
a.datas = remove_duplicates(a.datas)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    [],  # Changed from bundling everything into exe
    exclude_binaries=True,  # Important for directory-based build
    name='TrayList',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='image.png',
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)

# Create the directory with all files
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TrayList'
)