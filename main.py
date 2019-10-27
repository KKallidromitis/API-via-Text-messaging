import smtplib
import time
import imaplib
import email
import os
import send_mms

#Parameters
sender = 'dialogue.cornell@gmail.com'#
password = "*****" #Placeholder for password

sender_num ='6467278169'
sender_c = 'tmobile'
name = "K"

SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 587

carriers = { 'att':'@mms.att.net',
    'tmobile':'@tmomail.net',
    'verizon':'@vtext.com',
    'sprint':'@page.nextel.com',
    'gmail':'@gmail.com', }

contacts = {sender_c:sender_num}



#Code
def read():
    iter=[]
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(sender,password)
    mail.select('inbox')
    type, data = mail.search(None,'(FROM +1'+sender_num+'@mailmymobile.net)')
    for num in data[0].split():
        type, data = mail.fetch(num, '(RFC822)')
        raw=data[0][1].decode('utf-8')
        msg = email.message_from_string(raw)
        i=0
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            sent = str(part.get_payload(decode=True))
            a=sent.find('align="left">')+13
            b=sent[a:].find('</td></tr>')
            result = sent[a:a+b]
            iter.append(result)
            break
    return iter

body = 'server running'
send_mms.main(sender_c,sender_num,carriers,sender,name,body)
overall = read()
print(overall)

while 1:
    iter = read()
    if len(iter)> len(overall):
        print("Command Detected") #Online <min> , Offline
        cmd = iter[-1:]
        if cmd[0][:6]== "Online":
            body="I am available for the next "+cmd[0][6:]+" mins"
            send_mms.main(sender_c,sender_num,carriers,sender,name,body) #self+others
            send_mms.main('tmobile','9292505668',carriers,sender,name,body)
            send_mms.main('tmobile','8287129345',carriers,sender,name,body)
            send_mms.main('att','3326003251',carriers,sender,name,body)
        elif cmd[0]=="Offline":
            if iter[-2][:6]== "Online":
                body="I am offline"
                send_mms.main(sender_c,sender_num,carriers,sender,name,body) #self
            else:
                body="Invalid Offline command, first go Online."
                send_mms.main(sender_c,sender_num,carriers,sender,name,body) #self
        else:
            body="Command not Recognized"
            send_mms.main(sender_c,sender_num,carriers,sender,name,body) #self
        overall=iter
    else:
        print("API idle")
    time.sleep(1)

#https://docs.python.org/2/library/imaplib.html
