import time
import os
import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def log_report(tema):
    """Registra o envio em um arquivo markdown para o relatório semanal."""
    try:
        tz_brasilia = pytz.timezone('America/Sao_Paulo')
        data_br = datetime.datetime.now(tz_brasilia)
        data_formatada = data_br.strftime("%d/%m/%Y %H:%M")
        
        dia_semana = data_br.strftime("%A")
        dias = {
            'Monday': 'Segunda-feira', 'Tuesday': 'Terça-feira', 'Wednesday': 'Quarta-feira',
            'Thursday': 'Quinta-feira', 'Friday': 'Sexta-feira', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
        }
        dia_pt = dias.get(dia_semana, dia_semana)
        
        if not os.path.exists("RELATORIO_SEMANAL.md"):
            with open("RELATORIO_SEMANAL.md", "w", encoding="utf-8") as f:
                f.write("# 📝 Relatório de Envios - Briefing Safety\n\n")
                f.write("| Data e Hora | Dia da Semana | Tema Selecionado | Status |\n")
                f.write("| :--- | :--- | :--- | :--- |\n")
        
        with open("RELATORIO_SEMANAL.md", "a", encoding="utf-8") as f:
            f.write(f"| {data_formatada} | {dia_pt} | {tema} | ✅ Enviado |\n")
        print(f"✅ Relatório atualizado com sucesso: {tema}")
    except Exception as e:
        print(f"⚠️ Erro ao atualizar relatório: {e}")

def run_automation():
    NOME = "Max Millian Matheus Pereira de Sales"
    PLACA = "qux5f90"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 20)
        
        print("Acessando o formulário...")
        driver.get("https://forms.gle/PdgvP4GyG3UWWZYM9")
        
        # 1. Nome e Placa
        print("Preenchendo dados...")
        campos_texto = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="text"]')))
        if len(campos_texto) >= 2:
            campos_texto[0].send_keys(NOME)
            campos_texto[1].send_keys(PLACA)
        else:
            raise Exception(f"❌ Esperado 2 campos de texto, encontrado {len(campos_texto)}")
        
        # 2. Selecionar o tema (último da lista)
        print("Selecionando tema...")
        dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="listbox"]')))
        dropdown.click()
        
        opcoes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="option"]')))
        if opcoes:
            tema_escolhido = opcoes[-1]
            nome_tema = tema_escolhido.text
            tema_escolhido.click()
        else:
            raise Exception("❌ Nenhuma opção de tema encontrada")
        
        # 3. Avaliar 5 estrelas
        print("Selecionando 5 estrelas...")
        estrela_5 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="radio"][aria-label="5"]')))
        estrela_5.click()
        
        # 4. Enviar
        print("Enviando formulário...")
        botao_enviar = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button']//span[contains(text(), 'Enviar') or contains(text(), 'Submit')]")))
        botao_enviar.click()
        
        time.sleep(3)
        if "Sua resposta foi registrada" in driver.page_source or "Your response has been recorded" in driver.page_source:
            print(f"🚀 Sucesso: {nome_tema}")
            log_report(nome_tema)
        else:
            print("⚠️ Falha na confirmação visual, mas o envio pode ter funcionado.")
            log_report(f"{nome_tema} (sem confirmação)")
            
    except TimeoutException as e:
        print(f"❌ Timeout: Elemento não encontrado em tempo hábil - {e}")
    except NoSuchElementException as e:
        print(f"❌ Elemento não encontrado: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    finally:
        if driver:
            driver.quit()
            print("🔒 Navegador fechado")

if __name__ == "__main__":
    run_automation()