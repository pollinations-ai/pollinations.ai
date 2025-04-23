import pollinations

import pyaudio
import wave

# pollinations.Text().Transcribe("my_audio.mp3")

def main() -> None:
    p = pyaudio.PyAudio()
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    duration = 5
    frames = []

    print("Speak")

    stream = p.open(
        format=format,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=chunk,
    )

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("temp.wav", "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()

    text_model = pollinations.Text()
    result = text_model.Transcribe("temp.wav")
    print(result)

if __name__ == "__main__":
    main()
