#!/usr/bin/env python

import click

from gemini import commands


@click.group()
def cli():
    pass

@cli.command()
def upgrade():
    commands.upgrade()

@cli.command()
def rollback():
    commands.rollback()

@cli.command()
@click.option('--runtime', '-r', help='Specify the language runtime to use')
@click.option('--message', '-m', help='A few words to help identify the migration')
def migrate(runtime, message):
    commands.migrate(runtime_key=runtime, message=message)

@cli.command()
@click.argument('runtime')
def setup(runtime):
    commands.setup(runtime)

@cli.command()
@click.option('--runtime', '-r', help='Specify the language runtime to use')
def dryrun(runtime):
    commands.dryrun(runtime)


if __name__ == '__main__':
    cli()
