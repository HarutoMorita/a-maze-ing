#!/usr/bin/env python3
import sys
import os
import config
from mazegen import MazeGenerator
from mlx import Mlx


def display_maze(maze_gen):
    pixel = 30
    menu_height = 35
    m = Mlx()
    mlx_ptr = m.mlx_init()
    initial_maze = maze_gen.generate()
    state = {
        "maze": initial_maze,
        "show_path": False,
        "color_mode": 0,
        "needs_update": True,
        "win_ptr": None,
        "img_ptr": None
    }
    colors = [
        {
            "bg": 0xFF222222,
            "wall": 0xFFFFFFFF,
            "entry": 0xFF00FF00,
            "exit": 0xFFFF0000,
            "pattern": 0xFFFFFF00
        },
        {
            "bg": 0xFF000033,
            "wall": 0xFF00FFFF,
            "entry": 0xFFFFFF00,
            "exit": 0xFF00FF00,
            "pattern": 0xFFFF0000
        },
        {
            "bg": 0xFF000000,
            "wall": 0xFF00FF00,
            "entry": 0xFFFF0000,
            "exit": 0xFFFFFF00,
            "pattern": 0xFF00FF00
        }
    ]

    def create_window():
        win_width = state["maze"].width * pixel
        win_height = state["maze"].height * + menu_height

        state["win_ptr"] = m.mlx_new_window(
            mlx_ptr, win_width, win_height, "A-maze-ing")
        state["img_ptr"] = m.mlx_new_image(
            mlx_ptr, win_width, win_height)

    create_window()

    def update_buffer():
        p = colors[state["color_mode"]]
        img = state["img_ptr"]
        data, bpp, size_line, _ = m.mlx_get_data_addr(img)
        bpp_step = bpp // 8
        maze = state["maze"]
        for i in range(len(data)):
            data[i] = 0

        def put_p(x, y, color):
            offset = ((y + menu_height) * size_line) + (x * bpp_step)
            if offset + 3 < len(data):
                data[offset:offset+4] = color.to_bytes(4, 'little')

        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell((x, y))
                x_s = x * pixel
                y_s = y * pixel

                color = p["bg"]
                if cell.is_entry:
                    color = p["entry"]
                elif cell.is_exit:
                    color = p["exit"]
                elif getattr(cell, 'is_pattern', False):
                    color = p["pattern"]

                if state["show_path"] and getattr(cell, 'is_path', False):
                    color = 0xFF5555FF

                for dy in range(pixel):
                    for dx in range(pixel):
                        put_p(x_s + dx, y_s + dy, color)

                wall_c = p["wall"]
                v = cell.value
                if v & 1:
                    for i in range(pixel):
                        put_p(x_s + i, y_s, wall_c)
                if v & 2:
                    for i in range(pixel):
                        put_p(x_s + pixel - 1, y_s + i, wall_c)
                if v & 4:
                    for i in range(pixel):
                        put_p(x_s + i, y_s + pixel - 1, wall_c)
                if v & 8:
                    for i in range(pixel):
                        put_p(x_s, y_s + i, wall_c)

        state["needs_update"] = False

    def handle_key(keycode, param):
        if keycode == 65307 or keycode == 53:
            os._exit(0)
        elif keycode == 114:
            state["maze"] = maze_gen.generate()
            state["needs_update"] = True
        elif keycode == 112:
            state["show_path"] = not state["show_path"]
            state["needs_update"] = True
        elif keycode == 99:
            state["color_mode"] = (state["color_mode"] + 1) % len(colors)
            state["needs_update"] = True
        return 0

    def render(param=None):
        if state["needs_update"]:
            update_buffer()

        m.mlx_put_image_to_window(
            mlx_ptr, state["win_ptr"], state["img_ptr"], 0, 0)

        m.mlx_string_put(mlx_ptr, state["win_ptr"], 10, 970, 0xFFFFFFFF,
                         "R: Regen | P: Path | C: Color | ESC: Quit")
        return 0

    m.mlx_key_hook(state["win_ptr"], handle_key, None)
    m.mlx_loop_hook(mlx_ptr, render, None)
    m.mlx_loop(mlx_ptr)


def main() -> None:
    argc = len(sys.argv)
    if argc == 1:
        print("No config file provided. ", end="")
        print("Usage: python3 a-maze-ing.py <config text file>")
    else:
        try:
            setting = config.Config(sys.argv[1])
            mazegen = MazeGenerator(
                setting.width, setting.height,
                setting.entry, setting.exit, setting.perfect,
                setting.seed, setting.algo)
            display_maze(mazegen)
        except config.InvalidFormat as e:
            print(f"Config invalid format: {e}", file=sys.stderr)
        except ValueError as e:
            print(f"Config invalid values: {e}", file=sys.stderr)
        except FileNotFoundError as e:
            print(f"{e}", file=sys.stderr)


if __name__ == "__main__":
    main()
