#!/usr/bin/env python3
import sys
import config
# import mazegen


def main() -> None:
    argc = len(sys.argv)
    if argc == 1:
        print("No config file provided. ", end="")
        print("Usage: python3 a-maze-ing.py <config text file>")
    else:
        try:
            setting = config.Config(sys.argv[1])
            print(setting.width, setting.height, setting.entry, setting.exit,
                  setting.perfect, setting.output_file)
            # maze = mazegen.MazeGenerator(
            #     setting.width, setting.height,
            #     setting.entry, setting.exit, setting.perfect)
        except config.InvalidFormat as e:
            print(f"Config invalid format: {e}", file=sys.stderr)
        except ValueError as e:
            print(f"Config invalid values: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
