import importlib


class AppHandler:
    def __init__(self, **apps):
        self.appNames = apps.keys()
        for appName in self.appNames:
            app = importlib.import_module(f'piassistant.app.{appName}')
            app = app.App(**apps[appName])
            setattr(self, appName, app)
