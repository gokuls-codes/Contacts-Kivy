from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

import requests

# helper_text: "test"
# helper_text_mode: "on_focus"

login_url = "https://contaxmanagerapp.herokuapp.com/dj-rest-auth/login/"
register_url = "https://contaxmanagerapp.herokuapp.com/dj-rest-auth/registration/"

loader = """
<LoginScreen>:
    name: 'login'
    MDTextField:
        id: username
        hint_text: "Username"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.65}
        multiline: False
    MDTextField:
        id: password
        hint_text: "Password"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.55}
        multiline: False
    MDRectangleFlatButton:
        text: "Login"
        font_size: '18sp'
        pos_hint: {'center_x':0.4, 'center_y':0.45}
        on_release: app.login(username.text, password.text)
    MDRectangleFlatButton:
        text: "Register"
        font_size: '18sp'
        pos_hint: {'center_x':0.6, 'center_y':0.45}
        on_release: app.register_screen()
<ContactsScreen>:
    name: 'list'
    MDLabel:
        text: "CONTACTS LIST"
<RegisterScreen>:
    name: 'register'
    MDTextField:
        id: username
        hint_text: "Username"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.75}
        multiline: False
    MDTextField:
        id: email
        hint_text: "Email"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.65}
        multiline: False
    MDTextField:
        id: password
        hint_text: "Password"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.55}
        multiline: False
    MDTextField:
        id: password2
        hint_text: "Confirm Password"
        font_size: '20sp'
        size_hint: 0.6, None
        pos_hint: {'center_x':0.5, 'center_y':0.45}
        multiline: False
    MDRectangleFlatButton:
        text: "Back"
        font_size: '18sp'
        pos_hint: {'center_x':0.4, 'center_y':0.35}
        on_release: app.back_to_login()
    MDRectangleFlatButton:
        text: "Register"
        font_size: '18sp'
        pos_hint: {'center_x':0.6, 'center_y':0.35}
        on_release: app.register(username.text, email.text, password.text, password2.text)
"""

Builder.load_string(loader)

class LoginScreen(Screen):
    pass

class ContactsScreen(Screen):
    pass

class RegisterScreen(Screen):
    pass

class ContaXApp(MDApp):

    def build(self):
        
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightBlue"
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(ContactsScreen(name='list'))
        self.sm.add_widget(RegisterScreen(name='register'))
        
        return self.sm

    def login(self, uname, pwd):
        self.sm.get_screen('login').ids.username.text = ""
        self.sm.get_screen('login').ids.password.text = ""

        if uname == "" or pwd == "":
            check_string = 'Both Fields are required!'
            close_button = MDFlatButton(text="Close", on_release=self.close_login_dialog)
        else:
            login_data = {
                "username": uname,
                "password": pwd
            }
            response = requests.post(login_url, data=login_data)

            resp = response.json()
            if 'key' in resp:
                check_string = "Successfully Logged In!"
                close_button = MDFlatButton(text="Close", on_release=self.logged_in)
            else:
                check_string = "Invalid credentials!"
                close_button = MDFlatButton(text="Close", on_release=self.close_login_dialog)
            
        self.login_dialog = MDDialog(title ="Login", text=check_string, buttons=[close_button])
        self.login_dialog.open()

    def close_login_dialog(self, obj):
        self.login_dialog.dismiss()

    def logged_in(self, obj):
        self.login_dialog.dismiss()
        self.root.current = 'list'

    def register_screen(self):
        self.root.current = 'register'
    
    def back_to_login(self):
        self.root.current = 'login'

    def register(self, uname, email, pwd, pwd2):
        print(uname, email, pwd, pwd2)
        self.sm.get_screen('register').ids.username.text = ""
        self.sm.get_screen('register').ids.email.text = ""
        self.sm.get_screen('register').ids.password.text = ""
        self.sm.get_screen('register').ids.password2.text = ""

        if uname == "" or pwd == "" or pwd2 == "":
            check_string = 'Required Fields are missing!'
            close_button = MDFlatButton(text="Close", on_release=self.close_register_dialog)
        else:
            register_data = {
                "username": uname,
                "email": email,
                "password1": pwd,
                "password2": pwd2
            }
            response = requests.post(register_url, data=register_data)

            resp = response.json()
            print(resp)
            if 'key' in resp:
                check_string = "Successfully Registered!"
                close_button = MDFlatButton(text="Close", on_release=self.registered)
            else:
                check_string = "Invalid Data!"
                close_button = MDFlatButton(text="Close", on_release=self.close_register_dialog)
            
        self.register_dialog = MDDialog(title ="Register", text=check_string, buttons=[close_button])
        self.register_dialog.open()

        
    def close_register_dialog(self, obj):
        self.register_dialog.dismiss()

    def registered(self, obj):
        self.register_dialog.dismiss()
        self.root.current = 'list'

ContaXApp().run()