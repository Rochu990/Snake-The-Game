import curses
from curses import textpad

from snake import main


def print_menu(stdscr, selected_row_idx):
    stdscr.clear()
    sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh - 3, sw - 3]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    menu = ["Nowa Gra", "Najlepsze Wyniki"]
    for idx, row in enumerate(menu):
        x = box[0][1] + 2
        y = box[0][0] + 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()


def menu(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row = 0

    print_menu(stdscr, current_row)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                main(stdscr)
                print_menu(stdscr, current_row)
            else:
                stdscr.addstr(10, 10, f"Wybrano opcję {current_row + 1}")
                stdscr.refresh()
                stdscr.getch()
                break

        print_menu(stdscr, current_row)


curses.wrapper(menu)
