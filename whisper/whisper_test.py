import whisper
model = whisper.load_model("tiny") # モデルを読み込む
result = model.transcribe("out.wav", fp16=False) # 音声ファイルを指定する
print("finishied")
print(result["text"]) # 認識結果を出力