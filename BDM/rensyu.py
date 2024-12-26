import csv
import random
import speech_recognition as sr
import os
import sys
import subprocess
import time
from gpiozero import Button

def ButtonPressed(button):
    isButtonPressed = False  # 基本は押されていない設定

    if button.is_pressed:
        isButtonPressed = True
    else:
        isButtonPressed = False 

    return isButtonPressed

LOG_FILE = "debug_log.txt"  # デバッグ用ログファイル名

def log_to_file(message):
    """メッセージをログファイルに書き込む"""
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(message + "\n")

def handle_audio_device_conflict():
    """ターミナル操作で音声デバイスの競合を解消する"""
    try:
        print("# ここでターミナル操作を行う")
        result = subprocess.run(["fuser", "-v", "/dev/snd/*"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)

        for line in result.stdout.splitlines():
            if "/dev/snd/" in line:
                parts = line.split()
                if len(parts) >= 2:
                    pid = parts[1]  # PIDを取得
                    print(f"取得したPID: {pid}")
                    subprocess.run(["kill", "-9", pid])  # プロセスを強制終了
                    log_to_file(pid)
                    print(f"PID {pid} を強制終了しました。")
    except Exception as e:
        print(f"ターミナル操作中にエラーが発生しました: {e}")


def recognize_speech():
    """音声を認識し、テキストとして返す"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("音声入力を開始します。話してください...")
        log_to_file("音声入力を開始します。話してください...")
        try:
            audio = recognizer.listen(source, timeout=5)
            recognized_text = recognizer.recognize_google(audio, language='ja-JP')
            print(f"認識結果: {recognized_text}")
            log_to_file(f"認識結果: {recognized_text}")
            handle_audio_device_conflict
            return recognized_text
        except sr.UnknownValueError:
            message = "音声を認識できませんでした。もう一度お試しください。"
            print(message)
            log_to_file(message)
            handle_audio_device_conflict
            return None
        except sr.RequestError:
            message = "音声認識サービスに接続できません。"
            print(message)
            log_to_file(message)
            return None
        except sr.WaitTimeoutError:
            message = "音声入力がタイムアウトしました。"
            print(message)
            log_to_file(message)
            return None

def load_quizzes(csv_file):
    """CSVファイルからクイズデータを読み込む"""
    quizzes = []
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            quizzes.append({"id": row["id"], "question": row["question"], "answer": row["answer"]})
    return quizzes

def main():
    csv_file = "quizzes.csv"  # クイズデータを格納したCSVファイル名
    quizzes = load_quizzes(csv_file)

    print("\nクイズゲームへようこそ！")
    log_to_file("\nクイズゲームへようこそ！")

    current_question_number = 0
    status = "syutudai"  # 初期状態は問題出題
    button = Button(18, pull_up=True)

    while True:
        if status == "syutudai":
            # 状態1: 問題文を提示する状態
            quiz = random.choice(quizzes)
            current_question_number += 1

            question_message = f"\n第{current_question_number}問\nクイズ: {quiz['question']}"
            print(question_message)
            log_to_file(question_message)

            input_message = "準備ができたらボタンを押してください。"
            print(input_message)
            log_to_file(input_message)
            while True:
                if ButtonPressed(button):
                    break
                time.sleep(0.1)

            # input(input_message)
            
            status = "kaitou"

        elif status == "kaitou":
            # 状態2: 解答待機状態

            answer = recognize_speech()
            if answer is None:
                skip_message = "音声入力が認識されなかったため、スキップします。\n"
                print(skip_message)
                log_to_file(skip_message)
                status = "syutudai"
                continue
            user_answer = answer.strip()
            status = "judge"

        elif status == "judge":
            # 状態3: 正誤判定状態
            if user_answer == quiz['answer']:
                correct_message = "正解！\n"
                print(correct_message)
                log_to_file(correct_message)
            else:
                incorrect_message = f"不正解。正解は: {quiz['answer']}\n"
                print(incorrect_message)
                log_to_file(incorrect_message)
            status = "continue_check"

        elif status == "continue_check":
            # 状態4: 続けるかどうかを判定する状態
            print("続けますか？『続ける』『もう一問』『終了』と答えてください。")
            log_to_file("続けますか？『続ける』『もう一問』『終了』と答えてください。")
            next_action = recognize_speech()

            if next_action is None:
                no_recognition_message = "音声が認識されませんでした。続行操作はありません。\n"
                print(no_recognition_message)
                log_to_file(no_recognition_message)
                continue

            next_action = next_action.strip()
            if next_action in ["続ける", "もう一問","もう1問"]:
                continue_message = "次の問題に進みます。"
                print(continue_message)
                log_to_file(continue_message)
                status = "syutudai"
            elif next_action == "終了":
                end_message = "\nゲーム終了！お疲れ様でした！"
                print(end_message)
                log_to_file(end_message)
                break

if __name__ == "__main__":
    main()
