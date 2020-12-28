from campy.gui.events.timer import pause
from breakoutgraphics2 import BreakoutGraphics, Start, Gameover, Win
import keyboard

FRAME_RATE = 1000 / 120  # 120 frames per second.
NUM_LIVES = 5


def main():
    start = Start()
    if keyboard.read_key() == "space":

        graphics = BreakoutGraphics()
        start.window.close()
        lives = NUM_LIVES
        while True:
            if lives <= 0:
                break
            else:
                pause(FRAME_RATE)
                graphics.reflect()
                graphics.move()
                graphics.remove_and_score()
                graphics.countlives()
                if graphics.ball.y >= graphics.window.height:
                    lives -= 1
                    graphics.reset_ball()
                    graphics.switch_off()

                if lives <= 0:
                    # gamover 畫面
                    gameover = Gameover()
                    graphics.window.close()
                    if keyboard.read_key() == "esc":
                        gameover.window.close()
                    break

                finished = graphics.finished()
                if finished:
                    # win 畫面
                    win = Win()
                    graphics.window.close()
                    if keyboard.read_key() == "esc":
                        win.window.close()
                    break


if __name__ == '__main__':
    main()