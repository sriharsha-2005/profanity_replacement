# Video Profanity Replacer

**Created by: Sriharsha Chittipothu**  
**GitHub: [@sriharsha-2005](https://github.com/sriharsha-2005)**  
**Email: sriharshachittipothu@gmail.com**

An AI-powered web application that automatically detects and replaces profanity in videos with clean alternatives while maintaining natural speech flow.

## 🚀 Features

- **Drag & Drop Interface**: Easy-to-use web interface for video upload
- **AI Speech Recognition**: Uses Whisper AI for accurate speech-to-text conversion
- **Smart Profanity Detection**: Custom filter that detects profane words and phrases
- **Natural Voice Replacement**: Microsoft Edge TTS for generating replacement audio
- **Seamless Audio Integration**: Replaces profane segments while preserving video quality
- **Multiple Voice Options**: Choose between male and female voices for replacements
- **Multiple Format Support**: Supports MP4, AVI, MOV, MKV, WMV, FLV, and WebM formats

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Speech Recognition**: Faster Whisper
- **Text-to-Speech**: Microsoft Edge TTS
- **Audio Processing**: FFmpeg
- **Frontend**: HTML5, CSS3, JavaScript
- **Video Processing**: FFmpeg

## 📋 Prerequisites

Before running this application, make sure you have:

1. **Python 3.8+** installed
2. **FFmpeg** installed and accessible in your system PATH
3. **Git** (for cloning the repository)

### Installing FFmpeg

**Windows:**

```bash
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**macOS:**

```bash
# Using Homebrew
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install ffmpeg
```

## 🚀 Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd profanity_replacement
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv

   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**

   ```bash
   python run.py
   ```

5. **Access the application:**
   Open your web browser and navigate to `http://localhost:5000`

## 📖 Usage

1. **Upload Video**: Drag and drop your video file or click to browse
2. **Select Voice**: Choose between male or female voice for replacements
3. **Process**: Click "Process Video" to start the AI-powered profanity replacement
4. **Download**: Once processing is complete, download your clean video

## 🔧 How It Works

The application follows this processing pipeline:

1. **Video Upload**: User uploads a video through the web interface
2. **Audio Extraction**: FFmpeg extracts audio from the video
3. **Speech Recognition**: Whisper AI transcribes the audio to text
4. **Profanity Detection**: Custom filter identifies profane content
5. **Audio Generation**: Edge TTS creates replacement audio for profane segments
6. **Audio Replacement**: Original profane audio is replaced with clean alternatives
7. **Video Reconstruction**: Final video is created with censored audio
8. **Download**: Clean video is made available for download

## 📁 Project Structure

```
profanity_replacement/
├── app/                    # Flask application
│   ├── __init__.py        # Flask app initialization
│   ├── routes.py          # Web routes and API endpoints
│   ├── templates/         # HTML templates
│   │   └── index.html     # Main upload interface
│   └── static/            # Static files (CSS, JS, images)
├── python/                # Core processing engine
│   ├── main.py           # Main processing pipeline
│   ├── audio_processing/ # Audio handling modules
│   ├── text_processing/  # Text analysis modules
│   ├── utils/            # Utility functions
│   └── output/           # Processed video outputs
├── run.py                # Application entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## ⚙️ Configuration

### Profanity Filter

You can customize the profanity detection by editing `python/text_processing/profanity_filter.py`:

```python
PROFANITY_MAP = {
    r'\basshole\b': "jerk",
    r'\bshit\b': "crap",
    # Add your own patterns here
}
```

### Voice Options

The application supports different voice options for replacements. You can modify voice settings in the web interface or directly in the code.

## 🐛 Troubleshooting

### Common Issues

1. **FFmpeg not found**: Make sure FFmpeg is installed and in your system PATH
2. **Import errors**: Ensure all dependencies are installed: `pip install -r requirements.txt`
3. **Processing fails**: Check that your video file is supported and not corrupted
4. **Memory issues**: Large video files may require more RAM

### Logs

The application logs processing information to help with debugging. Check the console output for detailed information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 🚀 Deployment

### Deploy to Render

1. **Fork/Clone this repository** to your GitHub account
2. **Sign up for Render** at https://render.com
3. **Create a new Web Service**:
   - Connect your GitHub repository
   - Choose "Python" as the environment
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn run:app --bind 0.0.0.0:$PORT`
4. **Deploy** and wait for the build to complete

### Deploy to Heroku

1. **Install Heroku CLI** and login
2. **Create a new Heroku app**:
   ```bash
   heroku create your-app-name
   ```
3. **Deploy**:
   ```bash
   git push heroku main
   ```

### Environment Variables

For production deployment, you may need to set these environment variables:

- `FLASK_ENV`: Set to `production` for production mode
- `PORT`: The port number (usually set automatically by the platform)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Faster Whisper](https://github.com/guillaumekln/faster-whisper) for speech recognition
- [Microsoft Edge TTS](https://github.com/rany2/edge-tts) for text-to-speech
- [FFmpeg](https://ffmpeg.org/) for audio/video processing
- [Flask](https://flask.palletsprojects.com/) for the web framework

## 📞 Support

If you encounter any issues or have questions, please:

1. Check the troubleshooting section above
2. Search existing issues in the repository
3. Create a new issue with detailed information about your problem

---

**Note**: This application processes videos locally and does not upload your content to external servers. All processing happens on your machine for privacy and security.
