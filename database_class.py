from typing import List
import psycopg2
import time
from dataWriter_class import DataWriter

class error_conection(Exception):
    def __init__(self, msg) -> None:
        self.message = f'ERRO ao se conectar ao DB!\n>>{msg}'
        super().__init__(self.message)#classe pai sera iniciada com a 'message', como se fosse um erro
        
class Db:
    def __init__(self, datawriter:DataWriter) -> None:
        self.datawriter = datawriter
        
    def _conexao(self,type_conect) -> List:
        try:
            if type_conect == 'server':
                connection_data = psycopg2.connect(host = '', database = '', user = '', password = '', port = 5432) 
            elif type_conect == 'local':
                connection_data = psycopg2.connect(host = 'localhost', database = 'postgres', user = 'postgres', password = '123456', port = 5432) 
            cur = connection_data.cursor()
        except Exception as erro:
            #connection_data.rollback()
            self._print_msg('RAISE -----------')
            raise error_conection(erro) 
        else:
            return connection_data, cur
        
    def execute_script(self, sql) -> str:
        connection_data, cur = self._conexao('local')
        try: 
            cur.execute(sql)
            connection_data.commit()
            return 'Ok'
        except Exception as erro_sql:
            connection_data.rollback()
            return 'Erro'

    def _print_msg(self,msg) -> None:
        print(msg)
        self.datawriter._write_row(msg)
        
    def psql_export(self, sql,arq) -> None:
        start_time = time.time()
        connection_data, cur = self._conexao('server')
        outputquery = f"COPY ({sql}) TO STDOUT WITH CSV DELIMITER ','"#HEADER
        self._print_msg(f'---Exportação iniciada: {sql}')
        with open(f"/etc/smb_files/rotinas/rotina_data_export_import/{arq}", "w",encoding="utf-8") as f:
            cur.copy_expert(outputquery, f)
        self._print_msg(f'---Exportação finalizada -> Tempo decorido: {round(time.time() - start_time,2)} segundos')
        cur.close()
        connection_data.close()
        
    #csv deve conter permissão para todos acessarem -> https://stackoverflow.com/questions/54031813/i-am-trying-to-copy-a-file-but-getting-error-message   
    def psql_import(self, tabela,arq):
        start_time = time.time()
        self._print_msg(f'---Importação iniciada: {tabela}')
        sql = f'''
copy {tabela} 
FROM '/etc/smb_files/rotinas/rotina_data_export_import/{arq}' 
DELIMITER ',' CSV;
'''
        connection_data, cur = self._conexao('local')
        cur.execute(f'truncate table {tabela};')
        cur.execute(sql)
        connection_data.commit()
        cur.close()
        connection_data.close()
        self._print_msg(f'---Importação finalizada -> Tempo decorido: {round(time.time() - start_time,2)} segundos')
        self._print_msg('-'*50)
        
        
    
        
