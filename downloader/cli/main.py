# Copyright (c) 2022 Helltraitor <helltraitor@hotmail.com>
#
# This file is under MIT License (see full license text in music-downloader-py/LICENSE file)
"""This module represents entry point of cli implementation via `click` package.

This module is not designed for using by other applications, packages,
libraries, modules or scripts. But it is possible (see examples).

This module contains `main` function that is the entry application point.
Other functions must not be used.

Examples:
    Example of typical using

    >>> from downloader import cli
    >>>
    >>>
    >>> if __name__ == "__main__":
    >>>     cli.main()

    Example of debugging

    >>> from click.testing import CliRunner
    >>>
    >>> from downloader import cli
    >>>
    >>>
    >>> if __name__ == "__main__":
    >>>     runner = CliRunner()
    >>>     runner.invoke(cli.main, "cookies delete --domain example.com".split())
"""
import datetime
import logging

from pathlib import Path

import click


@click.group()
@click.option("--cookies",
              default=None,
              type=click.Path(file_okay=False, resolve_path=True, path_type=Path),
              help="""Path to the cookies folder. By default it is using
                      downloader/client/cookies""")
@click.option("--debug",
              default=False,
              is_flag=True,
              show_default=True,
              help="""Runs the application in the debug mode.
                      Doesn't change the application behavior""")
@click.pass_context
def main(context: click.Context, cookies: Path | None, debug: bool) -> None:
    """Music downloader allows to fetch, update and track music content.

    \b
    Examples:
        | downloader cookies set --domain yandex.ru --key Session_id --value <CookieValue>
        | downloader fetch <url> -c ignore -d %USERPROFILE%/Downloads

    \f
    Note (for documentation in `click` package):
        \b - disables wrapping for docs
        \f - truncate docs.

    Args:
        context: `Click` package context that will be shared within other commands.
        cookies: Expanded path of cookies directory (or None for default).
        debug: Boolean variable that influence on logs. Logs are located in:
            `music-downloader-py/downloader/logs`
    """
    # Click context setup
    context.ensure_object(dict)
    context.obj["cookies"] = cookies

    # Logging setup
    log_filename = datetime.datetime.now().strftime("%Y-%m-%d %H_%M_%S.%f.log")
    log_filepath = Path(__file__).parent.parent / "logs" / log_filename

    logging.basicConfig(
        filename=log_filepath,
        format="%(asctime)s %(levelname)7s: %(filename)s %(funcName)s: %(message)s",
        level=logging.DEBUG if debug else logging.INFO)


@main.command()
@click.argument("domain", default="")
def about(domain: str) -> None:
    """Provides information about specified domain or entire package.

    \b
    Displays information from __init__.py file of supported module,
    or displays the standard message. This allows user to understand
    which domains are supported.
    Also is possible to display information about package/application
    by ignoring domain argument (see example).

    \b
    Examples:
        | downloader about
        | downloader about yandex.ru
        | downloader about youtube.com
        | downloader about example.com

    \b
    Latest (or any other unknown domains) must display:
        `example.com domain is not supported.`

     \f
    Note (for documentation in `click` package):
        \b - disables wrapping for docs
        \f - truncate docs.

    Args:
        domain: The domain string value (e.g. yandex.ru)
    """


@main.command()
@click.option("-l", "--limit",
              default=4,
              help="Limit of the number of tracks that can be downloaded at one time",
              type=click.IntRange(1, 8),
              show_default=True)
@click.option("-c", "--conflict",
              default="ERROR",
              help="""Action in the case when the destination folder contains
                      the same file as downloaded one. Default is ERROR,
                      in that case the application will interrupt and shutdown.
                      IGNORE makes the application to ignore the issues and
                      continue work. OVERRIDE makes the application to override
                      all conflicting files.""",
              type=click.Choice(["ERROR", "IGNORE", "OVERRIDE"], case_sensitive=False),
              show_default=True)
@click.option("-d", "--dest",
              help="""Destination folder. Path supports expanding so it's
                      fine to use `~/` or `%USERPROFILE%`""",
              type=click.Path(file_okay=False, resolve_path=True, path_type=Path),
              required=True)
@click.argument("targets", nargs=-1)
def fetch(targets: tuple[str], limit: int, conflict: str, dest: Path) -> None:
    """Fetches musics from all url targets applying tags and cover.

    \b
    Urls will be processed by host models so result may vary. For now
    the following sources are supported:
        Yandex Music (domain yandex.ru, key Session_id)

    \b
    Examples:
        | downloader fetch <url1> <url2> ... <urlN> -d %USERPROFILE%/Downloads
        | downloader fetch <url> -d %USERPROFILE%/Downloads
        | downloader fetch <url> -d %USERPROFILE%/Downloads -c ignore
        | downloader fetch <url> -d %USERPROFILE%/Downloads -c ignore -l 8

    \f
    Note (for documentation in `click` package):
        \b - disables wrapping for docs
        \f - truncate docs.

    Args:
        targets: The list of url strings. Each one must be determined
            by host and process by host models.
        limit: The download limit. Guarantees to be in [1, 8]
            (by `click` package).
        conflict: Action to preform when file with the same name already
            exists. The one of the following variants `ERROR`, `IGNORE`,
            `OVERRIDE` (`ERROR` is default).
        dest: The destination folder for fetching music. Guarantees to be
            valid by `click` package.
    """
