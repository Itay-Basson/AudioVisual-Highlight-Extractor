# Video Highlight Extractor

This project automates the process of extracting highlights from videos based on volume and specific keywords found in the audio track. It utilizes a series of Python libraries to extract audio, analyze volume, perform speech recognition, create GIFs from peak moments, and finally, add background music to these GIFs. The tool is configurable to work with various input files and parameters, making it versatile for different use cases.

## Features

- **Extract Audio**: Extracts the audio track from a given video file.
- **Volume Analysis**: Identifies peak moments in the audio based on volume levels.
- **Speech Recognition**: Converts speech from the audio track to text, highlighting predefined special words.
- **GIF Creation**: Creates GIFs from identified peak moments in the video.
- **Add Background Music**: Adds a background music track to the generated GIF, converting it back into a video format.

## Getting Started

### Prerequisites

Ensure you have Python 3.6 or later installed on your system. This project also requires FFmpeg to process video and audio files. Install the required Python libraries with:

```bash
pip install moviepy pydub SpeechRecognition vosk argparse numpy
```

Download a Vosk model suitable for your language [here](https://alphacephei.com/vosk/models) and note its path for the configuration.

### Installation

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies as mentioned in the Prerequisites section.

### Configuration

Modify the `config.json` file in the project directory to set up your project paths and parameters:

```json
{
  "video_file": "path/to/your/video.mp4",
  "special_words_file": "path/to/your/special_words.txt",
  "music_file": "path/to/your/background_music.mp3",
  "model_path": "path/to/your/vosk-model",
  "output_audio_file": "output_audio.wav",
  "output_gif_file": "animated_gif.gif",
  "output_video_file": "video_with_music.mp4",
  "window_size": 1500,
  "threshold_multiplier": 1.5,
  "min_duration": 1000
}
```

## Usage

To run the script, use the following command in your terminal:

```bash
python your_script.py --config path/to/config.json
```

Replace `your_script.py` with the name of the main Python script of this project.

## Contributing

Your contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

