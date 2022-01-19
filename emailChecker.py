# modules
import imaplib
import email
import os
from confidential import *
import requests


def latest():
    # https://www.systoolsgroup.com/imap/
    gmail_host = "imap.gmail.com"

    # set connection
    mail = imaplib.IMAP4_SSL(gmail_host)

    # login
    mail.login(username, app_password)

    # select inbox
    mail.select("INBOX")

    # select specific mails
    _, selected_mails = mail.search(None, '(FROM "%s")' % sender)

    # total number of mails from specific user
    mails = selected_mails[0].split()
    mails.sort(key=None, reverse=True)
    num = mails[0]
    # for num in [mails[0]]:  # [selected_mails[0].split()[1]]:
    _, data = mail.fetch(num, "(RFC822)")
    _, bytes_data = data[0]

    # convert the byte data to message
    email_message = email.message_from_bytes(bytes_data)
    return email_message


def retrieveIqaamahTimesDoc(email_message=latest()):
    try:
        lastEmail = "empty"  # requests.get("https://moneyless-gnu-7476.dataplicity.io/mtws-iqaamah-times/email").json()['current email']
    except:
        lastEmail = "-1"
    if lastEmail == email_message["subject"]:
        print("Using previously downloaded: ", lastEmail)
        return lastEmail
    # requests.put("https://moneyless-gnu-7476.dataplicity.io/mtws-iqaamah-times/email",data= "{\"current email\": \"%s\"}"%lastEmail)
    # access data
    # print("Subject: ", email_message["subject"])
    # print("To:", email_message["to"])
    # print("From: ", email_message["from"])
    # print("Date: ", email_message["date"])
    for part in email_message.walk():
        if (
            part.get_content_type() == "text/plain"
            or part.get_content_type() == "text/html"
        ):
            message = part.get_payload(decode=True)
            # print("Message: \n", message.decode())
            # print("==========================================\n")
            # break
            # for part in email_message.walk():
            # this part comes from the snipped I don't understand yet...
        if part.get_content_maintype() == "multipart":
            continue
        if part.get("Content-Disposition") is None:
            continue
        fileName = part.get_filename()
        if not ("Iqaamah Times.docx" in fileName):
            print("No files found")
            exit()
        if bool(fileName):
            filePath = os.path.join("iqaamahdoc", fileName)
            # if not os.path.isfile(filePath) :
            fp = open(filePath, "wb")
            fp.write(part.get_payload(decode=True))
            fp.close()
            subject = email_message[
                "subject"
            ]  # str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
            print(
                'Downloaded "{file}" from email titled "{subject}".'.format(
                    file=fileName,
                    subject=subject,
                )
            )
    return lastEmail


retrieveIqaamahTimesDoc()
