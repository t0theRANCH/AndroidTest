from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivymd.app import MDApp
from jnius import autoclass, cast, JavaClass, MetaJavaClass
import traceback


class OutputLabel(Image):
    text = StringProperty('')

    def on_text(self, *_):
        l = Label(text=self.text)
        l.font_size = '48dp'
        l.texture_update()
        self.texture = l.texture


class RootWidget(BoxLayout):
    pass


class hnnnng(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Gray"

        try:
            # Get the current activity and context
            # LEAVE THIS HERE
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
            context = cast('android.content.Context', currentActivity.getApplicationContext())
            Intent = autoclass('android.content.Intent')

            # CODE TO DEBUG STARTS HERE

            # Use this label to display desired debug text
            label = OutputLabel(text="")

        # END OF CODE, DISPLAY TRACEBACK
        except Exception:
            t = traceback.format_exc()
            t2 = [t[i:i+50] for i in range(0, len(t), 50)]
            label = OutputLabel(text="\n".join(t2))
        return label


if __name__ == '__main__':
    hnnnng().run()
