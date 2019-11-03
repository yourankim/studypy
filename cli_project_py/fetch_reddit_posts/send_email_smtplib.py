import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
import configparser

config = configparser.ConfigParser()
config.read('..\prop.config')
section = 'SEND_EMAIL'
smtp_server = config.get(section,'SmtpServer')
port = config.get(section,'Port')
sender_email = config.get(section,'SenderEmail')
password = config.get(section,'Password')
receiver_email = config.get(section, 'ReceiverEmail')
today = date.today().strftime('%Y-%m-%d')


def send_email(text, html):

  message = MIMEMultipart("alternative")
  message["Subject"] = f"{today} reddit best posts"
  message["From"] = sender_email
  message["To"] = receiver_email
  text = text
  html = html

  part1 = MIMEText(text,"plain")
  part2 = MIMEText(html, "html")

  message.attach(part1)
  message.attach(part2)

  context = ssl.create_default_context()

  try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(sender_email, password)

    server.sendmail(sender_email,receiver_email, message.as_string())

  except Exception as e:
    print(e)
  finally:
    print("send email successfully.")
    server.quit()        


# 1차 시도: 메일이 전송은 됐는데 제목으로 쓴 부분이 보낸 사람 이름으로 들어갔다.
# 2차 시도: 예제의 메시지 부분을 그대로 복사해서 보내니 제 자리를 찾아갔다. 아무리 봐도 다른 점은 닫는 쌍따옴표가 내용 바로 뒤어 붙어있다는 점 뿐인데. 그리고 보낸 사람 이름은 여전히 안보임.























