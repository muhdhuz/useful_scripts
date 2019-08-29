import numpy as np
import librosa # for audio file loading and saving
import soundfile as sf

import os
import argparse

FLAGS = None
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--filename', type=str, help='For single mode, enter filename', default=None) 
parser.add_argument('--rootdir', type=str, help='Roots folder where class folders containing audio files are kept', default='./') 
parser.add_argument('--outdir', type=str, help='Output directory', default='./output')
parser.add_argument('--sr', type=int, help='Target samplerate', default=None) 

FLAGS, unparsed = parser.parse_known_args()
print('\n FLAGS parsed :  {0}'.format(FLAGS))
#======================================================================

def listDirectory(directory, fileExtList, regex=None):										 
	"""returns a list of file info objects in directory that contains extension in the list fileExtList (include the . in your extension string)
	and regex if specified
	fileList - fullpath from working directory to files in directory
	fnameList - basenames in directory (including extension)
	regex - a substring in the filename, if unspecified will list all files in directory"""	
	if regex is not None:
		fnameList = [os.path.normcase(f)
				for f in os.listdir(directory)
					if (not(f.startswith('.')) and (regex in f))] 
	else:
		fnameList = [os.path.normcase(f)
				for f in os.listdir(directory)
					if (not(f.startswith('.')))] 
	
	fileList = [os.path.join(directory, f) 
			   for f in fnameList
				if os.path.splitext(f)[1] in fileExtList]  
	return fileList , fnameList

def resample(file,target_sr,outdir):
	y, sr = librosa.load(file)
	if target_sr == None:
		target_sr = sr
	y_resampled = librosa.resample(y, sr, target_sr)
	try:
		os.stat(outdir) # test for existence
	except:
		os.mkdir(outdir) # create if necessary    
	#return librosa.output.write_wav(outdir + '/' + file, y_resampled, target_sr)
	return sf.write(outdir + '/' + file, y_resampled, target_sr, subtype='PCM_16')


if __name__ == '__main__':
	if FLAGS.filename != None and FLAGS.rootdir == None:
		resample(FLAGS.filename,FLAGS.sr,FLAGS.outdir)
	elif FLAGS.rootdir != None and FLAGS.filename == None:
		folder, _ = listDirectory(FLAGS.rootdir,'.wav')
		print("Converting the following:")
		print(folder)
		for file in folder:
			resample(file,FLAGS.sr,FLAGS.outdir)
	elif FLAGS.rootdir == None and FLAGS.filename == None:
		folder, _ = listDirectory(FLAGS.rootdir,'.wav')
		print("Converting the following:")
		print(folder)
		for file in folder:
			resample(file,FLAGS.sr,FLAGS.outdir)  