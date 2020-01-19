from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand

from app import db, Config, create_app, models
from app.config import DevelopmentConfig
from app.models import user_model, post_model
from app.common.consts import *

app = create_app(DevelopmentConfig)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, models=models)


manager.add_command("runserver", Server(host="0.0.0.0", port=5000))
manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command('db', MigrateCommand)


def create_roles():
    existing_role_names = []
    roles = user_model.Role.query.all()
    for role in roles:
        if role.name not in ROLES:
            db.session.delete(role)
        else:
            existing_role_names.append(role.name)

    for role in ROLES:
        if role not in existing_role_names:
            db.session.add(user_model.Role(name=role))

    db.session.commit()


def create_categories():
    existing_categories_names = []
    categories = post_model.Category.query.all()
    for category in categories:
        if category.name not in CATEGORIES:
            db.session.delete(category)
        else:
            existing_categories_names.append(category.name)

    for category in CATEGORIES:
        if category not in existing_categories_names:
            db.session.add(post_model.Category(name=category))

    db.session.commit()


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade

    # migrate database to latest revision

    upgrade()
    create_roles()
    create_categories()


if __name__ == '__main__':
    manager.run()
