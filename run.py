from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import sys


class SeleniumTest():

    def __init__(self, *args, **kwargs):
        self.issavescreen = False
        self.url = 'http://citas.panama.org.ve/comprobacion_persona_add.php'
        self.screenpath = os.path.join(
            os.path.dirname(__file__), 'Screenshots')

        if not os.path.exists(self.screenpath):
            os.makedirs(self.screenpath)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64)' \
                     ' AppleWebKit/537.36 (KHTML, like Gecko)' \
                     ' Chrome/37.0.2062.120 Safari/537.36'
        self.dcap = dict(DesiredCapabilities.PHANTOMJS)
        self.dcap["phantomjs.page.settings.userAgent"] = user_agent
        self.timeout = 25
        # self.target_email = "cnoriega68@gmail.com"
        self.target_email = "wasuaje@gmail.com"
        # self.driver = webdriver.PhantomJS(executable_path=r'phantomjs.exe',
        #                                  service_args=[
        #                                      '--ignore-ssl-errors=true',
        #                                      '--ssl-protocol=any'],
        #                                  desired_capabilities=self.dcap)
        # self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.PhantomJS()

        # self.driver.set_window_size(1400, 1000)
        self.driver.set_page_load_timeout(25)
        self.wait = WebDriverWait(self.driver, self.timeout)

    def start_process(self):
        self.doscreenshot('after check method click')
        self.driver.get(self.url)
        textbox = self.driver.find_element(By.ID, value='value_pos_cedula_1')
        textbox.send_keys('9411742')

        # close popup
        content = self.driver.find_elements(By.CLASS_NAME, value='close')
        print(content)
        if len(content) > 0:
            content[0].click()
            sleep(0.3)

        self.doscreenshot('after input phone number')
        btn = self.driver.find_element(By.ID, value="saveButton1")
        btn.click()
        sleep(0.5)

        checkbox = self.driver.find_element(
            By.ID, value='value_fk_categoria_1_3')
        checkbox.click()
        self.doscreenshot('after input code number')
        hay_citas = "CITAS DISPONIBLES" in self.driver.page_source
        # print("######### {}".format(hay_citas))
        if hay_citas:
            data_date = self.driver.find_element(
                By.CLASS_NAME, value='rnr-message')
            # print("#######", data_date.text)
            parsed_date = self.parse_date(data_date.text)
            # print("######### {}".format(parsed_date))
            textbox = self.driver.find_element(
                By.ID, value='value_fecha_cita_1')
            textbox.send_keys(parsed_date)
            btn = self.driver.find_element(By.ID, value="saveButton1")
            btn.click()
            sleep(0.5)
            self.send_email()

    def parse_date(self, text):
        import re
        months = {'ENERO': '01',
                  'FEBRERO': '02',
                  'MARZO': '03',
                  'ABRIL': '04',
                  'MAYO': '05',
                  'JUNIO': '06',
                  'JULIO': '07',
                  'AGOSTO': '08',
                  'SEPTIEMBRE': '09',
                  'OCTUBRE': '10',
                  'NOVIEMBRE': '11',
                  'DICIEMBRE': '12',
                  }
        reg_exp = "([0-9]{2}).*(ENERO|FEBRERO|MARZO|ABRIL|MAYO|JUNIO|JULIO|AGOSTO|SEPTIEMBRE|OCTUBRE|NOVIEMBRE|DICIEMBRE).*([0-9]{4})"
        expresion = re.compile(reg_exp)
        found = expresion.search(text)
        day = found.group(1)
        month = months[found.group(2)]
        year = found.group(3)
        return "{}-{}-{}".format(year, month, day)

    def send_email(self):
        # Import smtplib for the actual sending function
        import smtplib

        # Import the email modules we'll need
        from email.mime.text import MIMEText

        # Open a plain text file for reading.  For this example, assume that
        # the text file contains only ASCII characters.
        # with open(textfile) as fp:
        # Create a text/plain message
        #   msg = MIMEText(fp.read())
        msg = MIMEText("Mensaje de prueba")
        # msg = "Mensaje de prueba"
        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = 'Hay Citas en Panama Venezuela Site'
        msg['From'] = "wuelfhis asuaje"
        msg['To'] = self.target_email

        msg = "\r\n".join([
            "From: user_me@gmail.com",
            "To: user_you@gmail.com",
            "Subject: Just a message",
            "",
            "Why, oh why"
        ])

        # Send the message via our own SMTP server.
        s = smtplib.SMTP('mail.wasuaje.com', 25)
        s.ehlo()
        s.starttls()
        s.send_message(msg)
        s.quit()

    def doscreenshot(self, filename):
        if self.issavescreen:
            self.driver.get_screenshot_as_file(
                os.path.join(self.screenpath, filename + '.png'))


if __name__ == '__main__':

    sel = SeleniumTest()
    sel.start_process()


#"value_fecha_cita_1" = "2017-03-16"
# div class = rnr - message - -> div con citas disponibles
#"saveButton1" -> click
# text= "FECHA SUGERIDA DE ATENCIÓN: MARTES 18 DE ABRIL DE 2017 [16 CITAS
# DISPONIBLES]"
