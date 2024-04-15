from pydub import AudioSegment
from pydub.playback import play

def modify_audio(input_file, output_file, speed_factor=1.0, pitch_factor=1.0, volume_factor=1.0):
    # Load the input audio file
    audio = AudioSegment.from_file(input_file)

    # Apply speed change (time-stretching)
    audio = audio.speedup(playback_speed=speed_factor)

    # Apply pitch change
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * pitch_factor)
    })

    # Apply volume change
    audio = audio - (60 - 60 * volume_factor)

    # Export the modified audio
    audio.export(output_file, format="wav")

def combine_and_generate(input_file1, input_file2, output_file):
    # Load the input audio files
    audio1 = AudioSegment.from_file(input_file1)
    audio2 = AudioSegment.from_file(input_file2)

    # Ensure the audio files have the same frame rate
    audio1 = audio1.set_frame_rate(min(audio1.frame_rate, audio2.frame_rate))
    audio2 = audio2.set_frame_rate(min(audio1.frame_rate, audio2.frame_rate))

    # Ensure the audio files have the same number of channels
    audio1 = audio1.set_channels(min(audio1.channels, audio2.channels))
    audio2 = audio2.set_channels(min(audio1.channels, audio2.channels))

    # Combine the audio files
    combined_audio = audio1 + audio2  # Concatenate the audio files

    # Export the combined audio in MP3 format
    combined_audio.export(output_file, format="mp3")

# Example usage
piano_file = "/content/goldn-116392.mp3"
flute_file = "/content/the-cradle-of-your-soul-15700.mp3"
output_file = "/content/combined_output.mp3"

# Modify each input file
modify_audio(piano_file, "/content/modified_piano.mp3", speed_factor=1.2, pitch_factor=1.0, volume_factor=0.8)
modify_audio(flute_file, "/content/modified_flute.mp3", speed_factor=1.0, pitch_factor=1.3, volume_factor=1.2)

# Combine the modified audio files
combine_and_generate("/content/modified_piano.mp3", "/content/modified_flute.mp3", output_file)

# Play the original piano and flute audio, as well as the modified and combined audio for comparison
piano_audio = AudioSegment.from_file("/content/modified_piano.mp3")
flute_audio = AudioSegment.from_file("/content/modified_flute.mp3")
combined_audio = AudioSegment.from_file(output_file)

play(piano_audio)
play(flute_audio)
play(combined_audio)
