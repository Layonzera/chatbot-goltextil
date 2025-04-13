from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import fitz  # PyMuPDF

app = FastAPI()

PDF_PATH = "TABELA PREÇOS - Abril Vendedores.pdf"


def buscar_preco_por_codigo(codigo: str):
    doc = fitz.open(PDF_PATH)

    for page in doc:
        text = page.get_text()
        linhas = text.split('\n')
        for i, linha in enumerate(linhas):
            if codigo in linha:
                try:
                    descricao = linhas[i - 1].strip()
                    codigos = linha.strip()
                    preco_avista_atacado = linhas[i + 9].strip().replace(',', '.')
                    preco_avista = linhas[i + 1].strip().replace(',', '.')
                    preco_prazo30 = linhas[i + 3].strip().replace(',', '.')
                    preco_prazo60 = linhas[i + 5].strip().replace(',', '.')
                    preco_prazo75 = linhas[i + 7].strip().replace(',', '.')

                    return f"""🔍 Artigo: {descricao}

💰 Tabela de Preços:
- Prazo 75: R$ {preco_prazo75}
- Prazo 60: R$ {preco_prazo60}
- Prazo 30: R$ {preco_prazo30}
- À vista: R$ {preco_avista}
- À vista atacado: R$ {preco_avista_atacado}

📄 Código(s): {codigos}
"""
                except:
                    return "❌ Erro ao extrair os dados. Verifique se o código está correto."

    return f"❌ Código {codigo} não encontrado no PDF."


@app.get("/preco/{codigo}")
def get_preco(codigo: str):
    return {"resposta": buscar_preco_por_codigo(codigo)}


@app.post("/whatsapp")
async def responder_whatsapp(request: Request):
    form = await request.form()
    mensagem_recebida = form.get("Body")

    if mensagem_recebida and mensagem_recebida.strip().isdigit():
        resposta = buscar_preco_por_codigo(mensagem_recebida.strip())
    else:
        resposta = "❌ Por favor, envie apenas o código do produto. Exemplo: 3090"

    return PlainTextResponse(resposta)
