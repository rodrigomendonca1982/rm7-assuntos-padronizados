# RM7-MSG-CMATFN-PY - Versão 2.0.5

## Correções aplicadas

1. O arquivo JSON principal agora fica obrigatoriamente em:

```text
data/dados.json
```

2. Foi removido o campo **Observações** dos assuntos.

3. A observação agora existe somente no backup:

- aparece no modal de backup como **Observação do backup**;
- possui limite de 30 caracteres;
- é gravada no índice `backup/_indice_backups.json`;
- é exibida na listagem de backups para facilitar a identificação.

## Estrutura de pastas

```text
RM7-MSG-CMATFN-PY-V2/
├── backup/
│   └── _indice_backups.json
├── data/
│   └── dados.json
├── docs/
│   └── VERSAO-2.0.md
├── exportados/
├── static/
│   ├── app.js
│   └── style.css
├── index.html
├── server.py
├── iniciar_linux.sh
├── iniciar_windows.bat
└── README.md
```

## Campos dos assuntos

```json
{
  "id": 1,
  "responsavel": "ASS_PDR",
  "assunto": "Registro inicial de exemplo"
}
```

## Backup

Ao gerar backup, o sistema copia o conteúdo de `data/dados.json` para a pasta `backup/`.

A observação do backup não é gravada nos assuntos. Ela fica separada no arquivo:

```text
backup/_indice_backups.json
```

## Compatibilidade

Se existir um `dados.json` antigo na raiz, o sistema copia automaticamente esse arquivo para `data/dados.json` na primeira inicialização e remove campos antigos como `observacoes` ao salvar novamente.


## Correção 2.0.2

- Incluída a base atual enviada pelo usuário em `data/dados.json`, com 51 registros.
- O campo `padrao` foi preservado para identificar o assunto padrão.
- O campo de observação continua existindo somente para backups, no arquivo `backup/_indice_backups.json`.
