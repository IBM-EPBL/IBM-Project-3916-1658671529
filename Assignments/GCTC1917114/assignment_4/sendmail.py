
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import smtplib
from email.message import EmailMessage

def send_data(user):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("ganapriyakheersagar@gmail.com", "..")
    message = ""
    email_content = f"""
                                <html>
                                <head>
                                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                                </head>
                                
                                <body>
                                <div style="flex: 1 1 auto;padding: 1rem 1rem;background-color:#F5DADF;border: 1px solid #a2cce3;border-radius: 0.25rem; " >
                                    <center >
                                    <h3><b>EXPENSE TRACKER APP<b><h3>
                                    
                                    </center>
                                        <p style="margin-bottom: 0.5rem;"><br>Dear {user},<br></p>
                                        <h1>ALERT !!!!</h1>
                                        <p><b>You reached your budget limit. Please check your stats.</b></p>
                                        <br><br>
                                        <center>
                                        Thank you for using our app!
                                        </center>
                                        <br><br>
                                        Regards,<br>EXPENSE TRACKER,<br>2022-2023.</p>
                                    </div>
                                </div>
                                </body>
                                </html>
                                
                                """
    msg = EmailMessage()
    msg['Subject'] = "Alert! Budget limit reached"
    msg['From'] = "ganapriyakheersagar@gmail.com"
    msg['To'] = user
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    



def sendmail(user,text):
    message = Mail(
        from_email='ranj.1917139@gct.ac.in',
        to_emails=user,
        subject="Expense hiked alert",
        html_content=text
        )
    try:
        sg = SendGridAPIClient('')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)



