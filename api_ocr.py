from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract
from PIL import Image
import time
import os

app = Flask(__name__)

@app.route('/ocr/<nif>', methods=['GET'])
def consultar_nif(nif):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        driver.get("https://portaldocontribuinte.minfin.gov.ao/consultar-nif-do-contribuinte")

        wait = WebDriverWait(driver, 15)
        campo_nif = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
        campo_nif.send_keys(nif)

        botao = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Pesquisar')]")))
        botao.click()

        time.sleep(5)  # Ajuste se necessário

        screenshot_path = f"screenshot_{nif}.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()

        # OCR na imagem capturada
        img = Image.open(screenshot_path)
        texto = pytesseract.image_to_string(img, lang='por')
        os.remove(screenshot_path)

        return jsonify({"nif": nif, "resultado": texto.strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
