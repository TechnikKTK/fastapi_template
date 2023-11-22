import click

from cli.db import test_connection
from cli.site import site_dev_run


@click.group("db", help="Cli for working with main database")
def db_group():
    pass


@click.group("site", help="Cli for working with server")
def site_group():
    pass


@click.group()
def main_group():
    pass


site_group.add_command(site_dev_run)
db_group.add_command(test_connection)
main_group.add_command(site_group)
main_group.add_command(db_group)


if __name__ == "__main__":
    main_group()
