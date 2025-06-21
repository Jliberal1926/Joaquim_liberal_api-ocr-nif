from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def ocr_image():
    if 'image' not in request.files:
        return jsonify({"erro": True, "mensagem": "Imagem não enviada"}), 400

    image_file = request.files['image']
    caminho = f"/tmp/temp.png"
    image_file.save(caminho)

    try:
        img = Image.open(caminho)
        texto = pytesseract.image_to_string(img, lang='por')

        nome = estado = iva = ""

        if "Nome:" in texto:
            nome = texto.split("Nome:")[1].split("\n")[0].strip()
        if "Estado:" in texto:
            estado = texto.split("Estado:")[1].split("\n")[0].strip()
        if "Regime de IVA:" in texto:
            iva = texto.split("Regime de IVA:")[1].split("\n")[0].strip()

        os.remove(caminho)

        return jsonify({
            "erro": False,
            "nome": nome,
            "estado": estado,
            "regime_iva": iva
        })

    except Exception as e:
        return jsonify({"erro": True, "mensagem": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
