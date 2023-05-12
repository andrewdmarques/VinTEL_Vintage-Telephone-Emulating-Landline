import sounddevice as sd
import soundfile as sf
import keyboard
from pydub import AudioSegment

def record_audio():
    # Set the audio parameters
    duration = 0.1  # Length of each audio chunk in seconds
    sample_rate = 44100  # Sample rate in Hz
    channels = 2  # Number of audio channels (1 for mono, 2 for stereo)

    # Start recording
    with sf.SoundFile('recording.wav', mode='w', samplerate=sample_rate, channels=channels) as file:
        with sd.InputStream(samplerate=sample_rate, channels=channels, blocksize=int(duration * sample_rate)) as stream:
            print('Recording started (press space bar to stop)...')
            while True:
                # Read audio chunk from the stream
                data, _ = stream.read()

                # Write audio chunk to the file
                file.write(data)

                # Check if space bar is pressed to stop recording
                if keyboard.is_pressed(' '):
                    print('Recording stopped.')
                    break

    # Convert WAV to MP3 using pydub
    sound = AudioSegment.from_wav('recording.wav')
    sound.export('recording.mp3', format='mp3')
record_audio()