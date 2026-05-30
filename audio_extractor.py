from moviepy import VideoFileClip

# Load the video file
cvt_video = VideoFileClip('video.3gpp')

# Extract the audio track
ext_audio = cvt_video.audio

# Write the audio to an MP3 file
ext_audio.write_audiofile('audio_Extracted.mp3')

# Close the clips to release the file resources
ext_audio.close()
cvt_video.close()