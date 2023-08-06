import click

from cli.site import site_dev_run


@click.group('site', help='Cli for working with server')
def site_group():
    pass


@click.group()
def main_group():
    pass


site_group.add_command(site_dev_run)
main_group.add_command(site_group)


if __name__ == "__main__":
    main_group()
