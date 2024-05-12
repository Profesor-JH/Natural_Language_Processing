import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
import tempfile
import os
import base64

# Function to perform speech recognition
def recognize_speech(audio_clip):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_clip) as source:
        audio_data = recognizer.record(source)  # Record the audio from the source
        recognized_text = recognizer.recognize_google(audio_data, language='fr-FR')  # Perform speech recognition
        return recognized_text

# Function to create subtitle clips dynamically
def create_subtitle_clips(video_duration, recognized_text):
    # Split the recognized text into smaller chunks
    chunks = [recognized_text[i:i+50] for i in range(0, len(recognized_text), 50)]
    duration_per_chunk = video_duration / len(chunks)
    subtitle_clips = []
    start_time = 0
    for chunk in chunks:
        end_time = start_time + duration_per_chunk
        subtitle_clip = mp.TextClip(chunk, fontsize=36, color='yellow', bg_color='black', font='Arial-Bold').set_start(start_time).set_end(end_time)
        subtitle_clips.append(subtitle_clip)
        start_time = end_time
    return subtitle_clips

# Function to synchronize speech recognition with video playback
def play_video_with_speech_recognition(video_file_content):
    # Save the video file locally
    with open("temp_video.mp4", "wb") as f:
        f.write(video_file_content)

    # Perform speech recognition on the audio
    recognized_text = recognize_speech("temp_audio.wav")

    # Load the video clip
    video_clip = mp.VideoFileClip("temp_video.mp4")

    # Get the duration of the video
    video_duration = video_clip.duration

    # Create subtitle clips dynamically
    subtitle_clips = create_subtitle_clips(video_duration, recognized_text)

    # Composite the video clip with subtitle clips
    video_with_subtitles = mp.CompositeVideoClip([video_clip] + subtitle_clips)

    # Write the video with subtitles to a file
    output_file = "video_with_subtitles.mp4"
    video_with_subtitles.write_videofile(output_file, codec='libx264', fps=video_clip.fps)

    # Display the video with subtitles
    st.video(output_file)

if __name__ == "__main__":
    st.title("Video Player with Speech Recognition")
    video_file = st.file_uploader("Upload Video File", type=["mp4"])

    if video_file is not None:
        # Save the video file content
        video_file_content = video_file.read()

        # Write video file content to temporary file
        with open("temp_video.mp4", "wb") as f:
            f.write(video_file_content)

        # Extract audio from video
        video = mp.VideoFileClip("temp_video.mp4")
        video.audio.write_audiofile("temp_audio.wav", codec='pcm_s16le')

        # Play video with speech recognition
        play_video_with_speech_recognition(video_file_content)
