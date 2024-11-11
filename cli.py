# $ git log -n 2 v3.12.6..v3.12.7 -- Lib/argparse.py
# commit cbea45ad74779c0ffe760bab7f9d5ce149302495
# Author: Miss Islington (bot) <31488909+miss-islington@users.noreply.github.com>
# Date:   Sun Sep 29 11:18:06 2024 +0200

#     [3.12] gh-58573: Fix conflicts between abbreviated long options in the parent parser and subparsers in argparse (GH-124631) (GH-124759)
    
#     Check for ambiguous options if the option is consumed, not when it is
#     parsed.
#     (cherry picked from commit 3f27153e077d7e9448e2f081275931968b40cc74)
    
#     Co-authored-by: Serhiy Storchaka <storchaka@gmail.com>

# commit 5464c8aa9856a65f576f536532ee56310397e109
# Author: Miss Islington (bot) <31488909+miss-islington@users.noreply.github.com>
# Date:   Sun Sep 29 10:40:00 2024 +0200

#     [3.12] gh-116850: Fix argparse for namespaces with not directly writable dict (GH-124667) (GH-124758)
    
#     It now always uses setattr() instead of setting the dict item to modify
#     the namespace. This allows to use a class as a namespace.
#     (cherry picked from commit 95e92ef6c74e973ea13d15180190d0fa2af82fbf)
    
#     Co-authored-by: Serhiy Storchaka <storchaka@gmail.com>


# issue from https://github.com/python/cpython/pull/124631

# fail v3.12.7  https://github.com/python/cpython/commit/cbea45ad74779c0ffe760bab7f9d5ce149302495
argparse = __import__("argparse_cbea45a") 
# fail 3.13 (not yet released) https://github.com/python/cpython/commit/6925e5b5c778d0c7deab58c62545b69b4a3d3844
# argparse = __import__("argparse_6925e5b") 


# ok v3.12.7_prev https://github.com/python/cpython/commit/5464c8aa9856a65f576f536532ee56310397e109
# argparse = __import__("argparse_5464c8a") 

# ok v3.13.0 
# argparse = __import__("argparse_v3130") 

# fail main 
# argparse = __import__("argparse_main") 

# python (3.12.7 fail, everything else works)
# import argparse

from collections.abc import Sequence
from typing import Any, Callable, Optional, Union
import sys

Handler = Union[
    Callable[[argparse.ArgumentParser, argparse.Namespace], None],
    Callable[[argparse.ArgumentParser, argparse.Namespace, list[str]], None],
]

def _subcommand(
    subcommand: str,
    *,
    help: Optional[str] = None,  # pylint: disable=redefined-builtin
    description: Optional[str] = None,
    handler: Handler,
    allows_extra: bool = False,
) -> Callable[
    [Callable[[argparse.ArgumentParser], None]],
    Callable[["argparse._SubParsersAction"], None],
]:
    def _wrap_add_subcommand(
        f: Callable[[argparse.ArgumentParser], None]
    ) -> Callable[["argparse._SubParsersAction"], None]:
        def _wrapped_subcommand(subparsers: "argparse._SubParsersAction"):
            parser = subparsers.add_parser(
                subcommand, help=help, description=description
            )
            parser.set_defaults(handler=handler)
            parser.set_defaults(allows_extra=allows_extra)
            f(parser)

        return _wrapped_subcommand

    return _wrap_add_subcommand

def test(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
    extra: list[str],
) -> None:  # pragma: no cover
    print(f":ok args {args} {extra}")


@_subcommand(
    "test",
    help="run tests in a Basilisp project",
    description="Run tests in a Basilisp project.",
    handler=test,
    allows_extra=True,
)
def _add_test_subcommand(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("args", nargs=-1, help="arguments passed on to Pytest")

def invoke_cli(args: Optional[Sequence[str]] = None) -> None:
    """Entrypoint to run the Basilisp CLI."""
    parser = argparse.ArgumentParser(
        description="Basilisp is a Lisp dialect inspired by Clojure targeting Python 3."
    )

    subparsers = parser.add_subparsers(help="sub-commands")
    _add_test_subcommand(subparsers)


    print(f":1 args {sys.argv}")
    parsed_args, extra = parser.parse_known_args(args=args)
    print(f":2 args {parsed_args} {extra}")
    allows_extra = getattr(parsed_args, "allows_extra", False)
    if extra and not allows_extra:
        parser.error(f"unrecognized arguments: {' '.join(extra)}")
    elif hasattr(parsed_args, "handler"):
        if allows_extra:
            parsed_args.handler(parser, parsed_args, extra)
        else:
            parsed_args.handler(parser, parsed_args)
    else:
        parser.print_help()


if __name__ == "__main__":
    invoke_cli()
    
