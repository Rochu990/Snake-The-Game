import curses
import random
from curses import textpad


def create_food(snake, box):
    food = None
    while food is None:
        food = [
            random.randint(box[0][0] + 1, box[1][0] - 1),
            random.randint(box[0][1] + 1, box[1][1] - 1),
        ]
        if food in snake:
            food = None
    return food


def print_score(stdscr, score, player_name):
    sh, sw = stdscr.getmaxyx()
    score_text = "Score: {}".format(score)
    name_text = "Player: {}".format(player_name)
    full_text = "{}  |  {}".format(name_text, score_text)
    stdscr.addstr(0, sw // 2 - len(full_text) // 2, full_text)


def main(stdscr, player_name):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh - 3, sw - 3]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    snake = [[sh // 2, sw // 2 + 1], [sh // 2, sw // 2], [sh // 2, sw // 2 - 1]]
    direction = curses.KEY_RIGHT

    for y, x in snake:
        stdscr.addstr(y, x, "#")

    food = create_food(snake, box)
    stdscr.addstr(food[0], food[1], "*")

    score = 0
    print_score(stdscr, score, player_name)

    while 1:
        key = stdscr.getch()
        direction = select_direction(direction, key)
        head = snake[0]

        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1] + 1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1] - 1]
        elif direction == curses.KEY_UP:
            new_head = [head[0] - 1, head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0] + 1, head[1]]

        snake.insert(0, new_head)
        stdscr.addstr(new_head[0], new_head[1], "#")

        if snake[0] == food:
            food = create_food(snake, box)
            stdscr.addstr(food[0], food[1], "*")
            score += 1
            print_score(stdscr, score, player_name)
        else:
            stdscr.addstr(snake[-1][0], snake[-1][1], " ")
            snake.pop()

        if should_finish(box, snake):
            msg = "Game Over"
            stdscr.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            stdscr.nodelay(0)
            stdscr.getch()
            break

        stdscr.refresh()


def should_finish(box, snake):
    return (
        snake[0][0] in [box[0][0], box[1][0]]
        or snake[0][1] in [box[0][1], box[1][1]]
        or snake[0] in snake[1:]
    )


def select_direction(direction, key):
    if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
        oppo = {
            curses.KEY_RIGHT: curses.KEY_LEFT,
            curses.KEY_LEFT: curses.KEY_RIGHT,
            curses.KEY_UP: curses.KEY_DOWN,
            curses.KEY_DOWN: curses.KEY_UP,
        }
        if direction != oppo[key]:
            direction = key
    return direction


if __name__ == "__main__":
    curses.wrapper(main)
