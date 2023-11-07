import click
import uvicorn

from asgi import application


@click.command(
    "run", help="Run development server locally(DEVELOPMENT SERVER)"
)
def site_dev_run():
    uvicorn.run(
        "asgi:application",
        log_level=application.config.server.LOGLEVEL,
        port=application.config.server.PORT,
        host=application.config.server.HOST,
        reload=True,
    )
