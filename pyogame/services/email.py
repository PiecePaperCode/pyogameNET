import smtplib
import ssl
import pyogame.services as services
import pyogame.settings as Djangosettings
from email.mime.text import MIMEText


def send_verification(request):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        server.login(services.secrets.EMAIL_USER['user'], services.secrets.EMAIL_USER['password'])

        body = """
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <link rel="shortcut icon" type="image/x-icon" href="https://pyogame.net/static/svg/logo.svg">
                <link rel="stylesheet" type="text/css" href="https://pyogame.net/static/style/base.css">
                <link rel="stylesheet" type="text/css" href="https://pyogame.net/static/style/empire.css">
                <title>Verify your Account</title>
            </head>
            <body>
                <main>
                    <h1>Please verify your Account</h1>
                    <h2>PIN</h2>
                    <div class="whiteborder text_center">
                        <h3>{}</h3>
                    </div>
                    <h4>Enter the PIN in pyogameNET in your Profile Settings</h4>
                </main>
    
            </body>
            </html>
        """.format(services.encryption.hash_pin(request))

        msg = MIMEText(body, 'html')
        msg['Subject'] = 'Hello {} Welcome to Pyogame.net'.format(request.user.username)
        msg['To'] = request.user.email
        msg['From'] = 'pyogameNET@gmail.com'
        server.sendmail('pyogameNET@gmail.com', request.user.email, msg.as_string())
    return True


def send_recovery(user):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        server.login(services.secrets.EMAIL_USER['user'], services.secrets.EMAIL_USER['password'])

        body = """
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <link rel="shortcut icon" type="image/x-icon" href="https://pyogame.net/static/svg/logo.svg">
                <link rel="stylesheet" type="text/css" href="https://pyogame.net/static/style/base.css">
                <link rel="stylesheet" type="text/css" href="https://pyogame.net/static/style/empire.css">
                <title>Recover your Account</title>
            </head>
            <body>
                <main>
                    <h1>Recover your Account</h1>
                    <a href="https://{}/recover/{}">RESET</a>
                </main>

            </body>
            </html>
        """.format(Djangosettings.ALLOWED_HOSTS[0], services.encryption.hash(user))

        msg = MIMEText(body, 'html')
        msg['Subject'] = 'Recovery pyogameNET'.format(user.username)
        msg['To'] = user.email
        msg['From'] = 'pyogameNET@gmail.com'
        server.sendmail('pyogameNET@gmail.com', user.email, msg.as_string())
    return True
