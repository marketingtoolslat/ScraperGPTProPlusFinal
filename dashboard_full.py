from playwright.sync_api import sync_playwright
import gradio as gr

def scrape_url(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        title = page.title()
        browser.close()
        return f"Título de la página: {title}"

demo = gr.Interface(fn=scrape_url, inputs="text", outputs="text", title="ScraperGPT Pro++")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=10000)
