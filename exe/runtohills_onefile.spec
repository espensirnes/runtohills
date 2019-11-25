# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['exe_main.py'],
             pathex=['B:\\Forskning\\Papers\\experimentsGUI\\runtohills\\exe'],
             binaries=[
				('C:\\Program Files\\Python37\\Lib\\site-packages\\pyglet_ffmpeg2\\Win64\\*.dll','.'), 
				('C:\Windows\System32\downlevel\\*.dll','.')],
             datas=[
				('..\\runtohills\\images','runtohills\\images'),
				('..\\runtohills\\sounds','runtohills\\sounds')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='runtohills',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
