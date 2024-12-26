import time
from gpiozero import Button

def ButtonPressed(button):
    isButtonPressed = False  # 基本は押されていない設定

    if button.is_pressed:
        isButtonPressed = True
    else:
        isButtonPressed = False 

    return isButtonPressed

def main():
    # GPIO18に接続されたスイッチを設定
    button = Button(18, pull_up=True)
    while True:
        if (ButtonPressed(button)):
            print(ButtonPressed(button))
        else:
            print(ButtonPressed(button))
        time.sleep(0.1)

if __name__ == "__main__":
    main()
