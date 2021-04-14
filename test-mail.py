# coding: utf-8

# Python's email API is simple and easy to use!!!!!!!!!!!!!!

# Requirements:
# * UTF-8 headers
# * UTF-8 body
# * prefer quoted-printable to base64 transfer-encoding.
# * Don't escape "From" at the beginning of a line in the message - it's not
#   the 1800s any more

from cStringIO import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email import Charset
from email.generator import Generator


subject = u'Hello あ'
recipient = u'Bあb '
from_address = u'Bかb '

html = u'<html><body>Hey böb!\nFrom Jack, I got enhanced pills!</body></html>'
text = u'Hey böb!\nFrom Jack, I got enhanced pills!'

# Override python's weird assumption that utf-8 text should be encoded with
# base64, and instead use quoted-printable (for both subject and body).  I
# can't figure out a way to specify QP (quoted-printable) instead of base64 in
# a way that doesn't modify global state. :-(
Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')


# This example is of an email with text and html alternatives.
multipart = MIMEMultipart('alternative')

# We need to use Header objects here instead of just assigning the strings in
# order to get our headers properly encoded (with QP).
# You may want to avoid this if your headers are already ASCII, just so people
# can read the raw message without getting a headache.
multipart['Subject'] = Header(subject.encode('utf-8'), 'UTF-8').encode()
multipart['To'] = Header(recipient.encode('utf-8'), 'UTF-8').encode()
multipart['From'] = Header(from_address.encode('utf-8'), 'UTF-8').encode()

# Attach the parts with the given encodings.
htmlpart = MIMEText(html.encode('utf-8'), 'html', 'UTF-8')
multipart.attach(htmlpart)
textpart = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
multipart.attach(textpart)

# And here we have to instantiate a Generator object to convert the multipart
# object to a string (can't use multipart.as_string, because that escapes
# "From" lines).

io = StringIO()
g = Generator(io, False) # second argument means "should I mangle From?"
g.flatten(multipart)

# Pass the result of this to your SMTP library of choice.
print io.getvalue()