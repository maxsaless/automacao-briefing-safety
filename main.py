"""
Automação de Preenchimento de Formulário - Briefing Safety

Este script automatiza o preenchimento de um formulário do Google Forms,
selecionando aleatoriamente um tema da lista disponível e registrando
cada envio em um relatório semanal em markdown.

Requisitos:
    - selenium
    - webdriver-manager
    - pytz

Autor: Automação Briefing Safety
Data: 2026
"""

import time
import os
import logging
import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AutomacaoBriefing:
    """Classe responsável pela automação do formulário Briefing Safety."""
    
    def __init__(self, nome, placa, url_formulario):
        """
        Inicializa a automação com credenciais e URL.
        
        Args:
            nome (str): Nome do usuário
            placa (str): Placa do veículo
            url_formulario (str): URL do formulário Google Forms
        """
        self.nome = nome
        self.placa = placa
        self.url_formulario = url_formulario
        self.driver = None
        self.wait = None
        
    def _configurar_driver(self):
        """Configura e inicializa o WebDriver do Chrome com opções headless."""
        try:
            logger.info("Configurando WebDriver Chrome...")
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            logger.info("WebDriver configurado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao configurar WebDriver: {e}")
            return False
    
    def _acessar_formulario(self):
        """Acessa o formulário do Google Forms."""
        try:
            logger.info(f"Acessando formulário: {self.url_formulario}")
            self.driver.get(self.url_formulario)
            time.sleep(3)
            logger.info("Formulário carregado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao acessar formulário: {e}")
            return False
    
    def _preencher_dados(self):
        """Preenche os campos de Nome e Placa do formulário."""
        try:
            logger.info("Preenchendo dados pessoais (Nome e Placa)...")
            
            # Aguarda a presença dos campos de texto
            campos_texto = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="text"]'))
            )
            
            if len(campos_texto) < 2:
                raise Exception(f"Esperado 2 campos de texto, encontrado {len(campos_texto)}")
            
            # Preenche Nome
            campos_texto[0].clear()
            campos_texto[0].send_keys(self.nome)
            logger.info(f"Nome preenchido: {self.nome}")
            
            # Preenche Placa
            campos_texto[1].clear()
            campos_texto[1].send_keys(self.placa)
            logger.info(f"Placa preenchida: {self.placa}")
            
            return True
        except Exception as e:
            logger.error(f"Erro ao preencher dados: {e}")
            return False
    
    def _selecionar_tema(self):
        """Seleciona aleatoriamente um tema da lista disponível."""
        try:
            logger.info("Selecionando tema...")
            
            # Localiza e clica no dropdown de temas
            dropdown = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="listbox"]'))
            )
            dropdown.click()
            time.sleep(1)
            
            # Aguarda as opções carregarem
            opcoes = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="option"]'))
            )
            
            if not opcoes:
                raise Exception("Nenhuma opção de tema encontrada")
            
            # Seleciona a última opção
            ultima_opcao = opcoes[-1]
            tema_selecionado = ultima_opcao.text
            ultima_opcao.click()
            
            logger.info(f"Tema selecionado: {tema_selecionado}")
            time.sleep(1)
            
            return tema_selecionado
        except StaleElementReferenceException:
            logger.warning("Elemento tornou-se obsoleto, tentando novamente...")
            return self._selecionar_tema()
        except Exception as e:
            logger.error(f"Erro ao selecionar tema: {e}")
            return None
    
    def _enviar_formulario(self):
        """Envia o formulário."""
        try:
            logger.info("Enviando formulário...")
            
            # Localiza o botão de envio
            botao_envio = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="button"]'))
            )
            botao_envio.click()
            
            logger.info("Formulário enviado com sucesso")
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"Erro ao enviar formulário: {e}")
            return False
    
    def _registrar_relatorio(self, tema):
        """
        Registra o envio em um arquivo markdown para o relatório semanal.
        
        Args:
            tema (str): Tema que foi selecionado e enviado
        """
        try:
            logger.info(f"Registrando relatório para tema: {tema}")
            
            tz_brasilia = pytz.timezone('America/Sao_Paulo')
            data_br = datetime.datetime.now(tz_brasilia)
            data_formatada = data_br.strftime("%d/%m/%Y %H:%M")
            
            dia_semana = data_br.strftime("%A")
            dias_traducao = {
                'Monday': 'Segunda-feira',
                'Tuesday': 'Terça-feira',
                'Wednesday': 'Quarta-feira',
                'Thursday': 'Quinta-feira',
                'Friday': 'Sexta-feira',
                'Saturday': 'Sábado',
                'Sunday': 'Domingo'
            }
            dia_pt = dias_traducao.get(dia_semana, dia_semana)
            
            # Cria o arquivo se não existir
            if not os.path.exists("RELATORIO_SEMANAL.md"):
                with open("RELATORIO_SEMANAL.md", "w", encoding="utf-8") as f:
                    f.write("# 📝 Relatório de Envios - Briefing Safety\n\n")
                    f.write("| Data e Hora | Dia da Semana | Tema Selecionado | Status |\n")
                    f.write("| :--- | :--- | :--- | :--- |\n")
                logger.info("Arquivo RELATORIO_SEMANAL.md criado")
            
            # Adiciona a entrada
            with open("RELATORIO_SEMANAL.md", "a", encoding="utf-8") as f:
                f.write(f"| {data_formatada} | {dia_pt} | {tema} | ✅ Enviado |\n")
            
            logger.info(f"✅ Relatório registrado: {tema} em {data_formatada}")
        except Exception as e:
            logger.error(f"Erro ao registrar relatório: {e}")
    
    def _fechar_driver(self):
        """Fecha o WebDriver."""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver fechado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao fechar WebDriver: {e}")
    
    def executar(self):
        """Executa a automação completa."""
        try:
            logger.info("=" * 50)
            logger.info("Iniciando automação Briefing Safety")
            logger.info("=" * 50)
            
            # Configura o driver
            if not self._configurar_driver():
                return False
            
            # Acessa o formulário
            if not self._acessar_formulario():
                return False
            
            # Preenche os dados
            if not self._preencher_dados():
                return False
            
            # Seleciona o tema
            tema = self._selecionar_tema()
            if not tema:
                return False
            
            # Envia o formulário
            if not self._enviar_formulario():
                return False
            
            # Registra no relatório
            self._registrar_relatorio(tema)
            
            logger.info("=" * 50)
            logger.info("✅ Automação concluída com sucesso!")
            logger.info("=" * 50)
            return True
            
        except Exception as e:
            logger.error(f"Erro durante a execução: {e}")
            return False
        finally:
            self._fechar_driver()


def main():
    """Função principal."""
    # Credenciais via variáveis de ambiente
    NOME = os.getenv("BRIEFING_NOME", "Max Millian Matheus Pereira de Sales")
    PLACA = os.getenv("BRIEFING_PLACA", "qux5f90")
    URL_FORMULARIO = os.getenv("BRIEFING_URL", "https://forms.gle/PdgvP4GyG3UWWZYM9")
    
    # Cria instância e executa
    automacao = AutomacaoBriefing(NOME, PLACA, URL_FORMULARIO)
    sucesso = automacao.executar()
    
    # Retorna código de saída apropriado
    return 0 if sucesso else 1


if __name__ == "__main__":
    exit(main())