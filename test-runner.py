import os
import glob
from pathlib import Path
from dotenv import load_dotenv

# Importação das bibliotecas oficiais
from openai import OpenAI
import google.generativeai as genai
import anthropic

# Carrega variáveis de ambiente (.env) se existirem, ou pega do sistema
load_dotenv()

# ==============================================================================
# CONFIGURAÇÃO GERAL E MODELOS
# ==============================================================================
# Ajuste os nomes dos modelos conforme a disponibilidade na API.
# Como GPT-5 e Gemini 3 podem não estar públicos na API hoje, usei os mais recentes.
# Basta alterar a string quando tiver acesso.

MODELS_CONFIG = {
    "openai": {
        "model_id": "gpt-4o",  # Substituir por "gpt-5" quando disponível
        "api_key": os.getenv("OPENAI_API_KEY"),
        "client": None # Será inicializado depois
    },
    "google": {
        "model_id": "gemini-1.5-pro", # Substituir por "gemini-3-pro" quando disponível
        "api_key": os.getenv("GOOGLE_API_KEY"),
        "client": None
    },
    "anthropic": {
        "model_id": "claude-3-5-sonnet-20241022", # Substituir por "claude-4.5"
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
        "client": None
    }
}

# Configuração de Saída
INPUT_DIR = "prompts"   # Pasta onde estão os arquivos case-01.txt, etc.
OUTPUT_DIR = "results"  # Pasta onde os resultados serão salvos

# Cria diretório de saída se não existir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==============================================================================
# INICIALIZAÇÃO DOS CLIENTES
# ==============================================================================

def init_clients():
    # OpenAI
    if MODELS_CONFIG["openai"]["api_key"]:
        MODELS_CONFIG["openai"]["client"] = OpenAI(api_key=MODELS_CONFIG["openai"]["api_key"])
    
    # Google
    if MODELS_CONFIG["google"]["api_key"]:
        genai.configure(api_key=MODELS_CONFIG["google"]["api_key"])
        # O cliente do Google é instanciado na hora da chamada, mas configuramos a chave aqui
    
    # Anthropic
    if MODELS_CONFIG["anthropic"]["api_key"]:
        MODELS_CONFIG["anthropic"]["client"] = anthropic.Anthropic(api_key=MODELS_CONFIG["anthropic"]["api_key"])

# ==============================================================================
# FUNÇÕES DE CHAMADA (WRAPPERS)
# ==============================================================================

def call_openai(prompt_content):
    client = MODELS_CONFIG["openai"]["client"]
    model = MODELS_CONFIG["openai"]["model_id"]
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."}, # O prompt completo já contém a persona, aqui é só setup
                {"role": "user", "content": prompt_content}
            ],
            temperature=0.0, # Cientificamente correto para reprodutibilidade
            seed=42,         # Fixa a aleatoriedade
            max_tokens=4096
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"# ERROR calling OpenAI: {str(e)}"

def call_google(prompt_content):
    model_name = MODELS_CONFIG["google"]["model_id"]
    
    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "temperature": 0.0,
                "max_output_tokens": 4096
            }
        )
        response = model.generate_content(prompt_content)
        return response.text
    except Exception as e:
        return f"# ERROR calling Google: {str(e)}"

def call_anthropic(prompt_content):
    client = MODELS_CONFIG["anthropic"]["client"]
    model = MODELS_CONFIG["anthropic"]["model_id"]
    
    try:
        message = client.messages.create(
            model=model,
            max_tokens=4096,
            temperature=0.0,
            messages=[
                {"role": "user", "content": prompt_content}
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"# ERROR calling Anthropic: {str(e)}"

# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

def process_files():
    # Encontra arquivos case-01.txt até case-04.txt
    # Ajuste o padrão se seus arquivos tiverem nomes diferentes
    files = sorted(glob.glob(os.path.join(INPUT_DIR, "case-*.txt")))
    
    if not files:
        print(f"Nenhum arquivo encontrado em '{INPUT_DIR}'. Verifique o caminho.")
        return

    init_clients()
    
    print(f"Iniciando processamento de {len(files)} arquivos para 3 modelos...\n")

    for file_path in files:
        file_name = Path(file_path).stem # ex: case-01
        print(f"--- Processando: {file_name} ---")
        
        # Lê o conteúdo do arquivo de prompt
        with open(file_path, "r", encoding="utf-8") as f:
            prompt_content = f.read()

        # 1. OpenAI
        print(f"   > Enviando para {MODELS_CONFIG['openai']['model_id']}...")
        result_openai = call_openai(prompt_content)
        save_result(file_name, "gpt", result_openai)

        # 2. Google
        print(f"   > Enviando para {MODELS_CONFIG['google']['model_id']}...")
        result_google = call_google(prompt_content)
        save_result(file_name, "gemini", result_google)

        # 3. Anthropic
        print(f"   > Enviando para {MODELS_CONFIG['anthropic']['model_id']}...")
        result_anthropic = call_anthropic(prompt_content)
        save_result(file_name, "claude", result_anthropic)
        
        print("\n")

def save_result(case_name, model_alias, content):
    filename = f"result_{case_name}_{model_alias}.py"
    path = os.path.join(OUTPUT_DIR, filename)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"     -> Salvo em: {path}")

if __name__ == "__main__":
    # Crie uma pasta chamada 'prompts' e coloque os arquivos case-01.txt lá dentro
    # Ou altere a variável INPUT_DIR no início do script
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        print(f"Pasta '{INPUT_DIR}' criada. Coloque seus arquivos .txt lá e rode novamente.")
    else:
        process_files()