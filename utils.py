import requests
import os
import concurrent.futures
import shutil
from pyquran.tools import quran
import ctypes
import math


def get_video_size(video_clip):
	"""
	Get the dimensions of the video clip and its surface.
	"""
	video_size = (video_clip.size[0], video_clip.size[1])
	return video_size

def calculate_fontsize(video_clip, text, font="Arial", points=12):
	""" 
	
	Calculates the suitable fontsize depending on the length of the verse.
	I found this in a StackOverflow question, However, It doesnt work 100% perfectly.
	It seems to work fine for relatively short verses, However, It doesn't for very long verses.

	"""
	video_size_x, video_size_y = get_video_size(video_clip)
	text_size_x, text_size_y = GetTextDimensions(text, points, font)

	factor = (video_size_x / text_size_x) * 1.4

	print(math.ceil((points * factor)))
	return math.ceil((points * factor))



def length_normalize(arg):
	""" 
	This is only used to generate the suitable query for the API call. To fetch the aya, You need to use 
	Three digits for the surah, and three digits for the verse.
	So, This function does that for you, So for example, If I pass "5" to this function, It returns "005"
	"""
	if len(str(arg)) < 3:
	    number_of_zeros_to_add = 3 - len(str(arg))
	    query = "".join("0" for i in range(number_of_zeros_to_add))
	    query += str(arg)
	else:
	    query = str(arg)

	return query

def download_verse(muqri, aya, verse):
	""" 
	Function to download the verse

	"""
	aya_str = length_normalize(aya)
	verse_str = length_normalize(verse)
	url = f"https://everyayah.com/data/{muqri}/{aya_str}{verse_str}.mp3"
	response = requests.get(url)
	print(f'Fetching verse: {verse_str}')
	if response.status_code == 200 and len(response.content) > 0:
	    with open(f"downloaded_verses/{verse_str}.mp3", "wb") as f:
	        f.write(response.content)
	    with open(f"downloaded_verses/{verse_str}.txt", "w", encoding="utf-8") as f:
	    	f.write(quran.get_verse(aya,verse,True))
	else:
	    return f"Error fetching verse {verse} or verse doesn't exist."

def download_verses(aya, start_verse, end_verse, muqri="Abdul_Basit_Mujawwad_128kbps"):
	"""

	A function to download many verses using concurrent futures, to increase the speed.

	
	"""
	if start_verse <= end_verse:
	    if os.path.exists("downloaded_verses"):
	        shutil.rmtree("downloaded_verses")

	    os.makedirs("downloaded_verses")
	    with concurrent.futures.ThreadPoolExecutor() as executor:
	        futures = [executor.submit(download_verse, muqri, aya, verse) for verse in range(start_verse, end_verse + 1)]
	        concurrent.futures.wait(futures)
	else:
	    return "Enter a valid interval"

	return "All audios were downloaded"



def GetTextDimensions(text, points, font):

	""" 
	Used also to calculate the suitable fontsize for the verses' text.

	"""
	class SIZE(ctypes.Structure):
	    _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

	hdc = ctypes.windll.user32.GetDC(0)
	hfont = ctypes.windll.gdi32.CreateFontA(points, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, font)
	hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)

	size = SIZE(0, 0)
	ctypes.windll.gdi32.GetTextExtentPoint32A(hdc, text, len(text), ctypes.byref(size))

	ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
	ctypes.windll.gdi32.DeleteObject(hfont)

	return (size.cx, size.cy)




"""

Colors = [b'AliceBlue', b'AntiqueWhite', b'AntiqueWhite1', b'AntiqueWhite2', b'AntiqueWhite3', b'AntiqueWhite4', b'aqua', b'aquamarine', b'aquamarine1', b'aquamarine2', b'aquamarine3', b'aquamarine4', b'azure', b'azure1', b'azure2', b'azure3', b'azure4', b'beige', b'bisque', b'bisque1', b'bisque2', b'bisque3', b'bisque4', b'black', b'BlanchedAlmond', b'blue', b'blue1', b'blue2', b'blue3', b'blue4', b'BlueViolet', b'brown', b'brown1', b'brown2', b'brown3', b'brown4', b'burlywood', b'burlywood1', b'burlywood2', b'burlywood3', b'burlywood4', b'CadetBlue', b'CadetBlue1', b'CadetBlue2', b'CadetBlue3', b'CadetBlue4', b'chartreuse', b'chartreuse1', b'chartreuse2', b'chartreuse3', b'chartreuse4', b'chocolate', b'chocolate1', b'chocolate2', b'chocolate3', b'chocolate4', b'coral', b'coral1', b'coral2', b'coral3', b'coral4', b'CornflowerBlue', b'cornsilk', b'cornsilk1', b'cornsilk2', b'cornsilk3', b'cornsilk4', b'crimson', b'cyan', b'cyan1', b'cyan2', b'cyan3', b'cyan4', b'DarkBlue', b'DarkCyan', b'DarkGoldenrod', b'DarkGoldenrod1', b'DarkGoldenrod2', b'DarkGoldenrod3', b'DarkGoldenrod4', b'DarkGray', b'DarkGreen', b'DarkGrey', b'DarkKhaki', b'DarkMagenta', b'DarkOliveGreen', b'DarkOliveGreen1', b'DarkOliveGreen2', b'DarkOliveGreen3', b'DarkOliveGreen4', b'DarkOrange', b'DarkOrange1', b'DarkOrange2', b'DarkOrange3', b'DarkOrange4', b'DarkOrchid', b'DarkOrchid1', b'DarkOrchid2', b'DarkOrchid3', b'DarkOrchid4', b'DarkRed', b'DarkSalmon', b'DarkSeaGreen', b'DarkSeaGreen1', b'DarkSeaGreen2', b'DarkSeaGreen3', b'DarkSeaGreen4', b'DarkSlateBlue', b'DarkSlateGray', b'DarkSlateGray1', b'DarkSlateGray2', b'DarkSlateGray3', b'DarkSlateGray4', b'DarkSlateGrey', b'DarkTurquoise', b'DarkViolet', b'DeepPink', b'DeepPink1', b'DeepPink2', b'DeepPink3', b'DeepPink4', b'DeepSkyBlue', b'DeepSkyBlue1', b'DeepSkyBlue2', b'DeepSkyBlue3', b'DeepSkyBlue4', b'DimGray', b'DimGrey', b'DodgerBlue', b'DodgerBlue1', b'DodgerBlue2', b'DodgerBlue3', b'DodgerBlue4', b'firebrick', b'firebrick1', b'firebrick2', b'firebrick3', b'firebrick4', b'FloralWhite', b'ForestGreen', b'fractal', b'freeze', b'fuchsia', b'gainsboro', b'GhostWhite', b'gold', b'gold1', b'gold2', b'gold3', b'gold4', b'goldenrod', b'goldenrod1', b'goldenrod2', b'goldenrod3', b'goldenrod4', b'gray', b'gray', b'gray0', b'gray1', b'gray10', b'gray100', b'gray100', b'gray11', b'gray12', b'gray13', b'gray14', b'gray15', b'gray16', b'gray17', b'gray18', b'gray19', b'gray2', b'gray20', b'gray21', b'gray22', b'gray23', b'gray24', b'gray25', b'gray26', b'gray27', b'gray28', b'gray29', b'gray3', b'gray30', b'gray31', b'gray32', b'gray33', b'gray34', b'gray35', b'gray36', b'gray37', b'gray38', b'gray39', b'gray4', b'gray40', b'gray41', b'gray42', b'gray43', b'gray44', b'gray45', b'gray46', b'gray47', b'gray48', b'gray49', b'gray5', b'gray50', b'gray51', b'gray52', b'gray53', b'gray54', b'gray55', b'gray56', b'gray57', b'gray58', b'gray59', b'gray6', b'gray60', b'gray61', b'gray62', b'gray63', b'gray64', b'gray65', b'gray66', b'gray67', b'gray68', b'gray69', b'gray7', b'gray70', b'gray71', b'gray72', b'gray73', b'gray74', b'gray75', b'gray76', b'gray77', b'gray78', b'gray79', b'gray8', b'gray80', b'gray81', b'gray82', b'gray83', b'gray84', b'gray85', b'gray86', b'gray87', b'gray88', b'gray89', b'gray9', b'gray90', b'gray91', b'gray92', b'gray93', b'gray94', b'gray95', b'gray96', b'gray97', b'gray98', b'gray99', b'green', b'green', b'green1', b'green2', b'green3', b'green4', b'GreenYellow', b'grey', b'grey0', b'grey1', b'grey10', b'grey100', b'grey11', b'grey12', b'grey13', b'grey14', b'grey15', b'grey16', b'grey17', b'grey18', b'grey19', b'grey2', b'grey20', b'grey21', b'grey22', b'grey23', b'grey24', b'grey25', b'grey26', b'grey27', b'grey28', b'grey29', b'grey3', b'grey30', b'grey31', b'grey32', b'grey33', b'grey34', b'grey35', b'grey36', b'grey37', b'grey38', b'grey39', b'grey4', b'grey40', b'grey41', b'grey42', b'grey43', b'grey44', b'grey45', b'grey46', b'grey47', b'grey48', b'grey49', b'grey5', b'grey50', b'grey51', b'grey52', b'grey53', b'grey54', b'grey55', b'grey56', b'grey57', b'grey58', b'grey59', b'grey6', b'grey60', b'grey61', b'grey62', b'grey63', b'grey64', b'grey65', b'grey66', b'grey67', b'grey68', b'grey69', b'grey7', b'grey70', b'grey71', b'grey72', b'grey73', b'grey74', b'grey75', b'grey76', b'grey77', b'grey78', b'grey79', b'grey8', b'grey80', b'grey81', b'grey82', b'grey83', b'grey84', b'grey85', b'grey86', b'grey87', b'grey88', b'grey89', b'grey9', b'grey90', b'grey91', b'grey92', b'grey93', b'grey94', b'grey95', b'grey96', b'grey97', b'grey98', b'grey99', b'honeydew', b'honeydew1', b'honeydew2', b'honeydew3', b'honeydew4', b'HotPink', b'HotPink1', b'HotPink2', b'HotPink3', b'HotPink4', b'IndianRed', b'IndianRed1', b'IndianRed2', b'IndianRed3', b'IndianRed4', b'indigo', b'ivory', b'ivory1', b'ivory2', b'ivory3', b'ivory4', b'khaki', b'khaki1', b'khaki2', b'khaki3', b'khaki4', b'lavender', b'LavenderBlush', b'LavenderBlush1', b'LavenderBlush2', b'LavenderBlush3', b'LavenderBlush4', b'LawnGreen', b'LemonChiffon', b'LemonChiffon1', b'LemonChiffon2', b'LemonChiffon3', b'LemonChiffon4', b'LightBlue', b'LightBlue1', b'LightBlue2', b'LightBlue3', b'LightBlue4', b'LightCoral', b'LightCyan', b'LightCyan1', b'LightCyan2', b'LightCyan3', b'LightCyan4', b'LightGoldenrod', b'LightGoldenrod1', b'LightGoldenrod2', b'LightGoldenrod3', b'LightGoldenrod4', b'LightGoldenrodYellow', b'LightGray', b'LightGreen', b'LightGrey', b'LightPink', b'LightPink1', b'LightPink2', b'LightPink3', b'LightPink4', b'LightSalmon', b'LightSalmon1', b'LightSalmon2', b'LightSalmon3', b'LightSalmon4', b'LightSeaGreen', b'LightSkyBlue', b'LightSkyBlue1', b'LightSkyBlue2', b'LightSkyBlue3', b'LightSkyBlue4', b'LightSlateBlue', b'LightSlateGray', b'LightSlateGrey', b'LightSteelBlue', b'LightSteelBlue1', b'LightSteelBlue2', b'LightSteelBlue3', b'LightSteelBlue4', b'LightYellow', b'LightYellow1', b'LightYellow2', b'LightYellow3', b'LightYellow4', b'lime', 
b'LimeGreen', b'linen', b'magenta', b'magenta1', b'magenta2', b'magenta3', b'magenta4', b'maroon', b'maroon', b'maroon1', b'maroon2', b'maroon3', b'maroon4', b'matte', b'MediumAquamarine', b'MediumBlue', b'MediumForestGreen', b'MediumGoldenRod', b'MediumOrchid', b'MediumOrchid1', b'MediumOrchid2', b'MediumOrchid3', b'MediumOrchid4', b'MediumPurple', b'MediumPurple1', b'MediumPurple2', b'MediumPurple3', b'MediumPurple4', b'MediumSeaGreen', b'MediumSlateBlue', b'MediumSpringGreen', b'MediumTurquoise', b'MediumVioletRed', b'MidnightBlue', b'MintCream', b'MistyRose', b'MistyRose1', b'MistyRose2', b'MistyRose3', b'MistyRose4', b'moccasin', b'NavajoWhite', b'NavajoWhite1', b'NavajoWhite2', b'NavajoWhite3', b'NavajoWhite4', b'navy', b'NavyBlue', b'none', b'OldLace', b'olive', b'OliveDrab', b'OliveDrab1', b'OliveDrab2', b'OliveDrab3', b'OliveDrab4', b'opaque', b'orange', b'orange1', b'orange2', b'orange3', b'orange4', b'OrangeRed', b'OrangeRed1', b'OrangeRed2', b'OrangeRed3', b'OrangeRed4', b'orchid', b'orchid1', b'orchid2', b'orchid3', b'orchid4', b'PaleGoldenrod', b'PaleGreen', b'PaleGreen1', b'PaleGreen2', b'PaleGreen3', b'PaleGreen4', b'PaleTurquoise', b'PaleTurquoise1', b'PaleTurquoise2', b'PaleTurquoise3', b'PaleTurquoise4', b'PaleVioletRed', b'PaleVioletRed1', b'PaleVioletRed2', b'PaleVioletRed3', b'PaleVioletRed4', b'PapayaWhip', b'PeachPuff', b'PeachPuff1', b'PeachPuff2', b'PeachPuff3', b'PeachPuff4', b'peru', b'pink', b'pink1', b'pink2', b'pink3', b'pink4', b'plum', b'plum1', b'plum2', b'plum3', b'plum4', b'PowderBlue', b'purple', b'purple', b'purple1', b'purple2', b'purple3', b'purple4', b'red', b'red1', b'red2', b'red3', b'red4', b'RosyBrown', b'RosyBrown1', b'RosyBrown2', b'RosyBrown3', b'RosyBrown4', b'RoyalBlue', b'RoyalBlue1', b'RoyalBlue2', b'RoyalBlue3', b'RoyalBlue4', b'SaddleBrown', b'salmon', b'salmon1', b'salmon2', b'salmon3', b'salmon4', b'SandyBrown', b'SeaGreen', b'SeaGreen1', b'SeaGreen2', b'SeaGreen3', b'SeaGreen4', b'seashell', b'seashell1', b'seashell2', b'seashell3', b'seashell4', b'sienna', b'sienna1', b'sienna2', b'sienna3', b'sienna4', b'silver', b'SkyBlue', b'SkyBlue1', b'SkyBlue2', b'SkyBlue3', b'SkyBlue4', b'SlateBlue', b'SlateBlue1', b'SlateBlue2', b'SlateBlue3', b'SlateBlue4', b'SlateGray', b'SlateGray1', b'SlateGray2', b'SlateGray3', b'SlateGray4', b'SlateGrey', b'snow', b'snow1', b'snow2', b'snow3', b'snow4', b'SpringGreen', b'SpringGreen1', b'SpringGreen2', b'SpringGreen3', b'SpringGreen4', b'SteelBlue', b'SteelBlue1', b'SteelBlue2', b'SteelBlue3', b'SteelBlue4', b'tan', b'tan1', b'tan2', b'tan3', b'tan4', b'teal', b'thistle', b'thistle1', b'thistle2', b'thistle3', b'thistle4', b'tomato', b'tomato1', b'tomato2', b'tomato3', b'tomato4', b'transparent', b'turquoise', b'turquoise1', b'turquoise2', b'turquoise3', b'turquoise4', b'violet', b'VioletRed', b'VioletRed1', b'VioletRed2', 
b'VioletRed3', b'VioletRed4', b'wheat', b'wheat1', b'wheat2', b'wheat3', b'wheat4', b'white', b'WhiteSmoke', b'yellow', b'yellow1', b'yellow2', b'yellow3', b'yellow4', b'YellowGreen']

"""

