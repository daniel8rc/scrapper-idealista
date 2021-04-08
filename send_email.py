import smtplib
import json

class Mail():
    def __init__(self, data, search):
        self.data = data
        self.search = search

    def send(self):
        sender = 'daniel8rc-pisos@gmail.com'
        receivers = ['daniel8rc@gmail.com']
        raw_data = json.dumps(self.data, indent=4, sort_keys=True)
        message = """From: <daniel8rc-pisos@gmail.com>
To: To Person <to@todomain.com>
MIME-Version: 1.0
Content-type: text/html
Subject: [PISOS] - %s (%s€, %sm2)

<h1>%s</h1>
<img src="%s" height="225" width="300" alt="" style="visibility: visible;">
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

        """ %(
            self.search, str(self.data['title']), str(self.data['meters']),
            self.data['title'],
            str(self.data['image']),
            str(self.data['date']),
            str(self.data['prize']),
            str(self.data['meters']),
            str(self.data['floor']),
            str(self.data['url_element']),
            str(self.data['real_estate_title']), str(self.data['real_estate_link']),
            raw_data)

        

        message = message.encode('ascii', 'ignore')
        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, receivers, message)         
            print("Successfully sent email")
        except SMTPException:
            print("Error: unable to send email")
