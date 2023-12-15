import smtplib

# CREATE FAKE SMTP SERVER on OSX:
#  sudo python3 -m smtpd -n -c DebuggingServer localhost:25


# EHLO/HELO (SMTP Greeting):
server = smtplib.SMTP('smtp.example.com', 25)
server.ehlo() # or server.helo() for non-extended greeting

# MAIL FROM (Sender's Address):
from_address = 'sender@example.com'
server.sendmail(from_address, 'recipient@example.com', 'DATA command content')

# RCPT TO (Recipient's Address):
to_address = 'recipient@example.com'
server.sendmail(from_address, to_address, 'DATA command content')

#  DATA (Start of Email Content):
server.sendmail(from_address, to_address, 'DATA\\r\\nSubject: Test Subject\\r\\n\\r\\nThis is the message body')

#  QUIT (End the Session):
server.quit()
