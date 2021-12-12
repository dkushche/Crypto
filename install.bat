@IF NOT EXIST crypto_env (
    @ECHO "Start installation process"
    @python -m venv crypto_env
    @crypto_env\Scripts\activate.bat
    @pip install -r requirements_windows.txt
    @crypto_env\Scripts\deactivate.bat
    @ECHO "Installed"
) ELSE (
    @ECHO "Already installed"
)