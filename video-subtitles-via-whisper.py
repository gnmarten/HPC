# Sebastian Raschka 09/24/2022
# Create a new conda environment and packages
#   conda create -n whisper python=3.9
#   conda activate whisper
#   conda install mlxtend -c conda-forge

# Install ffmpeg
# macOS & homebrew
#   brew install ffmpeg
# Ubuntu
#   sudo apt-get install ffmpeg

# Install whisper and whisperx
#   pip install git+https://github.com/openai/whisper.git
#   pip install -U whisperx

import os
import os.path as osp
import subprocess
import whisperx
import whisper
import wave
import contextlib

# Path to the folder with input audio/video files
input_folder = "/kyukon/data/gent/427/vsc42730/sample_data/herzog/transcribes"
audio_outdir = "./extracted_audio"
subtitle_outdir = "./generated_subtitles"

# Function to find files with specific extensions
def find_files(path, extensions, recursive=True):
    matched_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                matched_files.append(osp.join(root, file))
        if not recursive:
            break
    return matched_files



for this_dir in (audio_outdir, subtitle_outdir):
    if not osp.exists(this_dir):
        os.mkdir(this_dir)

# Device configuration
device = "cuda"  # Use "cpu" if GPU is not available
model_name = "large-v2"

# Load the WhisperX model once before processing all files
model = whisperx.load_model(model_name, device)

# Find all audio and video files with .mp3, .wav, and .mp4 extensions
all_files = sorted(find_files(path=input_folder, extensions=[".mp3", ".wav", ".mp4"]))
print("Example path:", all_files[0])
print("Number of files to process:", len(all_files))

for f in all_files:
    print(f"Processing {f}...")

    # Get the base name and file extension
    base_name = osp.splitext(osp.basename(f))[0]
    file_extension = osp.splitext(f)[1].lower()

    # Convert to .wav if the file is not already in .wav format
    if file_extension != '.wav':
        wav_file = osp.join(audio_outdir, f"{base_name}.wav")
        if not osp.exists(wav_file):
            print(f"Converting {f} to {wav_file}...")
            subprocess.run(
                [
                    'ffmpeg', '-i', f, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', wav_file
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT
            )
    else:
        wav_file = f

    # Get the duration of the audio file using the wave module
    try:
        with contextlib.closing(wave.open(wav_file, 'r')) as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
    except Exception as e:
        print(f"Error getting duration of {wav_file}: {e}")
        continue

    # Calculate middle point and start time for trimming
    middle = duration / 2
    start_time = max(middle - 15, 0)  # Ensure start_time is not negative

    # Define the trimmed audio file path
    trimmed_file = osp.join(audio_outdir, f"{base_name}_trimmed.wav")

    # Extract 30 seconds from the middle of the audio
    try:
        # Use ffmpeg command-line tool via subprocess
        subprocess.run(
            [
                'ffmpeg', '-i', wav_file, '-ss', str(start_time), '-t', '30',
                '-ar', '16000', '-ac', '1', '-y', trimmed_file
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
    except Exception as e:
        print(f"Error trimming {wav_file}: {e}")
        continue

    # Transcribe the trimmed audio to detect language
    result_lang = model.transcribe(trimmed_file)
    detected_language_code = result_lang.get('language', 'unknown')
    print(f"Detected language: {detected_language_code}")

    # Remove the trimmed file as it's no longer needed
    os.remove(trimmed_file)

    # Load the alignment model for the detected language
    alignment_model, metadata = whisperx.load_align_model(
        language_code=detected_language_code, device=device
    )

    # Transcribe the full WAV file with the detected language and prevent translation
    result = model.transcribe(wav_file, language=detected_language_code, task='transcribe')

    # Align the transcription to get word-level timestamps
    result_aligned = whisperx.align(
        result["segments"], alignment_model, metadata, wav_file, device
    )

    # Prepare output file path
    output_file = osp.join(subtitle_outdir, f"{base_name}.srt")

    # Save the aligned segments as an SRT file
    def save_as_srt(segments, filename):
        def format_timestamp(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            millis = int(round((seconds - int(seconds)) * 1000))
            return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

        with open(filename, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, start=1):
                start_time = format_timestamp(segment['start'])
                end_time = format_timestamp(segment['end'])
                text = segment['text'].strip()
                f.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

    save_as_srt(result_aligned["segments"], output_file)

print("Processing complete. SRT files generated.")
