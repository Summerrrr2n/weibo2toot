import yagmail

# yag = yagmail.SMTP('1147122935@qq.com', 'mobrvipeechsfdjd', host='smtp.qq.com')


# contents = [
#     "This is the body, and here is just text http://somedomain/image.png",
#     "You can find an audio file attached.", '/local/path/to/song.mp3'
# ]
# yag.send('hn1147122935@someone.com', 'Log_PuppyBot', contents)


def SendEmail(fromAD, passport, toAD, host, subject, contents):
    yag = yagmail.SMTP(fromAD, passport, host=host)
    yag.send(toAD, subject, contents)

