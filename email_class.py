from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from abc import ABC, abstractclassmethod

class SendEmail(ABC):
    @abstractclassmethod
    def __init__(self,final_time) -> None:
        self.final_time = final_time
        
    
    def EmailNapp(self, frase):
        me = 'scripts_mike_teste@gmail.com'#E-mail de envio
        you = ['mike-william98@hotmail.com','mwdoop98@gmail.com'] #E-mail de recebimento
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Rotina Export/import tables"
        msg['From'] = 'rotinas_inteligencia@nappsolutions.com' 
        msg['To'] = 'mike-william98@hotmail.com,mwdoop98@gmail.com'#E-mail de recebimento
        text = frase
        html = f"""\
        <html>
        <head></head>
        <body>
            <font face="Courier New, Courier, monospace">{frase}<br></font>
        </body>
        </html>
        """
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('scripts_mike_teste@gmail.com', '123456')
        
        for email in you:
            mail.sendmail(me, email, msg.as_string())
        mail.quit()

class SendEmailAssert(SendEmail):
    def __init__(self,arq_log) -> None:
        self.arq_log = arq_log
        
    
    def menssege(self) -> str:
        #time.sleep(1)
        with open(f'{self.arq_log}.txt', 'r',encoding = 'utf-8') as arq:
            return  arq.readlines()  
        
    @property
    def edit_log_for_html(self) -> str:
            texto = ''
            texto_log = self.menssege()
            for line in texto_log:
                if 'ERROR' in line:
                    texto += f'<font color="red"> {line}'
                else:
                    texto += line
            if 'ERROR' in texto:
                texto = f'<h1><font color="red"> ERRO AO EXECUTAR EXPORTACAO/IMPORTACAO! </h1><br> </font> {texto}'
            else:
                texto = f'<h1><font color="green"> SUCESSO AO EXECUTAR TODAS AS EXPORTACOES e IMPORTACOES! </h1><br> </font> {texto}'
            return '<b>' + texto.replace('\n', '<br>')
        
    
class SendEmailError(SendEmail):
    def __init__(self, error , final_time) -> None:
            self.error = error
            super().__init__(final_time)
        
    