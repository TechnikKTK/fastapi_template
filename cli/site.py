import click
import uvicorn

from app import app


@click.command(
    "run", help="Run development server locally(DEVELOPMENT SERVER)"
)
def site_dev_run():
    uvicorn.run(
        app,
        log_level=app.config.server.LOGLEVEL,
        port=app.config.server.PORT,
        host=app.config.server.HOST,
    )
