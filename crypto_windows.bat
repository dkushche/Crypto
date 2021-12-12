set location=%cd%

@echo off
cmd /k "cd %location% & crypto_env\Scripts\activate.bat & python core.py %* & crypto_env\Scripts\deactivate.bat"
