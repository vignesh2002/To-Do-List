"""Entry Point script - Allows you to run the package as an executable program"""
# todo/__main__.py

from todo import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__)     # providing a value to prog_name ensures that your users get the correct app name when running the --help option

if __name__ == '__main__':
    main()