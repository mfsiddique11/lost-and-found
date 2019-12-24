from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from app import db, Config, create_app

app = create_app(Config)
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("runserver", Server(host="0.0.0.0", port=5000))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade

    # migrate database to latest revision
    upgrade()


if __name__ == '__main__':
    manager.run()
