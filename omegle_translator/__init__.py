import googletrans
from selenium import webdriver
import json
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException,UnexpectedAlertPresentException,InvalidSessionIdException,WebDriverException
from selenium.webdriver.common.by import By
from httpcore._exceptions import ConnectTimeout,ConnectError,ReadError,ReadTimeout
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions  
import time
import threading
from io import StringIO
import sys
import WConio2 as w
from googletrans import Translator
import os


class Omegle_Translator():

    def __init__(self):
        self.b = Bcolors()
        self.translator = Translator()
        self.google_lang_json = googletrans.LANGUAGES
        self.exception_s = (NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException,UnexpectedAlertPresentException)
        self.exceptions_http = (ConnectTimeout,ConnectError,ReadError,ReadTimeout)
        self.user_lang,self.stranger_lang  = self.change_language()
        self.stranger_status_active=False
        self.taking_input = False
        self.interreption = False
        self.input_text=''
        self.total_number_of_outputs = 0
        self.stranger_last_message = ''
        self.open = False

    def get_cwd(self):
        return os.path.dirname(os.path.abspath(__file__))
         
    def change_language(self):
        print(self.b.purple_text('Here is the list of language CODE corresponding to their languages respectively.'))
        print(json.dumps(self.google_lang_json, indent=4, sort_keys=True))

        return self.get_user_lang(), self.get_stranger_lang()

    def get_change_command(self,text):

        try:

            inp=text.split('(')
            change = inp[0]
            usr_lang = inp[1].split(',')[0]
            str_lang = inp[1].split(',')[1].split(')')[0]

            return change,usr_lang,str_lang

        except Exception:
            return '_','_','_'

    def get_input(self):
        i = self.total_number_of_outputs

        while True:
            print()
            input_key = w.getkey()

            if self.total_number_of_outputs!=i and self.taking_input:
                self.interreption = True


        

            if input_key == '\010':
                self.input_text = self.input_text[:-1]
                self.delete_last_line()
                print(self.b.blue_text('You:'),self.b.white_text(self.input_text),end="")
                continue
            if input_key =="\r":
                if self.input_text == '':
                    continue
                break
            self.input_text +=input_key
            self.delete_last_line()
            print(self.b.blue_text('You:'),self.b.white_text(self.input_text),end="")




        return self.input_text 

    def delete_last_line(self):
        "Use this function to delete the last line in the STDOUT"

        #cursor up one line
        sys.stdout.write('\x1b[1A')

        #delete last line
        sys.stdout.write('\x1b[2K')
        self.total_number_of_outputs -=1

    def check_language_code(self,dict,key):
        if key in dict.keys():
            pass
            return True
        else:
            print(key,"is invalid,please re-enter the correct Language Code")
            return False

    def print_instructions(self):
        self.b = Bcolors()
        print(f"{self.b.BOLD}",self.b.green_text("NEW Conversation Started."))
        print(self.b.yellow_text('Type \'exit()\' to exit the chat.'))
        print(self.b.yellow_text('Type \'change()\' to change the language.'))
        print(self.b.yellow_text('Type \'change(a,b)\',where \'a\' means user lang code and \'b\' means stranger lang code '))
        print(self.b.yellow_text('Type \'kill()\' to exit the chat.'))

    def get_user_lang(self):
        while True:
            print(f"{self.b.WARNING}Select your language CODE:{self.b.WARNING}",end="")
            self.user_lang = input()
            if self.check_language_code(self.google_lang_json,self.user_lang):
                print()
                return self.user_lang

    def get_stranger_lang(self):
        while True:
            print(f"{self.b.WARNING}Select Stranger's language CODE:{self.b.WARNING}",end="")
            self.stranger_lang = input()
            if self.check_language_code(self.google_lang_json,self.stranger_lang):
                print()
                return self.stranger_lang

    def trans_from_user_to_stranger(self,text):
        text_to_translate = self.translator.translate(
            text,
            src = self.user_lang,
            dest = self.stranger_lang
        )
        return text_to_translate.text

    def trans_from_stranger_to_user(self,text):
        text_to_translate = self.translator.translate(text,
            src = self.stranger_lang,
            dest = self.user_lang
        )
        
        return text_to_translate.text

    def open_chat_webpage(self):
        while True:
            try:
                self.taking_input=True
                self.interreption = False
                self.input_text = ''
                self.stranger_last_message = ''
                chromedriver = os.path.join(self.get_cwd(),'chromedriver')
                try:
                    if not self.open:
                        print(self.b.purple_text('Opening Chrome....'))
                        self.driver = webdriver.Chrome(chromedriver)
                        self.open = True
                    else:
                        print(self.b.purple_text('Chrome Already Opened....'))

                except WebDriverException:
                    print(self.b.purple_text('You need to download chrome driver extension as per your chrome version from https://chromedriver.chromium.org/downloads ,and paste the extension in the directory {}'.format(self.get_cwd())))
                    time.sleep(0.6)
                    break

                website = "https://www.omegle.com"
                self.driver.get(website)
                self.stranger_status_active = True

                self.total_number_of_outputs = 0


                start_chat_text = WebDriverWait(self.driver,50).until(
                            EC.presence_of_element_located((By.ID,'textbtn'))
                        )
                start_chat_text.click()
                return self.driver
            except self.exception_s as e:
                print(self.b.purple_text('Please Wait'))
                self.input_text = ''
                time.sleep(0.4)

    def get_stranger_text(self):
        while True:
            try:
                stranger_messages_list = self.driver.find_elements_by_class_name('strangermsg')
                status_log_list = self.driver.find_elements_by_class_name('statuslog')
                if len(stranger_messages_list)>0:
                    if self.stranger_last_message != stranger_messages_list[-1].text.split('Stranger:')[-1]:
                        if self.interreption:
                            self.delete_last_line()
                            print(self.b.red_text('Stranger:'),self.b.white_text(self.trans_from_stranger_to_user(stranger_messages_list[-1].text.split('Stranger:')[-1])))
                            print(f'{self.b.FAIL}')
                            print(self.b.blue_text('You:'),self.b.white_text(self.input_text),end="")
                            self.stranger_last_message = stranger_messages_list[-1].text.split('Stranger:')[-1]
                        else:
                            print(self.b.red_text('Stranger:'),self.b.white_text(self.trans_from_stranger_to_user(stranger_messages_list[-1].text.split('Stranger:')[-1])))
                            self.stranger_last_message = stranger_messages_list[-1].text.split('Stranger:')[-1]


                if self.stranger_status_active:
                    break
            except self.exception_s as e:
                self.input_text = ''
                print(self.b.purple_text('Waiting for stranger\'s message'))
            
            except InvalidSessionIdException:
                break

            except self.exceptions_http:
                continue

    def start_chatting(self):

        while True:
            try:
                if self.stranger_status_active:
                    stranger_thread = threading.Thread(target=self.get_stranger_text)
                    stranger_thread.start()
                    self.stranger_status_active = False


                body = WebDriverWait(self.driver,50).until(
                    EC.presence_of_element_located((By.TAG_NAME,'body'))
                    )
                textarea = WebDriverWait(self.driver,50).until(
                    EC.presence_of_element_located((By.TAG_NAME,'textarea'))
                    )
                new_connection = self.driver.find_element_by_class_name('disconnectbtn')
                send = self.driver.find_elements_by_tag_name('button')[1]
                textarea.click()
                
                self.last_message_by_user =''

                print(f"{self.b.FAIL}",end="")

                self.taking_input = True
                text_entered = self.get_input()
                self.taking_input = False
                self.delete_last_line()
                try:
                    if body.get_attribute('class') == 'inconversation':
                        pass

                    else:
                        print(f"{self.b.WARNING}DISCONNECTED!!")
                        self.total_number_of_outputs +=1
                        print("Connecting.....")
                        self.total_number_of_outputs +=1
                        if stranger_thread.is_alive():
                            self.stranger_status_active = True
                            stranger_thread.join()
                        self.print_instructions()
                        self.total_number_of_outputs +=1
                        new_connection.click()
                        self.input_text=''
                        time.sleep(0.506)
                        continue

                except self.exception_s as e:
                    print(self.b.purple_text('Please only type,when the cursor blinks,in the text area of the omegle website'))
                    time.sleep(0.256)
                    break 

                if text_entered == 'exit()':
                    new_connection.click()
                    new_connection.click()
                    new_connection.click()
                    self.stranger_status_active = True
                    stranger_thread.join()
                    self.print_instructions()
                    self.input_text=''
                    self.total_number_of_outputs +=1

                if text_entered == 'change()':
                    self.user_lang,self.stranger_lang=self.change_language()  
                    text_entered = 'Please, wait.'

                change,usr_lang,str_lang = self.get_change_command(text_entered)

                if change == 'change':
                    if self.check_language_code(self.google_lang_json,usr_lang) and self.check_language_code(self.google_lang_json,str_lang):
                        self.user_lang =usr_lang
                        self.stranger_lang = str_lang
                        print(
                            self.b.purple_text(
                                'Language changed to {} for user and {} for stranger'.format(self.google_lang_json[usr_lang],
                                                                                            self.google_lang_json[str_lang]))
                            )
                        text_entered = 'Please, wait.'
                    else:
                        print(self.b.purple_text('Invalid command'))

                if text_entered == 'kill()':
                    print(self.b.red_text('Exiting the chat,closing the program.....'))
                    killed = True
                    break



                
                textarea.send_keys(self.trans_from_user_to_stranger(text_entered))
                print(self.b.blue_text('You:'),self.b.green_text(text_entered))
                self.total_number_of_outputs +=1
                message_entered_by_user=''
                send.click()
                self.input_text=''
                self.last_message_by_user = text_entered
            except self.exception_s as e:
                self.input_text = ''
                print(self.b.purple_text('Please only type,when the cursor blinks,in the text area of the omegle website'))
                time.sleep(0.3)

    def start(self):
        self.driver = self.open_chat_webpage()
        self.print_instructions()
        self.start_chatting()
        print(self.b.red_text('Program Closed'))
        self.driver.close()
        print(f"{self.b.ENDC}")

                  




class Bcolors():

    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'
        
    def red_text(self,text):
        return f'{self.FAIL}'+text
    def blue_text(self,text):
        return f'{self.OKBLUE}'+text
    def green_text(self,text):
        return f'{self.OKGREEN}'+text
    def yellow_text(self,text):
        return f'{self.WARNING}'+text
    def purple_text(self,text):
        return f'{self.HEADER}'+text
    def white_text(self,text):
        return f'{self.ENDC}'+text
    def bold_text(self,text):
        return f'{self.BOLD}'+text
    def underline_text(self,text):
        return f'{self.UNDERLINE}',text




