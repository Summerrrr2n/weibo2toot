import yagmail


def SendEmail(fromAD, passport, toAD, host, subject, contents):
    yag = yagmail.SMTP(fromAD, passport, host=host)
    yag.send(toAD, subject, contents)

