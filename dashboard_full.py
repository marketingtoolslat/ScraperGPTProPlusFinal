import gradio as gr

def dummy_scraper(url):
    return "Scraping realizado sobre: " + url

demo = gr.Interface(
    fn=dummy_scraper,
    inputs="text",
    outputs="text",
    title="ScraperGPT Pro++"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=10000)
