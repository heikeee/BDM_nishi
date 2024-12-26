import pyaudio
import speech_recognition as sr

def main(device_index):
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=device_index)

    try:
        # デバイスのサポートしているパラメータを確認
        print(f"デバイスID {device_index} を使用します。")
        with mic as source:
            print("環境ノイズを調整中...")
            recognizer.adjust_for_ambient_noise(source)
            print("リアルタイム音声認識を開始します。終了するには Ctrl+C を押してください。")

            while True:
                print("話してください...")
                audio = recognizer.listen(source)
                try:
                    text = recognizer.recognize_google(audio, language="ja-JP")
                    print(f"認識結果: {text}")
                except sr.UnknownValueError:
                    print("音声を認識できませんでした。")
                except sr.RequestError as e:
                    print(f"Google Web Speech API にアクセスできません: {e}")

    except AssertionError as e:
        print(f"エラー: {e}. デバイスIDが正しいことを確認してください。")
    except AttributeError as e:
        print(f"エラー: {e}. オーディオデバイスが正しく設定されていることを確認してください。")
    except KeyboardInterrupt:
        print("音声認識を終了します。")

if __name__ == "__main__":
    # 使用したいデバイスIDを確認して指定
    main(device_index=1)
