from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import re

app = Flask(__name__)

@app.route('/consultar-nif', methods=['POST'])
def consultar_nif():
    try:
        data = request.get_json()
        nif = data.get("nif")

        if not nif:
            return jsonify({"erro": "NIF não fornecido"}), 400

        imagem = Image.open("erro_na_consulta.png")
        texto = pytesseract.image_to_string(imagem, lang="por")
        texto = texto.replace("\n", " ").replace("  ", " ")

        dados = {
            "nome": re.search(r"Nome:\s*(.*?)\s*Tipo:", texto),
            "tipo": re.search(r"Tipo:\s*(.*?)\s*Estado:", texto),
            "estado": re.search(r"Estado:\s*(.*?)\s*Regime de IVA:", texto),
            "regime_iva": re.search(r"Regime de IVA:\s*(.*?)(Residente|Fale|CONTRIBUINT|$)", texto),
        }

        for k in dados:
            dados[k] = dados[k].group(1).strip() if dados[k] else "❌ Não encontrado"

        return jsonify(dados)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
