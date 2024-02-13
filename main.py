from moviepy.editor import *
import numpy as np
from pydub import AudioSegment
import speech_recognition as sr
import json
from vosk import Model, KaldiRecognizer
import argparse
import os

# Load configuration
def load_config(config_path):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def extract_audio_from_video(video_file, output_audio_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(output_audio_file)

def calculate_average_volume(audio, start, end):
    segment = audio[start:end]
    return segment.dBFS

def ms_to_min_sec(milliseconds):
    minutes, remainder = divmod(milliseconds, 60000)
    seconds = remainder // 1000
    return f"{minutes} {seconds}"

def find_peak_moments(audio_file, window_size, threshold_multiplier, min_duration):
    audio = AudioSegment.from_file(audio_file)
    overall_avg_volume = audio.dBFS
    threshold = overall_avg_volume + threshold_multiplier

    peak_moments = []
    start_time = None

    for i in range(0, len(audio) - window_size, window_size):
        window_avg_volume = calculate_average_volume(audio, i, i + window_size)
        if window_avg_volume > threshold and start_time is None:
            start_time = i
        elif window_avg_volume <= threshold and start_time is not None:
            end_time = i
            if end_time - start_time >= min_duration:
                peak_moments.append((start_time, end_time))
            start_time = None

    return peak_moments

def convert_audio_to_text(audio_file, model_path, special_words_file):
    model = Model(model_path)
    with sr.AudioFile(audio_file) as source:
        recognizer = sr.Recognizer()
        audio_data = recognizer.record(source)
        raw_data = audio_data.get_raw_data(convert_rate=16000, convert_width=2)

    rec = KaldiRecognizer(model, 16000)
    rec.AcceptWaveform(raw_data)
    rec.SetWords(True)
    result = json.loads(rec.Result())

    print("Peak moments-based on special words:")
    special_words = set()
    with open(special_words_file, 'r') as f:
        for line in f:
            special_words.add(line.strip().lower())

    if 'result' in result:
        for word in result['result']:
            if word['word'].lower() in special_words:
                print(f"Found special word '{word['word']}' at [{word['start']:.2f}-{word['end']:.2f}]")
    else:
        print("No special words were recognized in the audio")

def create_gif_from_peak_moments(video_file, peak_moments, output_gif_file):
    video = VideoFileClip(video_file)
    peak_clips = [video.subclip(start/1000, end/1000).resize(height=360) for start, end in peak_moments]
    final_clip = concatenate_videoclips(peak_clips)
    final_clip.write_gif(output_gif_file, fps=10)

def add_background_music(gif_file, music_file, output_video_file):
    gif_clip = VideoFileClip(gif_file)
    music = AudioFileClip(music_file).set_duration(gif_clip.duration)
    video_with_music = gif_clip.set_audio(music)
    video_with_music.write_videofile(output_video_file, codec='libx264')

def main(config_path):
    config = load_config(config_path)

    extract_audio_from_video(config['video_file'], config['output_audio_file'])
    peak_moments = find_peak_moments(config['output_audio_file'], config['window_size'], config['threshold_multiplier'], config['min_duration'])

    print("Peak moments-based on volume:")
    for start_time, end_time in peak_moments:
        start_min_sec = ms_to_min_sec(start_time)
        end_min_sec = ms_to_min_sec(end_time)
        print(f"{start_min_sec} - {end_min_sec}")

    convert_audio_to_text(config['output_audio_file'], config['model_path'], config['special_words_file'])
    create_gif_from_peak_moments(config['video_file'], peak_moments, config['output_gif_file'])
    add_background_music(config['output_gif_file'], config['music_file'], config['output_video_file'])

    print("Execution completed successfully. All tasks have been performed. Please check the project folder for the newly generated video and animated GIF.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video and audio for highlights.")
    parser.add_argument("--config", help="Path to the configuration file", default="config.json")
    args = parser.parse_args()
    main(args.config)
