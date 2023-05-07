import zipfile
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from datetime import date
import os
import configparser

class VisualizationEmailer:
    def __init__(self, configpath):
        config = configparser.ConfigParser()
        config.read(configpath)
        self.zip_path = os.path.join(config.get("OUTPUT", "OUTPUT_PATH"), str(date.today()), str(date.today())) + '.zip'
        self.output_path =  os.path.join(config.get("OUTPUT", "OUTPUT_PATH"), str(date.today()))
        self.user = config.get("EMAIL", "USER")
        self.sender_email = config.get('EMAIL', "SENDER_EMAIL")
        self.sender_pass = config.get('EMAIL', 'SENDER_PASSWORD')
        self.recipient_email = config.get('EMAIL', 'RECIPIENT_EMAIL')
        #self.zip_path = self.output_path + "\\" + str(date.today())
        pass 

    def email_data(self):
        print("Entered email data function \n calling zip data function")
        self.__zip_data__()
        print("File zipped \n Generating email")

        subject = str(date.today()) + " Stocks Candlestick Visualiztaion for {}".format(self.user)

        print('email is {}'.format(self.sender_email))

        with open(self.zip_path, "rb") as attachment:

            part = MIMEBase("application", "octet-stream")
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(self.zip_path)}",
            )

        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = self.sender_email
        message['To'] = self.recipient_email
        html_part = MIMEText("Find Zip Attached")
        message.attach(html_part)
        message.attach(part)


        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(self.sender_email, self.sender_pass)
        server.sendmail(self.sender_email, self.recipient_email, message.as_string())
        server.quit()   
        print("Email has been sent")     
        pass 

    def __zip_data__(self):
        #shutil.make_archive(self.output_path, 'zip', self.zip_path)
        with zipfile.ZipFile(self.zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.output_path):
                for file in files:
                    if '.zip' not in file:
                        zipf.write(os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file),
                        os.path.join(self.output_path, '.')))
        pass
