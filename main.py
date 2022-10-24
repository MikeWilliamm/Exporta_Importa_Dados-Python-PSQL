import time
import datetime
from database_class import Db
from dataWriter_class import DataWriter
from email_class import SendEmailAssert

#'/etc/smb_files/rotinas/rotina_data from 35_data to local/logs/export_import_data_2022-08-30_14_37_58_294253'
start_time = time.time()
data_hora_inicio = str(datetime.datetime.now())[:19]
datawriter = DataWriter('export_import_data')
send_email = SendEmailAssert(datawriter.path)
database = Db(datawriter=datawriter)
try:
    #psql_export = base .35
    #psql_import = base local
    print(f'Data hora inicio --> {data_hora_inicio}')
    database.psql_export('select * from sales.stores_sales', 'sales_stores_sales.csv')
    database.psql_import('sales.stores_sales','sales_stores_sales.csv')

    database.psql_export('select * from clientes.data_client', 'clientes_data_cliente.csv')
    database.psql_import('clientes.data_client','clientes_data_cliente.csv')

    database.psql_export('select * from estoque.data_estoque', 'estoque_data_estoque.csv')
    database.psql_import('estoque.data_estoque','estoque_data_estoque.csv')
    
except Exception as erro:
    database._print_msg(f'ERROR Type -> {type(erro)}\nError -> {erro}')
    
finally:
    database._print_msg(f'Tempo total da execução --> {round(time.time() - start_time,2)} segundos')
    data_hora_fim = str(datetime.datetime.now())[:19]
    database._print_msg(f'Data hora início --> {data_hora_inicio}\nData hora fim --> {data_hora_fim}')
    send_email.EmailNapp(send_email.edit_log_for_html)