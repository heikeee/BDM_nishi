import pyaudio

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"デバイスID: {info['index']}, 名前: {info['name']}")
p.terminate()