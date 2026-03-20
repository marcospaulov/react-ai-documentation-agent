import subprocess
import os
from pathlib import Path

def read_file_tool(filepath: str) -> str:
    path = Path(filepath.strip())
    if not path.exists():
        return f"Erro: Arquivo {filepath} não encontrado."
    try:
        if path.is_dir():
            return f"Erro: {filepath} é um diretório, use a ferramenta list_directory em vez disso."
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Erro lendo arquivo: {str(e)}"

def list_directory_tool(dirpath: str) -> str:
    path = Path(dirpath.strip() or ".")
    if not path.exists() or not path.is_dir():
        return f"Erro: Diretório {dirpath} não encontrado."
    try:
        items = list(path.iterdir())
        files = [f"- {i.name} (Arquivo)" for i in items if i.is_file()]
        dirs = [f"- {i.name}/ (Pasta)" for i in items if i.is_dir()]
        return "Conteúdo de " + str(path) + ":\n" + "\n".join(dirs + files)
    except Exception as e:
        return f"Erro listando diretório: {str(e)}"

def git_log_tool(n: str) -> str:
    try:
        count = int(n.strip() or 5)
        res = subprocess.check_output(["git", "log", f"-n{count}", "--oneline"], text=True)
        return res if res else "Sem commits no repositório local."
    except Exception as e:
        return f"Erro ao acessar Git: {str(e)}"

def git_diff_tool(args: str) -> str:
    cmd = ["git", "diff"]
    if args and args.strip():
        cmd.extend(args.strip().split())
    try:
        res = subprocess.check_output(cmd, text=True)
        return res[:2000] if len(res) > 2000 else (res or "Nenhuma diferença/modificação git não rastreada encontrada (Tudo está clean).")
    except Exception as e:
        return f"Erro no Git diff: {str(e)}"

TOOLS = {
    "read_file": {
        "func": read_file_tool,
        "description": "read_file: Lê um arquivo local na raiz do projeto. Input obrigatório: caminho exato do arquivo (ex: src/llm.py)."
    },
    "list_directory": {
        "func": list_directory_tool,
        "description": "list_directory: Lista os arquivos de uma pasta local para saber os nomes dos arquivos. Input: caminho relativo (ex: . ou src)."
    },
    "git_log": {
        "func": git_log_tool,
        "description": "git_log: Traz git changelog / histórico de commits recentes. Input logico: numero inteiro de commits limitante (ex: 5)."
    },
    "git_diff": {
        "func": git_diff_tool,
        "description": "git_diff: Traz diferenças de commits ou arquivos soltos. Input opcional (vazio captura current diffs). Ex: 'HEAD~1 HEAD'."
    }
}

def execute_tool(name: str, input_val: str) -> str:
    if name not in TOOLS:
        return f"Erro crítico: Ferramenta inexistente ou formato Action falho. Tente de novo uma existente."
    try:
        return TOOLS[name]["func"](input_val)
    except Exception as e:
        return f"Erro fatal ao rodar {name}: {str(e)}"
