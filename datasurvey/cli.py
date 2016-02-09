#!/usr/bin/python
import click
import logging

from datasurvey.store import Store
from datasurvey.auction import scan_path

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('alembic').setLevel(logging.WARNING)
logging.getLogger('dataset').setLevel(logging.WARNING)


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--target', type=click.File('w'), default='-',
              help="Output to file")
@click.option('--progress', is_flag=True, help="Show scanning progress")
def main(path, target, **options):
    store = Store()
    scan_path(store, None, path)
    store.save(target)


if __name__ == "__main__":
    main()
