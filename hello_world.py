#!/usr/bin/env python3
"""A friendly Hello World program for the vrlab26 hackathon."""

BANNER = r"""
  _   _      _ _         __        __         _     _ _
 | | | | ___| | | ___    \ \      / /__  _ __| | __| | |
 | |_| |/ _ \ | |/ _ \    \ \ /\ / / _ \| '__| |/ _` | |
 |  _  |  __/ | | (_) |    \ V  V / (_) | |  | | (_| |_|
 |_| |_|\___|_|_|\___/      \_/\_/ \___/|_|  |_|\__,_(_)
"""

MESSAGE = """
Welcome to the vrlab26 hackathon!

  * Your journey starts with a single line of code.
  * Great things are built one commit at a time.
  * Have fun and build something amazing.
"""


def main() -> None:
    print(BANNER)
    print(MESSAGE)
    print("Hello, World! 🌍\n")


if __name__ == "__main__":
    main()
