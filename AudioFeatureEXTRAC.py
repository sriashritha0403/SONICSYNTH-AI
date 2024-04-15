# Audio feature Extraction
# Used LibROSA or similar libraries to extract various audio features, such as
import librosa
import numpy as np


def extract_audio_features(audio_file):
    try:
        # Load audio file
        y, sr = librosa.load(audio_file, sr=None)

        # Extract spectral features
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]

        # Extract temporal features
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env)

        # Extract chroma features
        chroma_features = librosa.feature.chroma_stft(y=y, sr=sr)

        # Calculate mean values for each feature
        features = {
            'spectral_centroid': np.mean(spectral_centroid),
            'spectral_bandwidth': np.mean(spectral_bandwidth),
            'spectral_rolloff': np.mean(spectral_rolloff),
            'tempo': tempo,
            'chroma_features': np.mean(chroma_features, axis=1)  # Average along the time axis
        }

        return features

    except Exception as e:
        print(f"Error processing audio file: {e}")
        return None


# Example usage
if _name_ == "_main_":
    try:
        audio_file_path = "path/to/your/audio/file.mp3"

        # Extract audio features
        audio_features = extract_audio_features(audio_file_path)

        if audio_features:
            print("Extracted Audio Features:")
            for feature, value in audio_features.items():
                print(f"{feature}: {value}")
        else:
            print("Failed to extract audio features.")

    except FileNotFoundError:
        print("Audio file not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")