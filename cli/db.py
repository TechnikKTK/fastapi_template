import click
import sqlalchemy as sa

from asgi import application


@click.command('test-connection', help='Test Db connection')
def test_connection():
    session_class = application.db_sync.session_class
    with session_class() as session:
        session.execute(sa.text('SELECT 1;'))
    print('CONNECTION IS STABLE!')
