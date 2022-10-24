import os
import datetime

class DataTypeNotSuportedForIngestionExcepition(Exception):
    def __init__(self, data) -> None:
        self.data = data
        self.message = f'Func >> Data type {type(data)} is not supported for ingestion'
        super().__init__(self.message)#classe pai sera iniciada com a 'message', como se fosse um erro
        
class DataWriter:
    def __init__(self, filename:str) -> None:
        self.filename = filename
        self.path = str(f'{os.path.dirname(os.path.abspath(__file__))}/logs/{filename}_{str(datetime.datetime.now()).replace(" ","_"). replace(".", "_").replace(":", "_")}')
        #self.path = str(f'{os.path.dirname(os.path.abspath(__file__))}\\logs\\{filename}_{str(datetime.datetime.now()).replace(" ","_"). replace(".", "_").replace(":", "_")}')
        #f'/etc/smb_files/rotinas/rotina_executa_sql/logs/{filename}_{str(datetime.datetime.now()).replace(" ","_"). replace(".", "_").replace(":", "_")}'
            
    def _write_row(self, row:str) -> None:
        if isinstance(row, str):
            with open(f'{self.path}.txt', 'a+',encoding='utf-8') as file:
                file.write(row  + '\n')
        else:
            raise DataTypeNotSuportedForIngestionExcepition(row)