from src.base.base import *

class RobotClass(Bot):
    def __init__(self) -> None:
        self.configs = read_json(CONFIG_PATH)
        self.HEADLESS = self.configs['BOT']['HEADLESS']
        self.DOWNLOAD_FILES = False
        super().__init__(self.HEADLESS, self.DOWNLOAD_FILES)
        self.DF = pd.read_excel(r'base\n_processos.xlsx', dtype=str)

    def run(self):
        for i, row in self.DF.iterrows():
            faz_log(f'Executando processo {i+1} de {len(self.DF)}')
            n_processo = row['n_processo']
            if '8.19' in n_processo:
                uf = 'RJ'
                if DBManager().verify_if_n_processo_exists(n_processo):
                    faz_log(f'  Processo {n_processo} ja existe')
                    continue
                faz_log(f'  Processo: {n_processo}')
                faz_log(f'  UF: {uf}')
                self.DRIVER.get(f"https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica?numProcessoCNJ={n_processo}")
                faz_log(f'Clicando em todos os personagens')
                self.DRIVER.switch_to.frame(espera_elemento(self.WDW, (By.CSS_SELECTOR, 'iframe[id="mainframe"]')))
                try:
                    espera_elemento_sair_do_dom(self.WDW7, (By.CSS_SELECTOR, 'div[class="modal-backdrop fade show"]'))
                except:pass
                try:
                    self.DRIVER.execute_script("""document.querySelector('div[class="modal-backdrop fade show"]').remove()""")
                except:
                    pass
                for ele in espera_e_retorna_lista_de_elementos(self.WDW, (By.CSS_SELECTOR, 'label[role="link"]')):
                    if 'listar todos os personagens' in ele.text.lower():
                        ele.click()
                        break
                faz_log(f'Capturando todos os personagens')
                lines = espera_e_retorna_lista_de_elementos(self.WDW, (By.CSS_SELECTOR, '#lista-personagens[style="display: block;"]>div>div>div~div table >tbody tr'))
                for line in lines:
                    tipo = line.find_element(By.CSS_SELECTOR, 'td').text
                    personagem = line.find_element(By.CSS_SELECTOR, 'td~td').text
                    
                    status = 'Capturado com sucesso!'
                    data_captura = data_e_hora_atual_como_string()
                    DBManager().create_item(n_processo=n_processo, status=status, data_captura=data_captura, uf=uf, tipo=tipo, personagem=personagem)
                else:
                    exportar_tabela_para_usuario('sqlite:///bin/database.db')