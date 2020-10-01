# https://www.amphioxus.org/content/timelapse-time-stamp-overlay
import json
import os
from PIL import Image, ImageFont, ImageDraw, ExifTags
from datetime import datetime

font = ImageFont.truetype("PlusJakartaText-Regular.ttf", 72)
fontsmall = ImageFont.truetype("PlusJakartaText-Regular.ttf", 32)
fontcolor = (238,161,6)
counter = 0
# Go through each file in current directory
for i in os.listdir(os.getcwd()):
	if i.endswith(".jpg"):
		counter += 1
		print("Image {0}: {1}".format(counter, i))
        
        # https://stackoverflow.com/a/62077871/4442148
		image_exif = Image.open(i)._getexif()
		# Make a map with tag names
		exif = { ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes }
		# Grab the date
		date_obj = datetime.strptime(exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')

		get_exif_datex = date_obj.strftime('%Y:%m:%d')
		get_exif_timex = date_obj.strftime('%H:%M')

		img = Image.open(i)
 
		# get a drawing context
		draw = ImageDraw.Draw(img)
		draw.text((img.width-220,img.height-150), get_exif_datex, fontcolor, font=fontsmall)
		draw.text((img.width-220,img.height-120), get_exif_timex, fontcolor, font=font)
		filename = "resized/" + i[0:-4] + "-resized.jpg"
		img.save(filename)
