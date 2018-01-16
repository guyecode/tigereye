# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask_script import Manager, Server, Shell
# from flask_migrate import MigrateCommand
from tigereye import create_app
from tigereye.extensions import db
from tigereye.models.cinema import Cinema
app = create_app()
manager = Manager(app)


def _make_context():
    from tigereye.models.cinema import Cinema  # noqa
    from tigereye.models.hall import Hall  # noqa
    from tigereye.models.movie import Movie  # noqa
    from tigereye.models.play import Play  # noqa
    from tigereye.models.seat import Seat  # noqa
    from tigereye.models.seat import PlaySeat  # noqa
    from tigereye.models.order import Order  # noqa
    locals().update(globals())
    return dict(**locals())

# Run local server
manager.add_command("runserver", Server("127.0.0.1", port=5000))
manager.add_command("shell", Shell(make_context=_make_context))
# manager.add_command('db', MigrateCommand)



@manager.command
def createdb():
    # from tigereye.models.cinema import Cinema  # noqa
    # from tigereye.models.hall import Hall  # noqa
    # from tigereye.models.movie import Movie  # noqa
    # from tigereye.models.play import Play  # noqa
    # from tigereye.models.seat import Seat  # noqa
    # from tigereye.models.seat import PlaySeat  # noqa
    # from tigereye.models.order import Order  # noqa
    db.create_all()


@manager.command
def dropdb():
    """Deletes the database."""
    # from tigereye.models.cinema import Cinema  # noqa
    # from tigereye.models.hall import Hall  # noqa
    # from tigereye.models.movie import Movie  # noqa
    # from tigereye.models.play import Play  # noqa
    # from tigereye.models.seat import Seat  # noqa
    # from tigereye.models.seat import PlaySeat  # noqa
    # from tigereye.models.order import Order  # noqa
    db.drop_all()


@manager.command
def testdata():
    """create test data."""
    from tigereye.models.cinema import Cinema
    from tigereye.models.movie import Movie
    print('start creating testdata.......')
    Cinema.create_test_data()
    Movie.create_test_data()


@manager.command
def init():
    dropdb()
    createdb()
    testdata()


@manager.command
def auto_unlock():
    app.logger.info('start auto unlock.')
    from tigereye.models.seat import PlaySeat, SeatStatus
    session = db.create_scoped_session()
    rows = session.query(PlaySeat).filter(
        PlaySeat.status == SeatStatus.locked.value,
        PlaySeat.locked_time < datetime.now() - timedelta(
            seconds=app.config['AUTO_UNLOCK_SECONDS'])).update(
                {'status': SeatStatus.ok.value,
                 'orderno': None, },
                synchronize_session=False)
    if rows:
        app.logger.info('auto unlocked %s seats' % rows)
        session.commit()


if __name__ == '__main__':
    manager.run()
