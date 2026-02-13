import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_automation():
    # Dados Fixos
    NOME = "Max Millian Matheus Pereira de Sales"
    PLACA = "qux5f90"
    
    # Configurações do Chrome para rodar na nuvem (Headless)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)
    
    try:
        print("Acessando o formulário...")
        driver.get("https://forms.gle/PdgvP4GyG3UWWZYM9")
        
        # 1. Nome do motorista
        print("Preenchendo Nome...")
        campos_texto = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="text"]')))
        campos_texto[0].send_keys(NOME)
        
        # 2. Placa
        print("Preenchendo Placa...")
        campos_texto[1].send_keys(PLACA)
        
        # 3. Selecionar o tema da semana
        # Lógica: Se não houver tema definido, pega o último da lista (geralmente o mais recente)
        print("Selecionando Tema...")
        dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="listbox"]')))
        dropdown.click()
        time.sleep(2)
        
        opcoes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="option"]')))
        # Seleciona a última opção da lista (estratégia para pegar o tema atual)
        opcoes[-1].click()
        print(f"Tema selecionado: {opcoes[-1].text}")
        
        # 4. Avaliar com 5 estrelas
        print("Avaliando com 5 estrelas...")
        estrela_5 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="radio"][aria-label="5"]')))
        estrela_5.click()
        
        # 5. Enviar
        print("Enviando formulário...")
        botao_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Enviar') or contains(text(), 'Submit')]")))
        botao_enviar.click()
        
        # Verificação de Sucesso
        time.sleep(3)
        if "Sua resposta foi registrada" in driver.page_source or "Your response has been recorded" in driver.page_source:
            print("✅ SUCESSO: Formulário enviado com sucesso!")
        else:
            print("⚠️ AVISO: O formulário pode ter sido enviado, mas a mensagem de confirmação não foi detectada.")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_automation()
