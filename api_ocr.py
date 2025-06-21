from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)

@app.route('/ocr/<nif>', methods=['GET'])
def consultar_nif(nif):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        driver.get("https://portaldocontribuinte.minfin.gov.ao/consultar-nif-do-contribuinte")

        wait = WebDriverWait(driver, 30)

        campo_nif = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text' and contains(@class, 'form-control')]")))
        campo_nif.clear()
        campo_nif.send_keys(nif)

        botao_pesquisar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Pesquisar')]")))
        botao_pesquisar.click()

        # Espera o painel com os dados aparecer
        painel = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "panel-body")))
        dados_texto = painel.text

        # Processa os dados para extrair nome, estado e regime de IVA
        resultado = {
            "nome": extrair(dados_texto, "Nome:"),
            "estado": extrair(dados_texto, "Estado:"),
            "regime_iva": extrair(dados_texto, "Regime de IVA:"),
        }

        driver.quit()
        return jsonify({"nif": nif, "resultado": resultado})

    except Exception as e:
        driver.save_screenshot("erro_na_consulta.png")
        driver.quit()
        return jsonify({"erro": str(e), "mensagem": "❌ Erro durante a consulta"}), 500

def extrair(texto, campo):
    try:
        inicio = texto.index(campo) + len(campo)
        fim = texto.index("\n", inicio)
        return texto[inicio:fim].strip()
    except:
        return "❌ Não encontrado"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
