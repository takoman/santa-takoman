from flask.ext.script import Manager
from santa import create_app

app = create_app()

manager = Manager(app)

@manager.shell
def make_shell_context():
    return dict(app=app, db=app.db)

if __name__ == "__main__":
    manager.run()
