# https://www.amphioxus.org/content/timelapse-time-stamp-overlay
import json
import os, sys, getopt
from PIL import Image, ImageFont, ImageDraw, ExifTags
from datetime import datetime

def main(argv):
	input_directory = '.'
	output_directory = './'
	truetype_font = 'PlusJakartaSans-Regular.ttf'
	image_ending = '.jpg'
	output_postfix = '-stamped'
	output_prefix = ''
	exif_date_tag = 'DateTimeOriginal'
	opts, args = getopt.getopt(argv,"hi:o:f:",["idirectory=","odirectory=","font=","image_ending=","output_prefix=,output_postfix=,exif_date_tag="])
	for opt, arg in opts:
		if opt == '-h':
			print ('timestamp.py -i <input directory> -o <output directory> -f <truetype font *.ttf> [image_ending=<ending>] [output_prefix=<prefix> [output_postfix=<postix>] [exif_date_tag=<exif_date_tag>]')
			sys.exit()
		elif opt in ("-i", "--idirectory"):
			input_directory = arg
		elif opt in ("-o", "--odirectory"):
			output_directory = arg
		elif opt in ("-f", "--font"):
			truetype_font = arg
		elif opt in ("--image_ending"):
			image_ending = arg
		elif opt in ("--output_prefix"):
			output_prefix = arg
		elif opt in ("--output_postfix"):
			output_postfix = arg
		elif opt in ("--exif_date_tag"):
			exif_date_tag = arg
	print ('Input directory is    ', input_directory)
	print ('Output directory is   ', output_directory)
	print ('truetype font file is ', truetype_font)
	print ('image ending is       ', image_ending)
	print ('output prefix is      ', output_prefix)
	print ('output postfix is     ', output_postfix)
	print ('exif_date_tag  is     ', exif_date_tag)

	font = ImageFont.truetype(truetype_font, 72)
	fontsmall = ImageFont.truetype(truetype_font, 32)
	fontcolor_rgb  = (238,161,6)
	fontcolor_gray = (238)
	counter = 0
	if  (len(output_prefix) == 0) or len(output_postfix):
		print("A output_prefix or output_postfix is needed!")
		sys.exit()

	# Go through each file in current directory
	for file in os.listdir(input_directory):
		if file.endswith(image_ending):
			if  (len(output_prefix) > 0) and (file.startswith(output_prefix)):
				print("Image {0} ignored. File starts with the output prefix!".format(file))
				continue
			if  (len(output_postfix) > 0) and (file.endswith(output_postfix + image_ending)):
				print("Image {0} ignored. File ends with the output postfix!".format(file))
				continue
			counter += 1
			print("Image {0}: {1}".format(counter, file))
			
			# https://stackoverflow.com/a/62077871/4442148
			img = Image.open(input_directory + file)

			image_exif = img._getexif()
			# Make a map with tag names
			exif = { ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes }
			# Grab the date
			date_obj = datetime.strptime(exif[exif_date_tag], '%Y:%m:%d %H:%M:%S')

			get_exif_datex = date_obj.strftime('%Y:%m:%d')
			get_exif_timex = date_obj.strftime('%H:%M')

			print(img.format, img.size, img.mode)

			if(img.mode == "L"):
				fontcolor = fontcolor_gray
			else:
				fontcolor = fontcolor_rgb

			# get a drawing context
			draw = ImageDraw.Draw(img)
			draw.text((img.width-220,img.height-150), get_exif_datex, fontcolor, font=fontsmall)
			draw.text((img.width-220,img.height-120), get_exif_timex, fontcolor, font=font)
			filename = output_directory + output_prefix + file[0:-len(image_ending)] + output_postfix + image_ending
			img.save(filename)
		

if __name__ == "__main__":
   main(sys.argv[1:])