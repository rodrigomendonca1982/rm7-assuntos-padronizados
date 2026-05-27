#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RM7-MSG-PY - Versão 2.0.5

Sistema local para gerenciamento de assuntos/registros com:
- visualização pública;
- autenticação simples por senha;
- menu administrativo oculto;
- cadastro, edição e exclusão;
- backup em pasta própria com observação de até 30 caracteres;
- restauração listando arquivos existentes;
- exportação da lista completa em HTML.

Correções da versão 2.0.1:
- o JSON principal fica obrigatoriamente na pasta data/dados.json;
- registros de assuntos não possuem campo Observações;
- a observação existe apenas no backup, registrada no índice de backups;
- base padrão inicial incluída em data/dados.json;
- campo Status removido da interface, API, exportação e novos registros;
- tabela principal mantida no padrão da versão 1.0;
- paginação adicionada no navegador com limite padrão de 25 itens por página.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
from datetime import datetime
from pathlib import Path
import json
import shutil
import re


# ============================================================
# CONFIGURAÇÕES PRINCIPAIS
# ============================================================

HOST = "0.0.0.0"
PORTA = 8765

BASE_DIR = Path(__file__).resolve().parent
PASTA_DATA = BASE_DIR / "data"
ARQUIVO_DADOS = PASTA_DATA / "dados.json"
ARQUIVO_DADOS_ANTIGO = BASE_DIR / "dados.json"
PASTA_BACKUP = BASE_DIR / "backup"
ARQUIVO_INDICE_BACKUPS = PASTA_BACKUP / "_indice_backups.json"
PASTA_EXPORTADOS = BASE_DIR / "exportados"

# Senha administrativa simples.
# Altere aqui a senha do administrador.
SENHA_ADMIN = "123456"


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def normalizar_registro(item):
    """
    Mantém somente os campos que pertencem aos assuntos.
    A observação foi removida dos assuntos e agora pertence apenas ao backup.
    """
    return {
        "id": item.get("id"),
        "responsavel": str(item.get("responsavel", "")).strip(),
        "assunto": str(item.get("assunto", "")).strip(),
        "padrao": bool(item.get("padrao", False)),
    }


def normalizar_lista_dados(dados):
    """
    Garante que o arquivo de dados contenha uma lista limpa de registros.
    Remove chaves antigas, como observacoes, caso venham de versões anteriores.
    """
    if not isinstance(dados, list):
        return []

    lista_normalizada = []
    for item in dados:
        if isinstance(item, dict):
            registro = normalizar_registro(item)
            if registro["assunto"]:
                lista_normalizada.append(registro)
    return lista_normalizada


def garantir_estrutura():
    """
    Garante que os arquivos e pastas essenciais existam.
    Também migra dados.json da raiz para data/dados.json, se existir versão antiga.
    """
    PASTA_DATA.mkdir(exist_ok=True)
    PASTA_BACKUP.mkdir(exist_ok=True)
    PASTA_EXPORTADOS.mkdir(exist_ok=True)

    if not ARQUIVO_DADOS.exists() and ARQUIVO_DADOS_ANTIGO.exists():
        shutil.copy2(ARQUIVO_DADOS_ANTIGO, ARQUIVO_DADOS)

    if not ARQUIVO_DADOS.exists():
        dados_iniciais = [
            {
                        "id": 1,
                        "responsavel": "ASS_PDR",
                        "assunto": "FULANO, BELTRANO, CICLANO",
                        "padrao": True
            },
            {
                        "id": 2,
                        "responsavel": "01.3",
                        "assunto": "OMS",
                        "padrao": False
            },
            {
                        "id": 3,
                        "responsavel": "100",
                        "assunto": "ASSUNTO DO 100",
                        "padrao": False
            },
            {
                        "id": 4,
                        "responsavel": "200",
                        "assunto": "ASSUNTO DO 200",
                        "padrao": False
            },
            {
                        "id": 5,
                        "responsavel": "300",
                        "assunto": "ASSUNTO DO 300",
                        "padrao": False
            },
            {
                        "id": 6,
                        "responsavel": "400",
                        "assunto": "ASSUNTO DO 400",
                        "padrao": False
            }
]
        salvar_dados(dados_iniciais)
    else:
        # Limpa arquivos herdados que ainda tenham campo observacoes.
        salvar_dados(ler_dados())

    if not ARQUIVO_INDICE_BACKUPS.exists():
        salvar_indice_backups([])


def ler_dados():
    """
    Lê o arquivo principal de dados JSON em data/dados.json.
    Se houver erro, retorna uma lista vazia para não derrubar o servidor.
    """
    try:
        if not ARQUIVO_DADOS.exists():
            return []
        with ARQUIVO_DADOS.open("r", encoding="utf-8") as arquivo:
            conteudo = json.load(arquivo)
            return normalizar_lista_dados(conteudo)
    except Exception:
        return []


def salvar_dados(dados):
    """
    Salva a lista de registros no arquivo principal data/dados.json.
    """
    PASTA_DATA.mkdir(exist_ok=True)
    dados_limpos = normalizar_lista_dados(dados)
    with ARQUIVO_DADOS.open("w", encoding="utf-8") as arquivo:
        json.dump(dados_limpos, arquivo, ensure_ascii=False, indent=2)


def ler_indice_backups():
    """
    Lê o índice de backups, onde fica a observação de cada backup.
    """
    try:
        if not ARQUIVO_INDICE_BACKUPS.exists():
            return []
        with ARQUIVO_INDICE_BACKUPS.open("r", encoding="utf-8") as arquivo:
            conteudo = json.load(arquivo)
            return conteudo if isinstance(conteudo, list) else []
    except Exception:
        return []


def salvar_indice_backups(indice):
    """
    Salva o índice de backups dentro da pasta backup.
    """
    PASTA_BACKUP.mkdir(exist_ok=True)
    with ARQUIVO_INDICE_BACKUPS.open("w", encoding="utf-8") as arquivo:
        json.dump(indice if isinstance(indice, list) else [], arquivo, ensure_ascii=False, indent=2)


def resposta_json(handler, status, payload):
    """
    Envia uma resposta JSON padronizada.
    """
    corpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(corpo)))
    handler.end_headers()
    handler.wfile.write(corpo)


def ler_json_requisicao(handler):
    """
    Lê o corpo JSON de uma requisição POST.
    """
    tamanho = int(handler.headers.get("Content-Length", "0"))
    if tamanho <= 0:
        return {}
    corpo = handler.rfile.read(tamanho).decode("utf-8")
    try:
        return json.loads(corpo)
    except Exception:
        return {}


def limitar_observacao_backup(texto):
    """
    Limita a observação original do backup a 30 caracteres.
    """
    observacao = (texto or "backup").strip()[:30]
    return observacao or "backup"


def sanitizar_nome_backup(descricao):
    """
    Sanitiza a observação do backup para uso seguro no nome do arquivo.
    """
    descricao = limitar_observacao_backup(descricao)

    substituicoes = {
        "á": "a", "à": "a", "ã": "a", "â": "a", "ä": "a",
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "í": "i", "ì": "i", "î": "i", "ï": "i",
        "ó": "o", "ò": "o", "õ": "o", "ô": "o", "ö": "o",
        "ú": "u", "ù": "u", "û": "u", "ü": "u",
        "ç": "c",
        "Á": "A", "À": "A", "Ã": "A", "Â": "A", "Ä": "A",
        "É": "E", "È": "E", "Ê": "E", "Ë": "E",
        "Í": "I", "Ì": "I", "Î": "I", "Ï": "I",
        "Ó": "O", "Ò": "O", "Õ": "O", "Ô": "O", "Ö": "O",
        "Ú": "U", "Ù": "U", "Û": "U", "Ü": "U",
        "Ç": "C",
    }

    for original, novo in substituicoes.items():
        descricao = descricao.replace(original, novo)

    descricao = descricao.lower()
    descricao = re.sub(r"[^a-z0-9]+", "-", descricao)
    descricao = descricao.strip("-")

    return descricao or "backup"


def proximo_id(dados):
    """
    Calcula o próximo ID numérico.
    """
    ids = []
    for item in dados:
        try:
            ids.append(int(item.get("id", 0)))
        except Exception:
            pass
    return max(ids, default=0) + 1


def escapar_html(valor):
    """
    Escapa texto para uso seguro no HTML exportado.
    """
    texto = str(valor if valor is not None else "")
    return (
        texto.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&#039;")
    )


def gerar_html_exportado(dados):
    """
    Gera o conteúdo HTML com a lista completa de registros.
    A exportação acompanha a tabela principal: Responsável e Assunto.
    """
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    linhas = []
    for item in dados:
        linhas.append(f"""
        <tr>
          <td>{escapar_html(item.get("responsavel", ""))}</td>
          <td>{escapar_html(item.get("assunto", ""))}</td>
        </tr>
        """)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Lista Completa de Assuntos</title>
  <style>
    body {{
      font-family: Arial, Helvetica, sans-serif;
      margin: 30px;
      color: #222;
      background: #ffffff;
    }}

    h1 {{
      margin-bottom: 5px;
      color: #0f2742;
    }}

    .subtitulo {{
      margin-bottom: 20px;
      color: #555;
      font-size: 14px;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}

    th, td {{
      border: 1px solid #cccccc;
      padding: 8px;
      text-align: left;
      vertical-align: top;
    }}

    th {{
      background: #0f2742;
      color: #ffffff;
    }}

    tr:nth-child(even) {{
      background: #f7f9fb;
    }}

    .rodape {{
      margin-top: 20px;
      font-size: 12px;
      color: #777;
    }}

    @media print {{
      body {{
        margin: 15px;
      }}
    }}
  </style>
</head>
<body>
  <h1>Lista Completa de Assuntos</h1>
  <div class="subtitulo">Exportado em: {escapar_html(agora)}</div>

  <table>
    <thead>
      <tr>
        <th>RESPONSAVEL</th>
        <th>Assunto</th>
      </tr>
    </thead>
    <tbody>
      {''.join(linhas)}
    </tbody>
  </table>

  <div class="rodape">
    Arquivo gerado pelo sistema RM7-MSG-PY - Versão 2.0.5.
  </div>
</body>
</html>
"""


# ============================================================
# HANDLER HTTP
# ============================================================

class SistemaHandler(SimpleHTTPRequestHandler):
    """
    Manipulador HTTP do sistema.
    Atende arquivos estáticos e endpoints da API local.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def log_message(self, format, *args):
        """
        Mantém o log do servidor mais limpo.
        """
        print("[%s] %s" % (datetime.now().strftime("%d/%m/%Y %H:%M:%S"), format % args))

    def do_GET(self):
        caminho = urlparse(self.path).path

        if caminho == "/api/dados":
            self.api_listar_dados()
            return

        if caminho == "/api/backups":
            self.api_listar_backups()
            return

        if caminho == "/":
            self.path = "/index.html"

        super().do_GET()

    def do_POST(self):
        caminho = urlparse(self.path).path

        if caminho == "/api/login":
            self.api_login()
            return

        if caminho == "/api/dados/criar":
            self.api_criar_registro()
            return

        if caminho == "/api/dados/editar":
            self.api_editar_registro()
            return

        if caminho == "/api/dados/excluir":
            self.api_excluir_registro()
            return

        if caminho == "/api/backup/criar":
            self.api_criar_backup()
            return

        if caminho == "/api/backup/restaurar":
            self.api_restaurar_backup()
            return

        if caminho == "/api/exportar":
            self.api_exportar_html()
            return

        resposta_json(self, 404, {"sucesso": False, "mensagem": "Endpoint não encontrado."})

    # --------------------------------------------------------
    # API: autenticação
    # --------------------------------------------------------

    def api_login(self):
        payload = ler_json_requisicao(self)
        senha = payload.get("senha", "")

        if senha == SENHA_ADMIN:
            resposta_json(self, 200, {"sucesso": True, "mensagem": "Autenticação realizada com sucesso."})
        else:
            resposta_json(self, 401, {"sucesso": False, "mensagem": "Senha incorreta."})

    # --------------------------------------------------------
    # API: dados
    # --------------------------------------------------------

    def api_listar_dados(self):
        resposta_json(self, 200, {"sucesso": True, "dados": ler_dados()})

    def api_criar_registro(self):
        payload = ler_json_requisicao(self)
        dados = ler_dados()

        novo = {
            "id": proximo_id(dados),
            "responsavel": payload.get("responsavel", "").strip(),
            "assunto": payload.get("assunto", "").strip(),
            "padrao": bool(payload.get("padrao", False)),
        }

        if not novo["assunto"]:
            resposta_json(self, 400, {"sucesso": False, "mensagem": "O campo assunto é obrigatório."})
            return

        dados.append(novo)
        salvar_dados(dados)
        resposta_json(self, 200, {"sucesso": True, "mensagem": "Registro criado com sucesso.", "registro": novo})

    def api_editar_registro(self):
        payload = ler_json_requisicao(self)
        dados = ler_dados()

        try:
            id_registro = int(payload.get("id"))
        except Exception:
            resposta_json(self, 400, {"sucesso": False, "mensagem": "ID inválido."})
            return

        for item in dados:
            if int(item.get("id", 0)) == id_registro:
                item["responsavel"] = payload.get("responsavel", "").strip()
                item["assunto"] = payload.get("assunto", "").strip()
                if not item["assunto"]:
                    resposta_json(self, 400, {"sucesso": False, "mensagem": "O campo assunto é obrigatório."})
                    return

                salvar_dados(dados)
                resposta_json(self, 200, {"sucesso": True, "mensagem": "Registro atualizado com sucesso."})
                return

        resposta_json(self, 404, {"sucesso": False, "mensagem": "Registro não encontrado."})

    def api_excluir_registro(self):
        payload = ler_json_requisicao(self)
        dados = ler_dados()

        try:
            id_registro = int(payload.get("id"))
        except Exception:
            resposta_json(self, 400, {"sucesso": False, "mensagem": "ID inválido."})
            return

        novos_dados = [item for item in dados if int(item.get("id", 0)) != id_registro]

        if len(novos_dados) == len(dados):
            resposta_json(self, 404, {"sucesso": False, "mensagem": "Registro não encontrado."})
            return

        salvar_dados(novos_dados)
        resposta_json(self, 200, {"sucesso": True, "mensagem": "Registro excluído com sucesso."})

    # --------------------------------------------------------
    # API: backup
    # --------------------------------------------------------

    def api_criar_backup(self):
        payload = ler_json_requisicao(self)
        observacao = limitar_observacao_backup(payload.get("observacao") or payload.get("descricao", ""))
        nome_seguro = sanitizar_nome_backup(observacao)

        PASTA_BACKUP.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = f"backup_{timestamp}_{nome_seguro}.json"
        destino = PASTA_BACKUP / nome_arquivo

        if not ARQUIVO_DADOS.exists():
            salvar_dados([])

        shutil.copy2(ARQUIVO_DADOS, destino)

        indice = ler_indice_backups()
        indice.insert(0, {
            "arquivo": nome_arquivo,
            "observacao": observacao,
            "criado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        })
        salvar_indice_backups(indice)

        resposta_json(self, 200, {
            "sucesso": True,
            "mensagem": "Backup criado com sucesso.",
            "arquivo": nome_arquivo,
            "observacao": observacao,
        })

    def api_listar_backups(self):
        PASTA_BACKUP.mkdir(exist_ok=True)

        indice = {item.get("arquivo"): item for item in ler_indice_backups() if isinstance(item, dict)}

        arquivos = []
        for arquivo in sorted(PASTA_BACKUP.glob("backup_*.json"), reverse=True):
            stat = arquivo.stat()
            item_indice = indice.get(arquivo.name, {})
            arquivos.append({
                "nome": arquivo.name,
                "observacao": item_indice.get("observacao", ""),
                "criado_em": item_indice.get("criado_em", ""),
                "tamanho": stat.st_size,
                "modificado_em": datetime.fromtimestamp(stat.st_mtime).strftime("%d/%m/%Y %H:%M:%S")
            })

        resposta_json(self, 200, {"sucesso": True, "backups": arquivos})

    def api_restaurar_backup(self):
        payload = ler_json_requisicao(self)
        nome = payload.get("arquivo", "")

        # Segurança: impede caminhos como ../arquivo.json
        nome_seguro = Path(nome).name
        origem = PASTA_BACKUP / nome_seguro

        if not origem.exists() or origem.suffix.lower() != ".json" or not nome_seguro.startswith("backup_"):
            resposta_json(self, 404, {"sucesso": False, "mensagem": "Backup não encontrado."})
            return

        # Valida se o backup contém JSON válido antes de restaurar.
        try:
            with origem.open("r", encoding="utf-8") as arquivo:
                dados_backup = json.load(arquivo)
            dados_backup = normalizar_lista_dados(dados_backup)
        except Exception:
            resposta_json(self, 400, {"sucesso": False, "mensagem": "O arquivo de backup não contém JSON válido."})
            return

        salvar_dados(dados_backup)
        resposta_json(self, 200, {"sucesso": True, "mensagem": "Backup restaurado com sucesso."})

    # --------------------------------------------------------
    # API: exportação
    # --------------------------------------------------------

    def api_exportar_html(self):
        PASTA_EXPORTADOS.mkdir(exist_ok=True)

        dados = ler_dados()
        html = gerar_html_exportado(dados)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = f"lista_completa_{timestamp}.html"
        destino = PASTA_EXPORTADOS / nome_arquivo

        destino.write_text(html, encoding="utf-8")

        resposta_json(self, 200, {
            "sucesso": True,
            "mensagem": "Exportação HTML criada com sucesso.",
            "arquivo": nome_arquivo,
            "caminho": f"exportados/{nome_arquivo}"
        })


# ============================================================
# INICIALIZAÇÃO
# ============================================================

def iniciar_servidor():
    garantir_estrutura()
    servidor = HTTPServer((HOST, PORTA), SistemaHandler)

    print("=" * 70)
    print("RM7-MSG--PY - Versão 2.0.5")
    print("=" * 70)
    print(f"Servidor iniciado em: http://127.0.0.1:{PORTA}")
    print(f"Acesso na rede local: http://IP-DESTE-COMPUTADOR:{PORTA}")
    print(f"Arquivo JSON principal: {ARQUIVO_DADOS}")
    print("Host configurado para 0.0.0.0")
    print("Pressione CTRL+C para encerrar.")
    print("=" * 70)

    servidor.serve_forever()


if __name__ == "__main__":
    iniciar_servidor()
