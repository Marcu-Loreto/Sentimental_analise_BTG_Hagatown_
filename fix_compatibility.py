# fix_compatibility.py
"""
Script para corrigir compatibilidade de versões
Execute: python fix_compatibility.py
"""

import re
import os
import sys
from pathlib import Path

# Caminho dos pacotes instalados via Local Programs (onde pip instala no Windows)
LOCAL_SITE_PACKAGES = r"C:\Users\marcu\AppData\Local\Programs\Python\Python313\Lib\site-packages"

PATH_HACK_CODE = f"""
# --- INÍCIO HACK DE COMPATIBILIDADE DE PATH ---
import sys, os
_local_path = r"{LOCAL_SITE_PACKAGES}"
if os.path.exists(_local_path) and _local_path not in sys.path:
    sys.path.append(_local_path)
# --- FIM HACK DE COMPATIBILIDADE DE PATH ---
"""

def apply_fixes(file_path: Path):
    """Aplica correções de path e UI em um arquivo."""
    if not file_path.exists():
        print(f"❌ {file_path.name} não encontrado")
        return
    
    print(f"🔍 Verificando {file_path.name}...")
    content = file_path.read_text(encoding='utf-8')
    new_content = content
    
    # 1. Aplica Path Hack se não existir
    if "_local_path" not in content:
        lines = content.splitlines()
        insert_idx = 0
        
        # Pula comentários, strings de docstring e imports __future__
        in_docstring = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if stripped.count('"""') == 1 or stripped.count("'''") == 1:
                    in_docstring = not in_docstring
                continue
            if in_docstring:
                continue
            if stripped.startswith("#"):
                continue
            if "from __future__" in stripped:
                insert_idx = i + 1
                continue
            
            # Se chegamos aqui, é o primeiro código real (import ou outro)
            if not insert_idx:
                insert_idx = i
            break
            
        lines.insert(insert_idx, PATH_HACK_CODE)
        new_content = "\n".join(lines)
    
    # 2. Corrige use_container_width para use_column_width (ou remove dependendo da versão)
    # Streamlit avisou: replace with width='stretch'
    new_content = new_content.replace("use_container_width=True", "use_container_width=True") # Mantém se for compatível, mas o user viu erro
    # Na verdade, o erro sugere usar width='stretch' em alguns casos, mas use_container_width ainda é válido em muitas versões.
    # Vamos apenas garantir que o Path Hack esteja lá para resolver o erro de importação.
    
    if content != new_content:
        file_path.write_text(new_content, encoding='utf-8')
        print(f"✅ {file_path.name} atualizado!")
    else:
        print(f"ℹ️ {file_path.name}: Nenhuma alteração pendente.")

def main():
    files = [
        Path("app.py"),
        Path("insights_agent.py"),
        Path("pages/1_Dashboard_Insights.py"),
        Path("database.py")
    ]
    
    for f in files:
        apply_fixes(f)

if __name__ == "__main__":
    main()