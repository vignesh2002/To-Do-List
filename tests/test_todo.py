# tests/test_todo.py

from typer.testing import CliRunner

from todo import __app_name__, __version__, cli

runner = CliRunner()

def test_version():                                                 # defines first unit test for testing application version
    result = runner.invoke(cli.app, ["--version"])                  # calls .invoke() on runner to run the application with the --version option.
    assert result.exit_code == 0                                    # sserts that the application’s exit code (result.exit_code) is equal to 0 to check that the application ran successfully.
    assert f"{__app_name__} v{__version__}\n" in result.stdout      # asserts that the application’s version is present in the standard output, which is available through result.stdout.