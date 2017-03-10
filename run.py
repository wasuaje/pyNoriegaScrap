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
        #self.target_email = "cnoriega68@gmail.com"
        self.target_email = "wasuaje@gmail.com"
        # self.driver = webdriver.PhantomJS(executable_path=r'phantomjs.exe',
        #                                  service_args=[
        #                                      '--ignore-ssl-errors=true',
        #                                      '--ssl-protocol=any'],
        #                                  desired_capabilities=self.dcap)
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.Chrome()
        #self.driver = webdriver.PhantomJS()

        #self.driver.set_window_size(1400, 1000)
        self.driver.set_page_load_timeout(25)
        self.wait = WebDriverWait(self.driver, self.timeout)

    def write_cedula(self):
        self.doscreenshot('after check method click')
        self.driver.get(self.url)
        textbox = self.driver.find_element(By.ID, value='value_pos_cedula_1')
        textbox.send_keys('9411742')

        self.doscreenshot('after input phone number')
        btn = self.driver.find_element(By.ID, value="saveButton1")
        btn.click()
        sleep(0.5)
        checkbox = self.driver.find_element(
            By.ID, value='value_fk_categoria_1_3')
        checkbox.click()
        self.doscreenshot('after input code number')
        hay_citas = "Citas electrónicas" in self.driver.page_source
        print("######### {}".format(hay_citas))
        if hay_citas:
            self.send_email()

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
        #msg = "Mensaje de prueba"
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
s = smtplib.SMTP('smtp.gmail.com', 587)
s.ehlo()
s.starttls()
s.send_message(msg)
s.quit()

    def checkbuy(self, paymethod):
        print(paymethod)
        self.driver.get(self.url)
        self.doscreenshot('main_')

        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'trigger-buy'))).click()

        sleep(0.3)
        self.doscreenshot('after buy click')
        payments = self.driver.\
            find_elements_by_class_name('payment-method-icon')

        for p in payments:
            try:
                alt = p.get_attribute('alt').lower()
            except:
                continue
            if alt == paymethod.lower() and p.is_displayed():
                paybank = p
                break

        # sleep(1)
        paybank.click()
        # login
        sleep(0.3)
        self.loginphone()
        # end login
        sleep(0.3)
        self.doscreenshot('after verifycate phone')
        # press buy
        bt_buys = self.driver.find_elements_by_class_name('buy-go')
        for b in bt_buys:
            if b.get_attribute('class') \
                    .find('place-order') > -1:
                b.click()
                break
        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'unique_ref')))
        self.doscreenshot('End_')
        print('Ok')
        self.driver.delete_all_cookies()

    def checksell(self, sellmethon):
        print(sellmethon)
        self.driver.get(self.url)
        self.doscreenshot('main_')
        self.wait.until(EC.element_to_be_clickable((
            By.CLASS_NAME, 'trigger-sell'))).click()
        self.doscreenshot('after sell click')
        if sellmethon == 'fa-credit-card-alt':
            self.wait.until(EC.element_to_be_clickable((
                By.CLASS_NAME, sellmethon))).click()
            self.wait.until(EC.element_to_be_clickable((
                By.NAME, 'number'))).send_keys('1111')
            self.wait.until(EC.element_to_be_clickable((
                By.CLASS_NAME, 'save-card'))).click()
        elif sellmethon == 'Qiwi wallet':
            self.wait.until(EC.element_to_be_clickable((
                By.CLASS_NAME, 'payment-method-icon')))
            selments = self.driver. \
                find_elements_by_class_name('payment-method-icon')

            for p in selments:
                try:
                    alt = p.get_attribute('alt').lower()
                except:
                    continue
                if alt == sellmethon.lower() and p.is_displayed():
                    sellbank = p
                    break
            sellbank.click()
            self.wait.until(EC.element_to_be_clickable((
                By.CLASS_NAME, 'phone'))).send_keys('1111')
            card_go = self.driver.find_elements_by_class_name('save-card')
            card_go[1].click()
        # cash
        else:
            self.wait.until(EC.element_to_be_clickable((
                By.CLASS_NAME, 'fa-money'))).click()
            sleep(0.5)
            self.driver.find_element_by_class_name('next-step').click()
        # login
        sleep(0.8)
        self.loginphone()
        # end login
        self.wait.until(EC.element_to_be_clickable((
            By.CLASS_NAME, 'sell-go'))).click()
        self.wait.until(EC.element_to_be_clickable((
            By.CLASS_NAME, 'unique_ref')))
        self.doscreenshot('End_')
        print('Ok')
        self.driver.delete_all_cookies()

    def doscreenshot(self, filename):
        if self.issavescreen:
            self.driver.get_screenshot_as_file(
                os.path.join(self.screenpath, filename + '.png'))


if __name__ == '__main__':
    sel = SeleniumTest()
    sel.write_cedula()
