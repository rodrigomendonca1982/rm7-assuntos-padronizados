#!/usr/bin/env bash

# ============================================================
# Inicializador Linux - RM7-MSG-CMATFN-PY
# ============================================================
# - Se o servidor já estiver rodando na porta 8765, apenas abre
#   o navegador em uma nova guia/aba.
# - Se a porta estiver livre, inicia o servidor Python e abre
#   automaticamente o navegador.
# ============================================================

cd "$(dirname "$0")"

PORTA=8765
URL="http://127.0.0.1:${PORTA}"

abrir_navegador() {
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$URL" >/dev/null 2>&1 &
  elif command -v sensible-browser >/dev/null 2>&1; then
    sensible-browser "$URL" >/dev/null 2>&1 &
  else
    echo "Abra manualmente no navegador: $URL"
  fi
}

if ss -ltn 2>/dev/null | grep -q ":${PORTA} "; then
  echo "O sistema já está rodando em $URL"
  abrir_navegador
  exit 0
fi

(sleep 1 && abrir_navegador) &
python3 server.py
