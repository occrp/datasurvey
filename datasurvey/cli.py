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
@click.option('--csv', type=click.File('w'), default=None,
              help="Output to CSV file")
@click.option('--db', type=click.Path(), default=None,
              help="SQLite database location")
def main(path, csv, db, **options):
    store = Store(db)
    scan_path(store, None, path)
    if csv is not None:
        store.save(csv)


if __name__ == "__main__":
    main()
