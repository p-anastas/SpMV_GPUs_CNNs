import sys
import os
# Import Pillow:
from PIL import Image

#import pkg_resources
#print (pkg_resources.get_distribution("PILLOW").version)

def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

if len (sys.argv) != 2:
	print ('Problem with input' )
else:
	src = str(sys.argv[1])
	if os.path.isfile(src)==False:
		print ( 'Dir ' + src + ' found')
	os.mkdir(src + 'Cropped_pics/')
	for in_file in os.listdir(src):
		if is_non_zero_file(src + in_file)==False:
			if os.path.isfile(src + in_file)==True:
				print ( 'Found empty file: ' +  in_file)
				#print ( 'Executing: ' +  'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file )
				#os.system( 'mv ' + src + in_file + ' ' +  src + 'Removed/' + in_file)
			else:
				print ( 'Found a directory: ' +  in_file)
		else:
			if in_file.endswith(".png"):
				img = Image.open(src+ in_file)
				width = img.size[0]
				height = img.size[1]	
				if width!= 640 or height!=480:
					print ( ' Error width = ' + width + ' height = ' + height)
				img2 = img.crop((142, 57, 514, 429))
				img2.save("Cropped_pics/cr_" + in_file)
				print ( 'Processed image cr_' + in_file ) 

