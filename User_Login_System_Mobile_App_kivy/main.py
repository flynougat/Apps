from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import json, glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    
    def login(self, uname, pword):
        with open ("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_done"
        else:
            self.ids.longin_wrong.text = "Incorrect user name or password."

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json", "r") as file:
            users = json.load(file)
        users[uname] = {'username': uname, 'password': pword, 'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_done"
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        
class SignUpDone(Screen):
    def go_to_login(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class LoginDone(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    def get_quote(self, feel):
        feel = feel.lower()
        available_feeling = glob.glob("mood/*txt")
        available_feeling = [Path(filename).stem for filename in available_feeling]
        if feel in available_feeling:
            # f = open(f"mood/{feel}.txt")
            with open(f"mood/{feel}.txt", encoding="utf8") as file:
                mood = file.read().splitlines()
            self.ids.quote.text = random.choice(mood)
        else:
            self.ids.quote.text = "Unique mood, try another"

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()