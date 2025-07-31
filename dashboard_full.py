import gradio as gr
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import csv
import gspread
import pandas as pd
import matplotlib.pyplot as plt
from oauth2client.service_account import ServiceAccountCredentials
import os

# Configuración de Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SHEET_NAME = "ScraperGPT_Resultados"

def connect_to_sheets():
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("gspread_credentials.json", SCOPE)
        client = gspread.authorize(creds)
        return client.open(SHEET_NAME).sheet1
    except Exception as e:
        print("Google Sheets no conectado:", e)
        return None

sheet = connect_to_sheets()

# Funciones de inferencia
def infer_nicho(text):
    text = text.lower()
    if any(k in text for k in ["copywriter", "copywriting", "vendas"]): return "Copywriting"
    if any(k in text for k in ["tráfego", "ads", "facebook ads"]): return "Tráfego Pago"
    if any(k in text for k in ["mentoria", "lançamento", "curso"]): return "Infoproductos"
    if any(k in text for k in ["emagrecer", "peso", "nutrição"]): return "Salud / Fitness"
    if any(k in text for k in ["espiritualidad", "energía", "meditación"]): return "Espiritualidad"
    return "Otro"

def infer_estilo(text):
    text = text.lower()
    if any(w in text for w in ["tú", "sientes", "transformación"]): return "Emocional"
    if any(w in text for w in ["resultado", "método", "hecho"]): return "Racional"
    return "Mixto"

def infer_formato(text):
    l = len(text)
    return "Copy Largo" if l > 400 else "Copy Corto" if l < 100 else "Copy Medio"

# Scraping
def scrape_facebook_ad(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0",
                "Accept-Language": "es-ES,es;q=0.9"
            })
            page.goto(url, timeout=60000)
            page.wait_for_timeout(3000)
            page.mouse.wheel(0, 2000)
            content = page.content()
            browser.close()

        soup = BeautifulSoup(content, "html.parser")
        text = soup.get_text(separator=" ").lower()
        title = soup.title.string.strip() if soup.title else "Sin título"
        cta = "saiba mais" if "saiba mais" in text else "Otro"
        fecha = re.findall(r"(\d{1,2} de .*? de \d{4})", text)
        idioma = "Portugués" if "brasil" in text else "Desconocido"
        pais = "Brasil" if "brasil" in text else "Otro"
        total_ads = text.count("impresiones")

        if total_ads < 3:
            return None

        data = {
            "titulo": title,
            "cta": cta,
            "fecha": fecha[0] if fecha else "Desconocida",
            "idioma": idioma,
            "pais": pais,
            "nicho": infer_nicho(text),
            "estilo": infer_estilo(text),
            "formato": infer_formato(text),
            "anuncios_activos": total_ads,
            "texto_visible": text[:1000]
        }

        with open("resultados.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

        if sheet:
            sheet.append_row(list(data.values()))

        return list(data.values())
    except Exception as e:
        return [f"Error: {e}"] + [""] * 9

# Análisis y visualización
def load_visual():
    if not os.path.exists("resultados.csv"):
        return None, None, None, None
    df = pd.read_csv("resultados.csv")

    fig1, ax1 = plt.subplots()
    df["nicho"].value_counts().plot(kind="bar", ax=ax1, title="Nicho")
    fig2, ax2 = plt.subplots()
    df["estilo"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax2, title="Estilo")
    fig3, ax3 = plt.subplots()
    df["formato"].value_counts().plot(kind="barh", ax=ax3, title="Formato")

    return df, fig1, fig2, fig3

# Batch scraping + dashboard
def full_run(input_text):
    urls = [line.strip() for line in input_text.strip().split("\n") if line.strip()]
    results = []
    for url in urls:
        if url.isdigit():
            url = f"https://www.facebook.com/ads/library/?id={url}"
        result = scrape_facebook_ad(url)
        if result:
            results.append(result)
    df, fig1, fig2, fig3 = load_visual()
    return df, fig1, fig2, fig3

demo = gr.Interface(
    fn=full_run,
    inputs=gr.Textbox(label="Pega IDs o URLs (uno por línea)", lines=10),
    outputs=[
        gr.Dataframe(label="Resultados"),
        gr.Plot(label="Gráfico por Nicho"),
        gr.Plot(label="Gráfico por Estilo"),
        gr.Plot(label="Gráfico por Formato")
    ],
    title="ScraperGPT Pro++ FINAL (Todo en Uno)",
    description="Scrapea + Exporta + Visualiza desde un solo panel"
)

demo.launch(server_name="0.0.0.0", server_port=10000)
