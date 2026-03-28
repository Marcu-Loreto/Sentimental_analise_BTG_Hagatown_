import os
import sys
from datetime import datetime

# Garante que o diretório raiz está no path para importar database e insights_agent
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def check_system():
    print(f"--- 🏥 System Health Check ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")
    
    # 1. Check Prompts
    print("\n[1/4] Verificando Prompts:")
    prompts = [
        "prompt/prompt_agente.md",
        "prompt/prompt_insight_relatorio.md",
        "prompt/prompt_insight_chat.md",
        "prompt/prompt_feedback_usuario.md"
    ]
    for p in prompts:
        if os.path.exists(p):
            size = os.path.getsize(p)
            print(f"  ✅ {p} ({size} bytes)")
        else:
            print(f"  ❌ {p} NÃO ENCONTRADO")

    # 2. Check Database
    print("\n[2/4] Verificando Banco de Dados:")
    try:
        from database import DATABASE_AVAILABLE, init_db, get_connection, put_connection
        init_db()
        if DATABASE_AVAILABLE:
            print("  ✅ Conexão com Banco OK")
            conn = get_connection()
            if conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) FROM messages;")
                    count = cur.fetchone()[0]
                    print(f"  🔹 Total de mensagens no banco: {count}")
                put_connection(conn)
        else:
            print("  ⚠️ Banco de dados indisponível (verifique POSTGRES_* no .env)")
    except Exception as e:
        print(f"  ❌ Erro ao testar banco: {e}")

    # 3. Check Insights Agent & Templates
    print("\n[3/4] Verificando Templates de Insight:")
    try:
        from insights_agent import get_insight_prompt
        template = get_insight_prompt("prompt_insight_chat.md")
        # Test formatting
        test_format = template.format(
            status_sentimento="Teste",
            media_sentimento="0.0",
            palavras_frequentes="nuvem, teste",
            textos_mensagens="Olá mundo"
        )
        print("  ✅ Template 'prompt_insight_chat' carregado e formatado com sucesso.")
    except Exception as e:
        print(f"  ❌ Erro ao formatar template: {e}")

    # 4. Check Key Dependencies
    print("\n[4/4] Verificando Dependências:")
    deps = ["streamlit", "openai", "psycopg2", "streamlit_autorefresh", "pytest_json_report"]
    for d in deps:
        try:
            __import__(d.replace("-", "_"))
            print(f"  ✅ {d} está instalado.")
        except ImportError:
            # Special case for psycopg2 (sometimes binary)
            if d == "psycopg2":
                try: 
                    import psycopg2
                    print(f"  ✅ {d} está instalado.")
                except:
                    print(f"  ⚠️ {d} não encontrado (pode impactar PostgreSQL).")
            else:
                print(f"  ❌ {d} não encontrado.")

    print("\n--- ✅ Health Check Finalizado ---")

if __name__ == "__main__":
    check_system()
