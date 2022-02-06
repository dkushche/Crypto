@ECHO "Start installation process"

@python -m venv crypto_env

@crypto_env\Scripts\activate.bat
@pip install -r windows_platform\requirements.txt
@crypto_env\Scripts\deactivate.bat

@ECHO "Installed"
