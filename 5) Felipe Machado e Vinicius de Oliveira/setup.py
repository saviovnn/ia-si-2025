import os
import subprocess
import sys

# Criar venv se não existir
if not os.path.exists("venv"):
    subprocess.run([sys.executable, "-m", "venv", "venv"])

# Instalar dependências
pip_exec = "venv\\Scripts\\pip.exe" if os.name == "nt" else "venv/bin/pip"
subprocess.run([pip_exec, "install", "-r", "requirements.txt"])

# Rodar o servidor Flask
python_exec = "venv\\Scripts\\python.exe" if os.name == "nt" else "venv/bin/python"
subprocess.run([python_exec, "app.py"])
