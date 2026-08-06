# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 19:30:02 2026

@author: ap4an
"""
import os
import requests
import yfinance as yf

ativos = [
    {"ticker": "VOW3.DE", "nome": "Volkswagen", "moeda": "€"},
    {"ticker": "TTWO", "nome": "Take-Two Interactive", "moeda": "$"},
    {"ticker": "SXR8.DE", "nome": "S&P 500", "moeda": "€"},
    {"ticker": "NQSE.DE", "nome": "Nasdaq", "moeda": "€"},
    {"ticker": "EGLN.L", "nome": "Ouro", "moeda": "$"},
    {"ticker": "ISLN.L", "nome": "Prata", "moeda": "$"},
    {"ticker": "IB1T.DE", "nome": "Bitcoin", "moeda": "€"},
]

linhas_geral = []
linhas_destaque = []

for item in ativos:
    try:
        dados = yf.Ticker(item["ticker"]).history(period="5d")
        
        if len(dados) >= 2:
            preco_atual = dados["Close"].iloc[-1]
            preco_anterior = dados["Close"].iloc[-2]
            var_pct = ((preco_atual - preco_anterior) / preco_anterior) * 100
            sinal = "📈" if var_pct >= 0 else "📉"

            linha = f"{sinal} **{item['nome']}** (`{item['ticker']}`): {preco_atual:.2f} {item['moeda']} ({var_pct:+.2f}%)"
            linhas_geral.append(linha)

            # Se a variação for de +3% ou mais, ou -3% ou menos (grande oscilação)
            if abs(var_pct) >= 3.0:
                icone_alerta = "🔥 OPORTUNIDADE/SUBIDA" if var_pct > 0 else "💥 QUEDA BRUSCA"
                linhas_destaque.append(
                    f"• {icone_alerta}: **{item['nome']}** variou **{var_pct:+.2f}%** ({preco_atual:.2f} {item['moeda']})"
                )

        else:
            linhas_geral.append(f"⚠️ **{item['nome']}**: Sem dados recentes")
    except Exception:
        linhas_geral.append(f"❌ **{item['nome']}**: Erro a carregar")

# Montar a mensagem final
mensagem = ["📊 **Resumo Diário do Portefólio**\n"]

# Se houver algum ativo com variação >= 3%, cria a secção especial no topo
if linhas_destaque:
    mensagem.append("🚨 **GRANDES MOVIMENTOS (≥ 3%)** 🚨")
    mensagem.extend(linhas_destaque)
    mensagem.append("\n" + "─"*30 + "\n")

mensagem.extend(linhas_geral)
texto_final = "\n".join(mensagem)

# Enviar para o Discord
webhook_url = os.getenv("DISCORD_WEBHOOK")

if webhook_url:
    payload = {"content": texto_final}
    response = requests.post(webhook_url, json=payload)
    print("Enviado com sucesso!" if response.status_code == 204 else f"Erro: {response.status_code}")
else:
    print("DISCORD_WEBHOOK não configurado.")




