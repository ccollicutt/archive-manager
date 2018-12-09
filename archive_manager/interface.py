import click
from archive_manager import ArchiveManager, ArchiveManagerException
from module import get_config
import sys
import os

CONFIG_FILE = "/etc/archive-manager/config.yml"

@click.group(invoke_without_command=True)
@click.option('--config', '-c', required=False, help='Config file location', type=str)
@click.option('--verbose', '-v', required=False, help='Set to verbose mode', is_flag=True)
def cli(config, verbose):
    """Manage size and number of tar.gz files in a set of directories"""

    if config:
        config_file = config
    else:
        config_file = CONFIG_FILE

    # Load the config
    try:
        cfg = get_config(config_file)
    except RuntimeError, err:
        msg = "ERROR: %s" % str(err)
        click.echo(msg, err=True)
        sys.exit(1)
     
    try:
        archive = ArchiveManager(cfg, verbose)
    except ArchiveManagerException, err:
        msg = "ERROR: %s" % str(err)
        click.echo(msg, err=True)
        sys.exit(1)

    for d in archive.backup_dirs:

        try:
            archive.delete_until_size_or_min(d)
        except ArchiveManagerException, err:
            msg = "ERROR: %s" % str(err)
            click.echo(msg, err=True)
            sys.exit(1)

        try:
            archive.keep_max_files(d)
        except ArchiveManagerException, err:
            msg = "ERROR: %s" % str(err)
            click.echo(msg, err=True)
            sys.exit(1)