#!/usr/bin/env python
import os
from datetime import datetime

from flask_migrate import Migrate, MigrateCommand
from flask_rq import get_connection
from flask_script import Manager
from rq import Connection, Queue, Worker
from rq_scheduler import Scheduler
from rq_scheduler.utils import setup_loghandlers

from app import create_app, db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def fetch_fresh_data():
    """Fetch data from hackernews"""
    from app.tasks import fetch_data
    fetch_data()


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    setup_general()


@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin user."""
    pass


@manager.command
def start_fetching():
    scheduler = Scheduler(connection=get_connection())
    from app.tasks import fetch_data
    scheduler.schedule(
        scheduled_time=datetime.utcnow(),
        func=fetch_data,
        interval=int(60),
        repeat=None
    )


@manager.command
def stop_fetching():
    scheduler = Scheduler(connection=get_connection())
    for j in scheduler.get_jobs():
        scheduler.cancel(j)


@manager.command
def restart_fetching():
    stop_fetching()
    start_fetching()


@manager.command
def run_worker():
    """Initializes a rq task queue."""
    listen = ['default']
    with Connection(get_connection()):
        worker = Worker(map(Queue, listen))
        worker.work(with_scheduler=False)


@manager.command
def run_scheduler():
    """rq-scheduler for periodic tasks"""
    if app.debug:
        setup_loghandlers('DEBUG')
    scheduler = Scheduler(connection=get_connection(), interval=30)
    scheduler.run()


if __name__ == '__main__':
    manager.run()
