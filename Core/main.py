from pynput.keyboard import Key, Controller

import flask
import time


keyboard = Controller()

app = flask.Flask(__name__)


@app.route('/instructions', methods=['POST'])
def instructions():
    request = flask.request.get_json()
    print(f"{request['direction']} instruction received")
    if request['direction'] == 'left':
        move_left()
    if request['direction'] == 'right':
        move_right()    
    return request['direction']


@app.route('/shoot')
def shoot():
    print("shoot instruction received")
    press_up()
    return 'shoot'


def press_up():
    for _ in range(1500):
        keyboard.press(Key.up)
    keyboard.release(Key.up)

def press_space():
    for _ in range(1500):
        keyboard.press(Key.space)
    keyboard.release(Key.space)


def move_left():
    for _ in range(900):
        keyboard.press(Key.left)
    keyboard.release(Key.left)

def move_right():
    for _ in range(800):
        keyboard.press(Key.right)
    keyboard.release(Key.right)


if __name__ == '__main__':
    app.run(debug=False)