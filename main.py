from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivy import platform

class Bullet(Image):
    def __init__(self,**kwargs):
        super().__init__(self,**kwargs)
        self.source = "assets/images/bullet.png"
        self.size_hint = (None, None)

class MainScreen(MDScreen):
    ...

class GameScreen(MDScreen):
    fps = 60
    ship_speed = 5
    bullet_speed = 10

    def __init__(self,**kwargs):
        super().__init__(self, **kwargs)
        self.keys = {"left": False, "right": False, "fire": False}
        self.bullets = []
        self.game_event = None

    def on_enter(self, *args):
        self.game_event = Clock.schedule_interval(self.update, 1 / self.fps)

    def on_leave(self, *args):
        if self.game_event:
            self.game_event.cancle()

    def update(self, dt):
        ship = self.ids.ship

        if self.keys["left"] and ship.x > 0:
            ship.x -= self.ship_speed

        if self.keys["right"] and ship.right < Window.width:
            ship.x += self.ship_speed

        for bullet in self.bullets[:]:
            bullet.y += self.bullet_speed
            if bullet.y > Window.heigth:
                self.ids.front.remove_widget(bullet)
                self.bullets.remove(bullet)

    def fire(self):
        bullet = Bullet()

        bullet.center_x = self.ids.ship.center_x
        bullet.y = self.ids.ship.top
        self.ids.ship.front.add_widget(bullet)
        self.bullets.append(bullet)


class ShooterApp(MDApp):
    def build(self):
        self.theme_cls.theme_style ="Dark"
        self.theme_cls.primary_pallet = "Gray"

        self.sm = MDScreenManager()

        self.sm.add_widget(MainScreen(name="main"))
        self.sm.add_widget(MainScreen(name="game"))

        return self.sm

if platform != "android":
    Window.size = (450,900)
    Window.top = 100
    Window.left = 600

app = ShooterApp()
app.run()