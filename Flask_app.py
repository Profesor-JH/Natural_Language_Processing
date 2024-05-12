from flask import Flask, render_template, request, send_file
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import speech_recognition as sr

app = Flask(__name__)

# Function to perform speech recognition
def recognize_speech(audio_clip):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_clip) as source:
        audio_data = recognizer.record(source)  # Record the audio from the source
        recognized_text = recognizer.recognize_google(audio_data, language='fr-FR')  # Perform speech recognition
        return recognized_text

# Function to add subtitles to the video
# Function to add subtitles to the video
def add_subtitles(video_file, subtitles):
    video_clip = VideoFileClip(video_file)
    subtitle_clips = []

    for subtitle_text, start_time, end_time in subtitles:
        # Create TextClip for subtitle
        subtitle_clip = TextClip(subtitle_text, fontsize=24, color='white', bg_color='yellow')
        subtitle_clip = subtitle_clip.set_duration(end_time - start_time).set_start(start_time)
        subtitle_clips.append(subtitle_clip)

    # Composite subtitle clips onto the video clip
    video_with_subtitles = CompositeVideoClip([video_clip] + subtitle_clips)

    # Write video with subtitles to a file
    output_file = "output_video_with_subtitles.mp4"
    video_with_subtitles.write_videofile(output_file, codec='libx264')

    return output_file


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    video_file = request.files['file']
    audio_file = "temp_audio.wav"
    video_file.save(video_file.filename)
    video_clip = VideoFileClip(video_file.filename)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_file)

    recognized_text = recognize_speech(audio_file)
    # Split recognized text into subtitles
    # Example: [(subtitle_text, start_time, end_time), ...]
    subtitles = [(recognized_text, 0, video_clip.duration)]

    output_file = add_subtitles(video_file.filename, subtitles)
    return render_template('index.html', video_file=output_file)

@app.route('/download')
def download():
    filename = request.args.get('filename')
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
