<div align="center">

# 🛡️ RM7-MSG-CMATFN-PY

## 📨 Sistema Centro de Mensagem - Assuntos

![Versão](https://img.shields.io/badge/vers%C3%A3o-2.0.6-0A66C2?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-Local-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-Interface-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-Estilos-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Intera%C3%A7%C3%A3o-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![JSON](https://img.shields.io/badge/JSON-Base%20local-5E5C5C?style=for-the-badge)

**Sistema local para consulta, gerenciamento, backup, restauração e exportação de assuntos usados no endereçamento de mensagens.**

</div>

---

## 🧭 Sumário

- [🎯 Propósito](#-propósito)
- [✨ Visão Geral Atual](#-visão-geral-atual)
- [🧱 Estrutura do Projeto](#-estrutura-do-projeto)
- [📁 Arquivos Principais](#-arquivos-principais)
- [🚀 Como Executar](#-como-executar)
- [🌐 Acesso em Rede](#-acesso-em-rede)
- [🔐 Modos de Uso](#-modos-de-uso)
- [📋 Tabela Atual](#-tabela-atual)
- [🧠 Base de Dados](#-base-de-dados)
- [🔎 Pesquisa e Paginação](#-pesquisa-e-paginação)
- [🛠️ Administração](#️-administração)
- [💾 Backup](#-backup)
- [♻️ Restauração](#️-restauração)
- [📤 Exportação HTML](#-exportação-html)
- [🔌 API Local](#-api-local)
- [🛡️ Segurança](#️-segurança)
- [🧰 Manutenção Recomendada](#-manutenção-recomendada)
- [✅ Resumo Operacional](#-resumo-operacional)

---

## 🎯 Propósito

> O **RM7-MSG-CMATFN-PY** foi desenvolvido para funcionar como um sistema local de consulta e manutenção de assuntos do Centro de Mensagem.

Ele permite que a base de assuntos seja acessada diretamente pelo navegador, usando um servidor Python simples e um arquivo JSON como banco de dados local.

<table>
  <tr>
    <td width="33%" bgcolor="#E8F3FF">
      <h3>🔎 Consulta rápida</h3>
      <p>Pesquisa por responsável ou assunto, com tabela simples e objetiva.</p>
    </td>
    <td width="33%" bgcolor="#EFFFF4">
      <h3>🔐 Administração protegida</h3>
      <p>Cadastro, edição, exclusão, backup, restauração e exportação exigem senha.</p>
    </td>
    <td width="33%" bgcolor="#FFF8E6">
      <h3>📁 Base local</h3>
      <p>Dados armazenados em <code>data/dados.json</code>, sem necessidade de banco externo.</p>
    </td>
  </tr>
</table>

---

## ✨ Visão Geral Atual

> A interface atual está na versão **2.0.6** e voltou ao padrão de tabela simples da versão 1.0.

<table>
  <tr>
    <td bgcolor="#F0F7FF"><strong>📌 Versão</strong></td>
    <td>2.0.6 na interface</td>
  </tr>
  <tr>
    <td bgcolor="#F0F7FF"><strong>📋 Tabela</strong></td>
    <td>Colunas <strong>RESPONSAVEL</strong> e <strong>Assunto</strong></td>
  </tr>
  <tr>
    <td bgcolor="#F0F7FF"><strong>🧾 Dados</strong></td>
    <td>Base principal em <code>data/dados.json</code></td>
  </tr>
  <tr>
    <td bgcolor="#F0F7FF"><strong>💾 Backup</strong></td>
    <td>Arquivos em <code>backup/</code> e índice em <code>backup/_indice_backups.json</code></td>
  </tr>
  <tr>
    <td bgcolor="#F0F7FF"><strong>📤 Exportação</strong></td>
    <td>HTML gerado em <code>exportados/</code></td>
  </tr>
</table>

### ✅ Recursos disponíveis

- 🔎 Pesquisa por responsável ou assunto.
- 📋 Tabela limpa com **RESPONSAVEL** e **Assunto**.
- 📊 Cards superiores com total de registros, registros filtrados e total de páginas.
- 📄 Paginação no navegador.
- 🔢 Seletor de itens por página: **10**, **25**, **50**, **100** ou **Todos**.
- ☰ Menu lateral oculto.
- 👁️ Modo visitante como padrão.
- 🔐 Modo administrador liberado por senha.
- ➕ Cadastro de novo assunto.
- ✏️ Edição de assunto existente.
- 🗑️ Exclusão com confirmação.
- 💾 Backup com observação de até 30 caracteres.
- ♻️ Restauração por lista de backups.
- 📤 Exportação da lista completa em HTML.

> [!IMPORTANT]
> Os campos **Status** e **Observações** não fazem mais parte dos registros de assuntos.  
> A observação existe somente para identificar backups.

---

## 🧱 Estrutura do Projeto

```text
RM7-MSG-CMATFN-PY-V2/
├── 🐍 server.py
├── 🌐 index.html
├── 📘 README.md
├── 🪟 iniciar_windows.bat
├── 🐧 iniciar_linux.sh
├── 📂 data/
│   └── 🧾 dados.json
├── 🎨 static/
│   ├── ⚙️ app.js
│   └── 🎨 style.css
├── 💾 backup/
│   ├── 🗂️ _indice_backups.json
│   └── 🧾 backup_*.json
├── 📤 exportados/
│   └── 🌐 lista_completa_*.html
└── 📚 docs/
    └── 📄 VERSAO-2.0.md
```

---

## 📁 Arquivos Principais

<table>
  <tr>
    <th bgcolor="#0A66C2"><font color="white">Arquivo/Pasta</font></th>
    <th bgcolor="#0A66C2"><font color="white">Função</font></th>
  </tr>
  <tr>
    <td>🐍 <code>server.py</code></td>
    <td>Servidor local, APIs, dados, backup, restauração, exportação e autenticação.</td>
  </tr>
  <tr>
    <td>🌐 <code>index.html</code></td>
    <td>Interface principal aberta no navegador.</td>
  </tr>
  <tr>
    <td>⚙️ <code>static/app.js</code></td>
    <td>Comportamento da tela, login, tabela, paginação, modais e chamadas da API.</td>
  </tr>
  <tr>
    <td>🎨 <code>static/style.css</code></td>
    <td>Estilos da barra superior, menu lateral, tabela, cards, botões e modais.</td>
  </tr>
  <tr>
    <td>🧾 <code>data/dados.json</code></td>
    <td>Arquivo principal da base de assuntos.</td>
  </tr>
  <tr>
    <td>💾 <code>backup/</code></td>
    <td>Pasta dos backups JSON.</td>
  </tr>
  <tr>
    <td>🗂️ <code>backup/_indice_backups.json</code></td>
    <td>Índice com a observação cadastrada para cada backup.</td>
  </tr>
  <tr>
    <td>📤 <code>exportados/</code></td>
    <td>Pasta dos arquivos HTML exportados.</td>
  </tr>
</table>

---

## 🚀 Como Executar

### 🪟 Windows

Use o inicializador:

```bat
iniciar_windows.bat
```

Ou execute manualmente no Prompt de Comando/PowerShell:

```bat
python server.py
```

O arquivo `iniciar_windows.bat` abre automaticamente:

```text
http://127.0.0.1:8765
```

### 🐧 Linux

No terminal, dentro da pasta do sistema:

```bash
chmod +x iniciar_linux.sh
./iniciar_linux.sh
```

Ou execute diretamente:

```bash
python3 server.py
```

> [!NOTE]
> No Linux, o inicializador verifica se a porta `8765` já está em uso. Se o sistema já estiver rodando, ele apenas abre o navegador.

---

## 🌐 Acesso em Rede

### 💻 No próprio computador

```text
http://127.0.0.1:8765
```

### 🖧 Em outro computador da mesma rede

```text
http://IP-DESTE-COMPUTADOR:8765
```

Exemplo:

```text
http://192.168.0.10:8765
```

<table>
  <tr>
    <td bgcolor="#FFF3CD">⚠️ <strong>Atenção</strong></td>
    <td>Para acesso em rede, o computador servidor precisa estar ligado, o <code>server.py</code> precisa estar em execução e o firewall deve permitir conexões na porta <code>8765</code>.</td>
  </tr>
</table>

---

## 🔐 Modos de Uso

<table>
  <tr>
    <td width="50%" bgcolor="#E8F3FF">
      <h3>👁️ Modo Visitante</h3>
      <p>Modo inicial do sistema.</p>
      <ul>
        <li>Visualiza a tabela.</li>
        <li>Pesquisa por responsável ou assunto.</li>
        <li>Altera itens por página.</li>
        <li>Navega pela paginação.</li>
      </ul>
    </td>
    <td width="50%" bgcolor="#EFFFF4">
      <h3>🔐 Modo Administrador</h3>
      <p>Liberado após senha administrativa.</p>
      <ul>
        <li>Cadastra novos assuntos.</li>
        <li>Edita assuntos existentes.</li>
        <li>Exclui assuntos.</li>
        <li>Gera backup.</li>
        <li>Restaura backup.</li>
        <li>Exporta lista HTML.</li>
      </ul>
    </td>
  </tr>
</table>

### 🔑 Senha padrão

A senha administrativa fica no arquivo `server.py`:

```python
SENHA_ADMIN = "123456"
```

> [!WARNING]
> Recomenda-se alterar a senha antes de usar o sistema em rotina real.

---

## 📋 Tabela Atual

A tabela principal exibe:

| 🧩 Coluna | 📌 Descrição |
|---|---|
| **RESPONSAVEL** | Código, setor ou responsável relacionado ao assunto. |
| **Assunto** | Descrição do assunto para consulta. |

Quando o administrador está autenticado, a tabela ganha a coluna:

| 🛠️ Coluna | 📌 Descrição |
|---|---|
| **Ações** | Botões de editar e excluir o registro. |

---

## 🧠 Base de Dados

O arquivo principal da base é:

```text
data/dados.json
```

### 🧾 Estrutura de um registro

```json
{
  "id": 1,
  "responsavel": "ASS_PDR",
  "assunto": "Texto do assunto",
  "padrao": true
}
```

### 🧩 Campos atuais

| Campo | Tipo | Uso |
|---|---|---|
| `id` | número | Identificador do registro. |
| `responsavel` | texto | Código ou responsável pelo assunto. |
| `assunto` | texto | Descrição do assunto. Campo obrigatório. |
| `padrao` | booleano | Marcador interno preservado para identificar assunto padrão. |

### 🚫 Campos removidos

| Campo antigo | Situação atual |
|---|---|
| `status` | Removido da interface, API, exportação e registros novos. |
| `observacoes` | Removido dos assuntos. A observação existe somente nos backups. |

---

## 🔎 Pesquisa e Paginação

<table>
  <tr>
    <td bgcolor="#E8F3FF">
      <h3>🔎 Pesquisa</h3>
      <p>Filtra registros por <strong>responsável</strong> ou <strong>assunto</strong>.</p>
    </td>
    <td bgcolor="#F3E8FF">
      <h3>📄 Paginação</h3>
      <p>Controla a quantidade de registros exibidos na tela.</p>
    </td>
    <td bgcolor="#EFFFF4">
      <h3>📊 Resumo</h3>
      <p>Mostra total de registros, filtrados e páginas.</p>
    </td>
  </tr>
</table>

### 🔢 Itens por página

- 10
- 25
- 50
- 100
- Todos

---

## 🛠️ Administração

As ações administrativas só aparecem após autenticação.

### ➕ Cadastrar assunto

Pode ser feito por:

- botão **Adicionar Registro** no menu lateral;
- botão **+ Cadastrar Assunto** acima da tabela.

Campos do formulário:

- **Responsável**
- **Assunto**

> [!IMPORTANT]
> O campo **Assunto** é obrigatório.

### ✏️ Editar assunto

Disponível pelo botão de edição na coluna **Ações**. Permite alterar:

- responsável;
- assunto.

### 🗑️ Excluir assunto

Disponível pelo botão de exclusão na coluna **Ações**.

Antes de excluir, o sistema solicita confirmação para evitar remoção acidental.

---

## 💾 Backup

O backup copia o conteúdo atual de:

```text
data/dados.json
```

para a pasta:

```text
backup/
```

### 📝 Observação do backup

Ao gerar backup, o sistema solicita uma observação curta:

- limite de **30 caracteres**;
- usada para identificar o backup;
- sanitizada para formar o nome do arquivo;
- registrada em `backup/_indice_backups.json`.

### 🧾 Padrão do nome

```text
backup_ANO-MES-DIA_HORA-MINUTO-SEGUNDO_OBSERVACAO.json
```

Exemplo:

```text
backup_2026-05-27_14-45-44_teste.json
```

<table>
  <tr>
    <td bgcolor="#FFF3CD">💡 <strong>Importante</strong></td>
    <td>A observação do backup não é gravada dentro dos assuntos. Ela fica separada no arquivo <code>backup/_indice_backups.json</code>.</td>
  </tr>
</table>

---

## ♻️ Restauração

Ao clicar em **Restaurar Backup**, o sistema:

- 📂 lista os arquivos `backup_*.json`;
- 📝 mostra nome, observação, data de modificação e tamanho;
- ✅ permite escolher o backup desejado;
- ⚠️ pede confirmação antes de restaurar;
- 🧪 valida se o arquivo contém JSON válido;
- 🔁 substitui os dados atuais;
- 🔄 recarrega a tabela.

> [!CAUTION]
> Restaurar um backup substitui o conteúdo atual de `data/dados.json`.

---

## 📤 Exportação HTML

A opção **Exportar** cria uma lista completa em HTML na pasta:

```text
exportados/
```

### 🧾 Padrão do nome

```text
lista_completa_ANO-MES-DIA_HORA-MINUTO-SEGUNDO.html
```

Exemplo:

```text
lista_completa_2026-05-27_14-47-58.html
```

### 🌐 Conteúdo exportado

O HTML exportado acompanha a tabela atual do sistema:

- responsável;
- assunto.

Após exportar, a interface pergunta se o usuário deseja abrir o arquivo em uma nova aba.

---

## 🔌 API Local

Endpoints usados internamente pela interface:

| Método | Endpoint | Função |
|---|---|---|
| `GET` | `/api/dados` | Lista os assuntos. |
| `GET` | `/api/backups` | Lista backups disponíveis. |
| `POST` | `/api/login` | Valida a senha administrativa. |
| `POST` | `/api/dados/criar` | Cria novo assunto. |
| `POST` | `/api/dados/editar` | Edita assunto existente. |
| `POST` | `/api/dados/excluir` | Exclui assunto. |
| `POST` | `/api/backup/criar` | Gera backup. |
| `POST` | `/api/backup/restaurar` | Restaura backup. |
| `POST` | `/api/exportar` | Gera exportação HTML. |

> [!NOTE]
> O uso normal do sistema deve ser feito pela interface web. A API é usada pela própria página.

---

## 🔁 Compatibilidade e Estrutura Automática

Ao iniciar, o sistema garante a estrutura necessária:

| Ação automática | Resultado |
|---|---|
| Cria `data/` | Garante local da base principal. |
| Cria `backup/` | Garante local dos backups. |
| Cria `exportados/` | Garante local das exportações. |
| Cria `_indice_backups.json` | Mantém as observações dos backups. |
| Migra `dados.json` antigo | Copia da raiz para `data/dados.json`, se necessário. |
| Normaliza registros | Remove campos antigos que não pertencem mais aos assuntos. |

---

## 🛡️ Segurança

A autenticação atual é simples e adequada para uso local ou em rede interna controlada.

<table>
  <tr>
    <td bgcolor="#FFE8E8">
      <h3>⚠️ Não recomendado</h3>
      <p>Não exponha este sistema diretamente na internet sem melhorias de segurança.</p>
    </td>
    <td bgcolor="#E8F3FF">
      <h3>🔒 Para ambiente externo</h3>
      <p>Seria necessário implementar usuários, sessões, senha criptografada, HTTPS, logs e permissões.</p>
    </td>
  </tr>
</table>

### 🔐 Melhorias necessárias para internet

- usuários individuais;
- senha criptografada;
- sessão segura no servidor;
- HTTPS;
- logs de auditoria;
- controle de permissões;
- regras de firewall;
- publicação segura.

---

## 🧰 Manutenção Recomendada

| Frequência | Ação |
|---|---|
| Antes de alterações importantes | Gerar backup. |
| Antes do uso real | Alterar a senha padrão. |
| Periodicamente | Copiar backups importantes para local externo. |
| Periodicamente | Testar restauração. |
| Sempre | Evitar editar `data/dados.json` sem backup. |
| Sempre | Preservar `backup/_indice_backups.json`. |

---

## ✅ Resumo Operacional

### 🔎 Para consultar

1. Inicie o sistema.
2. Acesse `http://127.0.0.1:8765`.
3. Use a pesquisa, a paginação e o seletor de itens por página.

### 🔐 Para administrar

1. Abra o menu lateral.
2. Digite a senha administrativa.
3. Use as opções liberadas.

### 💾 Para gerar backup

1. Entre como administrador.
2. Clique em **Backup**.
3. Informe uma observação de até 30 caracteres.
4. Confirme.

### ♻️ Para restaurar backup

1. Entre como administrador.
2. Clique em **Restaurar Backup**.
3. Escolha o arquivo desejado.
4. Confirme a restauração.

### 📤 Para exportar

1. Entre como administrador.
2. Clique em **Exportar**.
3. O sistema salva o HTML na pasta `exportados/`.

---

## 👨‍💻 Desenvolvido por

<div align="center">

### **RM7Tech - Rodrigo de Oliveira Mendonça**

![Autor](https://img.shields.io/badge/RM7Tech-Rodrigo%20de%20Oliveira%20Mendon%C3%A7a-0A66C2?style=for-the-badge)

</div>
