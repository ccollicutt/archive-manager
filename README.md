[![Build Status](https://travis-ci.com/ccollicutt/archive-manager.svg?branch=master)](https://travis-ci.com/ccollicutt/archive-manager)

# Archive Manager

Manage files in directories in a backup root directory. It will ensure the total size of all the files in the directories are less than a maximum size, but will always keep the minimum number of files. Once the total size is ensured, it will then delete files until the maximum number of files exist.

The assumption is that some other process, such as a backup script, is generating "archives" in a directory or directories. `archive-manager` will help to manage those files to ensure that there is always room for the most recent backup file.

## Requirements

* This will probably only run on Linux

## Installation

Future releases will include installation via pip and RPM.

```bash
virtualenv archive-manager-venv
. archive-manager-venv/bin/activate
pip install archive-manager
```

Now that it's installed, the `archive-manager` command should be available.

```bash
$ which archive-manager
<venv>/bin/archive-manager
```

## Usage

By default `archive-manager` looks for its config file in `/etc/archive-manager/config.yml`. It does not require any options to run, and can simply be executed by `archive-manager`.

Options:

```bash
$ archive-manager --help
Usage: archive-manager [OPTIONS] COMMAND [ARGS]...

  Manage size and number of files in a set of directories

Options:
  -c, --config TEXT  Config file location
  -v, --verbose      Set to verbose mode
  --help             Show this message and exit.
```

## Configuration File

There is an [example configuration](config.yml.example) file in this repository. All of the options in the example file are required.

```bash
mkdir /etc/archive-manager
cp config.yaml.example /etc/archive-manager/config.yml
vi /etc/archive-manager/config.yml #edit file to suit requirements
```

## Test

### Unit Tests

`make test` will run the available unit tests.