from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

@app.route('/consultar_nif', methods=['GET'])
def consultar_nif():
    nif = request.args.get('nif')
    if not nif:
        return jsonify({"status": "erro", "mensagem": "NIF não fornecido"}), 400

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://portaldocontribuinte.minfin.gov.ao/consultar-nif-do-contribuinte")
        time.sleep(3)

        input_field = driver.find_element(By.ID, "j_id_2x:txtNIFNumber")
        input_field.send_keys(nif)
        driver.find_element(By.XPATH, "//button[.//span[text()='Pesquisar']]").click()
        time.sleep(5)

        def extrair(xpath):
            try:
                return driver.find_element(By.XPATH, xpath).text.strip()
            except:
                return ""

        nome = extrair("//label[contains(text(), 'Nome')]/following::div[1]")
        tipo = extrair("//label[contains(text(), 'Tipo')]/following::div[1]")
        estado = extrair("//label[contains(text(), 'Estado')]/following::div[1]")
        regime_iva = extrair("//label[contains(text(), 'Regime de IVA')]/following::div[1]")

        driver.quit()

        if not nome and not tipo:
            return jsonify({"status": "erro", "mensagem": "NIF não encontrado ou página mudou"}), 404
        else:
            return jsonify({
                "status": "ok",
                "nome": nome,
                "tipo": tipo,
                "estado": estado,
                "regime_iva": regime_iva
            })
    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
        import os

   if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render usa uma variável de ambiente PORT
    app.run(host='0.0.0.0', port=port)
