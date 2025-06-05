import sys
import os

# Adiciona o diretório 'src/Game' ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'Game'))

from Menu import menuPrincipal

menuPrincipal(800, 600)
