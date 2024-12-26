import pygame
import sys
import time

def play_wav_file(file_path):
    # pygameを初期化
    pygame.init()
    pygame.mixer.init()
    
    try:
        # サウンドをロード
        sound = pygame.mixer.Sound(file_path)
        
        # 音声の長さを取得（秒）
        duration = sound.get_length()
        
        # 音声を再生
        sound.play()
        
        # 音声の再生が終わるまで待機
        time.sleep(duration)
        
    except pygame.error as e:
        print(f"エラーが発生しました: {e}")
        
    except KeyboardInterrupt:
        print("\n再生を中断しました")
        
    finally:
        # pygameを終了
        pygame.mixer.quit()
        pygame.quit()

if __name__ == "__main__":

    wav_file = "pinpon1.wav"  # デフォルトのファイル名
    
    play_wav_file(wav_file)