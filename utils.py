import unicodedata
import re

# Função para remover acentuação e caracteres especiais
def remover_acentos(texto):
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    return re.sub(r'[^A-Za-z0-9-]', '', texto_normalizado)
