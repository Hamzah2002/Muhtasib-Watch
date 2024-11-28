# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('models', 'models'),  # Include models
        ('data/phishing_emails.csv', 'data/phishing_emails.csv'),  # Include data
        ('resources', 'resources'),  # Include resources folder
        ('ui', 'ui'),  # Include UI folder
    ],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'nltk.corpus',
        'attachment_scanner',
        'dkim_spf_validator',
        'gmail_downloader',
        'outlook_downloader',
        'url_checker',
        # Add NumPy imports to resolve the "numpy.core.multiarray" issue
        'numpy',
        'numpy.core',
        'numpy.core.multiarray',
        'numpy.lib',
        'numpy.linalg',
        'numpy.fft',
        'numpy.polynomial',
        'numpy.random',
    ],
    hookspath=[],  # Optional: Add NumPy hook path if necessary
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
