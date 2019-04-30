import click
from . import myshell
from . import myserver


def read_config(ctx, param, value):
    if not value:
        return {}
    import json

    def underline_dict(d):
        if not isinstance(d, dict):
            return d
        return dict((k.replace('-', '_'), underline_dict(v)) for k, v in six.iteritems(d))

    config = underline_dict(json.load(value))
    ctx.default_map = config
    return config


@click.group(invoke_without_command=True)
@click.option('-c', '--config', callback=read_config, type=click.File('r'),
              help='a json file with default values for subcommands. {"webui": {"port":5001}}')
@click.pass_context
def cli(ctx, **kwargs):
    pass

@cli.command()
@click.pass_context
def test(ctx):
    print("test")


@cli.command()
@click.pass_context
def shell(ctx):
    cls = myshell.Shell()
    cls.console({'ctx': ctx})


@cli.command()
@click.pass_context
def server(ctx):
    svr = myserver.Server()
    svr.server()


def main():
    cli()
