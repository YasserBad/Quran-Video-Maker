# Script Author = Yasser Badache.

# Imports
import moviepy
from moviepy.editor import *
import utils
import os
import math
from muqris import muqris


"""---------------------------------------------------- FUNCTIONS ------------------------------------------------ """

def add_text(content, start, duration, VideoClip, bg_color="black"):
	"""
	This functions adds a Moviepy TextClip Object with the following arguments.
	content = The text's content
	start = The starting moment
	duration = The duration of the text
	VideoClip = The moviepy VideoFileClip object that the text will be added to.
	bg_color = The text's background color. Check utils.py for a list of supported color names.

	"""
	txt_clip = TextClip(txt=content, fontsize=utils.calculate_fontsize(VideoClip, content) ,
		color='white', stroke_color="white", stroke_width=2, bg_color=bg_color
						).set_pos('center').set_start(start).set_duration(duration)

	return txt_clip



def calculate_final_video_length(audio_file_path):
	""" 
	Calculates the output video's length depending on the sum of the lengths of the audio files present 
	in the folder.

	"""
	final_duration = 0
	if os.path.exists(audio_file_path):
		files_list = os.listdir(audio_file_path)
		for file in files_list:
			if ".mp3" in file:
				audio = AudioFileClip(f"downloaded_verses/{file}")
				final_duration += audio.duration
				audio.close() # Not closing the file will result in errors.
	else:
		return "No directory 'downloaded_verses' found."

	return math.ceil(final_duration)


def check_source_video(video_path):
	"""
	Checks if the source video is present and returns a VideoFileClip object for it.

	"""
	if os.path.exists(video_path):
		video_clip = VideoFileClip(video_path, audio=False)
		return video_clip
	else:
		return "Video source not found."




def montage(aya, start_verse, end_verse, source_video_path="videos/source_video/source.mp4", 
	muqri=muqris['Al_Husary']):
	""" All the magic is happening here """

	# First we download all audios.
	utils.download_verses(aya, start_verse, end_verse, muqri)
	# Now here, we set the duration of the final video and check if the source video exists.
	output_vid_duration = calculate_final_video_length("downloaded_verses") # To set as the final video's length.
	source_video = check_source_video(source_video_path).set_duration(output_vid_duration)

	# Here we montage the video.
	# Initilatizing variables.
	audios = []
	current_timestamp = 0
	cooked_audioclip = None
	texts = []
	# Here, we go through each audio file, and add it to the output video, while also adding the text of the verse.
	for file in os.listdir("downloaded_verses"):
		if ".mp3" in file:
			content = None
			with open(f"downloaded_verses/{file}".replace('.mp3', '.txt'), 'r', encoding="utf-8") as f:
				content = f.read()
			audioclip = AudioFileClip(f"downloaded_verses/{file}")
			audioclip.start = current_timestamp
			text_object = add_text(content, current_timestamp, audioclip.duration, source_video)
			texts.append(text_object)
			#print(f'Duration of {file} is {audioclip.duration}')
			print(f'{file} STARTED at : {current_timestamp}')
			current_timestamp += audioclip.duration
			print(f'{file} FINISHED at : {current_timestamp}')
			audios.append(audioclip)

	# We merge all verses audios into one single one.
	merged_audio_clips = concatenate_audioclips(audios)
	# We put it in the video
	source_video.audio = merged_audio_clips
	# We burn the texts into the video clip.
	all_objects = [source_video] + texts
	final_video = CompositeVideoClip(all_objects)
	final_video.write_videofile("videos/output_video/output.mp4")
