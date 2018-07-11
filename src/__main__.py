import click
import get as get_package
import put as put_package
import watch as watch_package
import utils
from os import system
from click import echo
from config import VERSION
from container import Container


@click.group()
def get_group():
    pass


@get_group.command()
@click.argument('key', required=True)
@click.argument('path', required=True)
@click.option('--code/--no-code', default=True, help='get code source')
@click.option('--result/--no-result', default=True, help='get result')
@click.option('--unzip/--no-unzip', default=False, help='unzip input')
def get(key, path, code, result, unzip):
    if code:
        get_package.Get(key).get(path, unzip)
    if result:
        get_package.Get(key, 'result').get(path, unzip)


@click.group()
def put_group():
    pass


@put_group.command()
@click.argument('key', required=True)
@click.argument('path', required=True)
@click.option('--folder/--no-folder', default=True, help='upload directory')
@click.option('--code/--no-code', default=False, help='upload code')
@click.option('--result/--no-result', default=False, help='put result')
def put(key, path, folder, code, result):
    if code:
        put_package.Put(key).put(path, folder)
    if result:
        put_package.Put(key, 'result').put(path, folder)


@click.group()
def watch_group():
    pass


@watch_group.command()
@click.option('-k', '--key')
@click.option('-t', '--time', default=10, help='loop time (s)')
def watch(key, time):
    watch_package.Watch(key, time).watch()


@click.group()
def init_group():
    pass


@init_group.command()
def init():
    utils.init_environment()


@click.group()
def upgrade_group():
    pass


@upgrade_group.command()
def upgrade():
    system('pip install --upgrade eubh --no-cache-dir')


@click.group()
def version_group():
    pass


@version_group.command()
def version():
    echo(VERSION)


@click.group()
def container_group():
    pass


@container_group.command()
@click.argument('key', required=True)
@click.option('--lists/--no-lists', default=False, help='list container name')
@click.option('--log', help='Get the container log')
def container(key, lists, log):
    if lists:
        Container(key).lists()
    elif log:
        Container(key).log(log, is_watch=True)


cli = click.CommandCollection(
    sources=[get_group, put_group, watch_group, init_group, upgrade_group, version_group, container_group])


def main():
    cli()


if __name__ == "__main__":
    cli()
