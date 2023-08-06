import click
import uvicorn

from app import make_app


@click.command(
    'run', help='Run development server locally(DEVELOPMENT SERVER)'
)
def site_dev_run():
    app = make_app()
    uvicorn.run(
        app, log_level=app.app_config.server.LOGLEVEL,
        port=app.app_config.server.PORT,
        host=app.app_config.server.HOST
    )
