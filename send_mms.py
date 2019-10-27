import smtplib,time

def send(message,receiver,sender):
    password = "*****" #Placeholder for password
    auth = (sender, password)
    server = smtplib.SMTP("smtp.gmail.com", 587 )
    server.starttls()
    server.login(auth[0], auth[1])
    server.sendmail(auth[0], receiver, message)
    server.quit()
    return



def main(c,number,carriers,sender,name,body):
    name = name+"'s update:"
    receiver = number+carriers[c]
    message = ("From: %s\r\n" % sender + "To: %s\r\n" % receiver + "Subject: %s\r\n" % name + "\r\n" + body)
    send(message,receiver,sender)
    return
