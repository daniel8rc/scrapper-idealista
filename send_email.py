import smtplib
import json


from io import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email import charset as Charset
from email.generator import Generator
from email.utils import COMMASPACE, formatdate, formataddr

class Mail():
    def __init__(self, data, search):
        self.data = data
        self.search = search

    def send(self):
        sender = 'daniel8rc-pisos@gmail.com'
        receivers = ['daniel8rc@gmail.com']
        raw_data = json.dumps(self.data, indent=4, sort_keys=True)

        subject = u'[PISOS] - %s (%s€, %sm2)' % (self.data['title'], str(self.data['prize']), str(self.data['meters']))
        recipient = 'daniel8rc@gmail.com'
        from_address = 'daniel8rc-pisos@gmail.com'

        message = """
            <html>
                <body>
                    <h1>%s</h1>
                    <img src="%s" height="225" width="300" alt="" style="visibility: visible;">
                    <p>%s</p>
                    <p>Fecha: %s</p>
                    <p>Precio: %s</p>
                    <p>Metros: %s</p>
                    <p>Planta: %s</p>
                    <p>Url: %s</p>
                    <p>
                        Inmobiliaria: %s
                        Link: %s
                    </p>
                    <br/><br/><br/><br/><br/>
                    <pre>%s</pre>
                </body>
            </html>
        """ %(
            self.data['title'],
            str(self.data['image']),
            str(self.data['description']),
            str(self.data['date']),
            str(self.data['prize']),
            str(self.data['meters']),
            str(self.data['floor']),
            str(self.data['url_element']),
            str(self.data['real_estate_title']), str(self.data['real_estate_link']),
            raw_data)

        Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')

        multipart = MIMEMultipart('alternative')
        multipart['Subject'] = subject
        multipart['To'] = formataddr(('Recipient',recipient))
        multipart['From'] = formataddr(('Daniel Scrapper',from_address))

        htmlpart = MIMEText(message.encode('utf-8'), 'html', 'UTF-8')
        multipart.attach(htmlpart)
        
        io = StringIO()
        g = Generator(io, False) # second argument means "should I mangle From?"
        g.flatten(multipart)


        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, receivers, io.getvalue())         
            print("Successfully sent email")
        except SMTPException:
            print("Error: unable to send email")
