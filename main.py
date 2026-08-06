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
houve_grande_movimento = False

for item in ativos:
    try:
        dados = yf.Ticker(item["ticker"]).history(period="5d")
        
        if len(dados) >= 2:
            preco_atual = dados["Close"].iloc[-1]
            preco_anterior = dados["Close"].iloc[-2]
            var_pct = ((preco_atual - preco_anterior) / preco_anterior) * 100
            sinal = "📈" if var_pct >= 0 else "📉"

            linha = f"{sinal} {item['nome']}: {preco_atual:.2f} {item['moeda']} ({var_pct:+.2f}%)"
            linhas_geral.append(linha)

            # Se variar >= 3%
            if abs(var_pct) >= 3.0:
                houve_grande_movimento = True
                icone_alerta = "🔥 OPORTUNIDADE" if var_pct > 0 else "💥 QUEDA"
                linhas_destaque.append(
                    f"• {icone_alerta}: {item['nome']} ({var_pct:+.2f}%)"
                )
        else:
            linhas_geral.append(f"⚠️ {item['nome']}: Sem dados")
    except Exception:
        linhas_geral.append(f"❌ {item['nome']}: Erro")

# Montar o texto da notificação
mensagem = []

if linhas_destaque:
    mensagem.append("🚨 GRANDES MOVIMENTOS (≥ 3%) 🚨")
    mensagem.extend(linhas_destaque)
    mensagem.append("\n" + "─"*25 + "\n")

mensagem.extend(linhas_geral)
texto_final = "\n".join(mensagem)

# --- ENVIAR NOTIFICAÇÃO PUSH (NTFY.SH) ---
topico_ntfy = os.getenv("NTFY_TOPIC") # Usa o teu nome único do Passo 1

if topico_ntfy:
    # Se houver grande movimento (>=3%), a notificação faz mais barulho/prioridade alta!
    prioridade = "high" if houve_grande_movimento else "default"
    
    requests.post(
        f"https://ntfy.sh/{topico_ntfy}",
        data=texto_final.encode("utf-8"),
        headers={
            "Title": "📊 Mercado & Portefólio",
            "Priority": prioridade,
            "Tags": "chart_with_upwards_trend,moneybag"
        }
    )

# --- OPÇÃO: Manter também o Discord (Opcional) ---
webhook_url = os.getenv("DISCORD_WEBHOOK")
if webhook_url:
    requests.post(webhook_url, json={"content": texto_final})