# About Quran-Video-Maker
This tool is a Python script that allows users to create videos by adding recitations of specific Quranic verses to a source video. The tool merges the audio of various renowned Quran reciters, sourced from everyayah.com, with a specified source video, while also overlaying the text of each recited verse onto the video.
# Key Features

- Verse Download: The tool fetches Quranic verses from everyayah.com, downloading the recitations of selected verses in MP3 format.

- Reciter Options: Users can choose from a variety of well-known Quran reciters available in the muqris.py file.
  
- Source Video Integration: The script supports the integration of the recited verses' audio into a designated source video, adding a layer to the video's audio.
  
- Text Overlay: As the audio of each recited verse plays, the tool automatically overlays the corresponding text onto the video, allowing viewers to read and contemplate the verses' meanings.

# Usage

- Using the function montage(), That is found in the quran_video_maker.py

  `from quran_video_maker import *`

- Then we simply call our function.

  `montage(surah, start_verse, end_verse, source_video_path="videos/source_video/source.mp4", 
	muqri=muqris['Al_Husary'])`
  
