import smtplib
import ssl
import os
from email.mime.text import MIMEText
from config import SMTP, BASE_DIR

port        = SMTP["port"]
smtp_server = SMTP["server"]
sender      = SMTP["sender"]
password    = SMTP["password"]
receiver    = SMTP["receiver"]

def get_body(currencies: dict, formatted_date: str):
    template_path = os.path.join(BASE_DIR, "templates", "email_template.html")
    with open(template_path) as f:
        template = f.read()

    rows_html = ""
    for currency, rates in currencies.items():
        rows_html += f"""
            <tr style="background-color: #615e59; color: white; text-align: center;">
                <td style="padding: 20px; border: 1px solid #615e59;" colspan="3"> {currency} </td>
            </tr>
            """
        for rate_name, value in rates.items():
            currencies_parts = rate_name.split('_')
            rows_html += f"""
             <tr style="background-color: #ebebeb; text-align: center;">
                <td style="padding: 10px; border: 1px solid #615e59;"> 1 {currencies_parts[0]} </td>
                <td style="padding: 10px; border: 1px solid #615e59;"> {round(value, 4)} {currencies_parts[1]} </td>
            </tr>
            """

    template = template.replace("{{ rows }}", rows_html)        
    template = template.replace("{{ date }}", formatted_date)
    return template

def send(currencies: dict, formatted_date: str):
    # connect to gmail server
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)
        msg = MIMEText(get_body(currencies, formatted_date), 'html')
        msg["Subject"] = f"Exchange Rates {formatted_date}"
        msg["From"] = sender
        msg["To"] = receiver
        server.sendmail(sender, receiver, msg.as_string())
        print("Email has been sent!")

