# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 19:30:02 2026

@author: ap4an
"""
import os
import requests
import yfinance as yf

ativos = [
    {"ticker": "VOW3.DE", "nome": "Volkswagen", "moeda": "€"},        # Corrigido: VOW3.DE
    {"ticker": "TTWO", "nome": "Take-Two Interactive", "moeda": "$"},
    {"ticker": "SXR8.DE", "nome": "S&P 500", "moeda": "€"},           # Adicionado de volta
    {"ticker": "NQSE.DE", "nome": "Nasdaq", "moeda": "€"},
    {"ticker": "EGLN.L", "nome": "Ouro", "moeda": "$"},
    {"ticker": "ISLN.L", "nome": "Prata", "moeda": "$"},             # Corrigido: ISLN.L
    {"ticker": "IB1T.DE", "nome": "Bitcoin", "moeda": "€"},  
]

linhas_mensagem = ["📊 **Resumo Diário do Portefólio**\n"]

for item in ativos:
    try:
        dados = yf.Ticker(item["ticker"]).history(period="5d")
        
        if len(dados) >= 2:
            preco_atual = dados["Close"].iloc[-1]
            preco_anterior = dados["Close"].iloc[-2]
            var_pct = ((preco_atual - preco_anterior) / preco_anterior) * 100
            sinal = "📈" if var_pct >= 0 else "📉"

            linhas_mensagem.append(
                f"{sinal} **{item['nome']}** (`{item['ticker']}`): {preco_atual:.2f} {item['moeda']} ({var_pct:+.2f}%)"
            )
        else:
            linhas_mensagem.append(f"⚠️ **{item['nome']}**: Sem dados recentes")
    except Exception:
        linhas_mensagem.append(f"❌ **{item['nome']}**: Erro a carregar")

texto_final = "\n".join(linhas_mensagem)

webhook_url = os.getenv("DISCORD_WEBHOOK")

payload = {"content": texto_final}
response = requests.post(webhook_url, json=payload)

print("Enviado com sucesso!" if response.status_code == 204 else f"Erro: {response.status_code}")




