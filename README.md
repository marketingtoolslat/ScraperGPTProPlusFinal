# 🚀 ScraperGPTProPlusFinal

**ScraperGPT Pro++** es una herramienta de scraping inteligente + análisis + dashboard, desarrollada para analizar campañas de Facebook Ads y generar insights accionables de forma automatizada.

---

## ✅ ¿Qué hace esta herramienta?

- 🔎 Scrapea dinámicamente URLs o IDs de Facebook Ads Library
- 🧠 Detecta idioma, país, fecha, CTA, estilo de copy, nicho, formato
- 📈 Filtra anuncios con múltiples variantes (3+ activos)
- 📤 Exporta automáticamente resultados a:
  - `resultados.csv`
  - Google Sheets (opcional)
- 📊 Muestra gráficos de:
  - Distribución por nicho
  - Estilo de copy
  - Formato (corto, medio, largo)
- 🧩 Preparado para conectarse con GPTs como **Modelator 3060L KN**

---

## 🧪 ¿Cómo usarlo?

1. **Deploy automático** en [https://render.com](https://render.com)
   - Ya viene listo con `render.yaml`
2. Al abrir la app, verás:
   - Campo para pegar múltiples IDs o URLs
   - Resultados tabulados + gráficos
3. Los datos también se guardan en `resultados.csv` (y en Google Sheets si lo configurás)

---

## 🛠 Tecnologías

- Python 3
- Gradio (UI)
- Playwright (scraping dinámico)
- BeautifulSoup (parsing)
- Pandas + Matplotlib (análisis)
- GSpread (export a Sheets)

---

## ⚙ Configuración Opcional (Google Sheets)

1. Crea un archivo `gspread_credentials.json`
2. Agregalo a Render (desde el panel Environment → Files)
3. Asegurate de crear un Google Sheet llamado `ScraperGPT_Resultados`

---

## 🧩 Integraciones futuras

- Sincronización con GPT personalizado: **Modelator 3060L KN**
- Generación automática de creatividades a partir de datos scrapeados
- Export en formato JSON o API para desarrolladores

---

## 📄 Licencia

MIT — libre para usar, modificar y mejorar.
