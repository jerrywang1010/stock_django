import urllib
from yahoo_fin.stock_info import get_analysts_info, get_data, tickers_sp500
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from smtplib import SMTP
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import matplotlib

import io
import urllib
import base64
matplotlib.use('TkAgg')


price_dict = {}


def draw_company_stock_price(company_name, duration):
    if company_name == "" or duration is None:
        return
    print(f'searching {company_name} stock price')
    # get stock price
    try:
        daily_price = get_data(company_name, interval='1d')['close']
    except:
        assert False, "get price date failed, probably fucked up comany name"

    # draw stock price
    # fig = plt.figure()
    if duration == 'YTD':
        plt.title(f'{company_name} YTD')
        plt.plot(daily_price[-365: -1])
    elif duration == 'MTD':
        plt.title(f'{company_name} MTD')
        plt.plot(daily_price[-30: -1])
    elif duration == 'ALL':
        plt.title(f'{company_name} HISTORICAL')
        plt.plot(daily_price)
    else:
        assert False, "something fucked up in duration"
    plt.ylabel("$USD")
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri


def clear_graph():
    plt.cla()
    return


def send_email(email_address):
    assert email_address.find('@') != -1 or email_address.find('com') != -1, "fucked up email address"

    message = MIMEMultipart()

    text_content = MIMEText('大笨蛋', 'plain', 'utf-8')
    message['From'] = Header('王大锤', 'utf-8')
    message['To'] = Header('大笨蛋', 'utf-8')
    message['Subject'] = Header('中笨蛋', 'utf-8')
    message.attach(text_content)

#     for id, t in enumerate(ticker_list):
#         with open('C:\\Users\\jerry\\Downloads\\{}.png'.format(t), 'rb') as f:
#             mime = MIMEBase('image', 'png', filename='{}.png'.format(t))
#             mime.add_header('Content-Disposition',
#                             'attachment', filename='img1.png')
#             mime.add_header('X-Attachment-Id', str(id))
#             mime.add_header('Content-ID', '<{}>'.format(str(id)))
#             mime.set_payload(f.read())
#             encode_base64(mime)
#             message.attach(mime)

    with open(r'C:\Users\jerry\stock_django\stock_website\stock_price\static\stock_price\frog.jpg', 'rb') as f:
        mime = MIMEBase('image', 'png', filename='黄鱼.png')
        mime.add_header('Content-Disposition',
                        'attachment', filename='黄鱼.png')
    
        mime.set_payload(f.read())
        encode_base64(mime)
        message.attach(mime)

    sender = 'jerrywang1010@gmail.com'
    receivers = [email_address]
    smtper = SMTP('smtp.gmail.com:587')
    # 请自行修改下面的登录口令
    smtper.ehlo()
    smtper.starttls()
    smtper.login(sender, 'wang0815')
    smtper.sendmail(sender, receivers, message.as_string())
    print('邮件发送完成!')
