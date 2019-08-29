import numpy as np
import soundfile as sf

import os
import argparse

FLAGS = None
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--filename', type=str, help='For single mode, enter filename', default=None) 
parser.add_argument('--rootdir', type=str, help='Roots folder where class folders containing audio files are kept', default=None) 
parser.add_argument('--outdir', type=str, help='Output directory', default='./output')
parser.add_argument('--recursive', type=bool, help='If recursive will looks for files in all the subdirs in rootdir', default=False)
parser.add_argument('--start', type=float, help='Start time to trim (in sec or sample no.)', default=0.)
parser.add_argument('--end', type=float, help='End time to trim (in sec or sample no.)', required=True)
parser.add_argument('--units', type=str, help='Define start and end times in units as seconds or sample no.', choices=['sec', 'sample'], default='sec')
parser.add_argument('--sr', type=int, help='Samplerate of files', default=16000) 

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

def listDirectory_all(directory,topdown=True):
	"""returns a list of all files in directory and all its subdirectories"""
	fileList = []
	fnameList = []
	for root, _, files in os.walk(directory, topdown=topdown):
		for name in files:
			fileList.append(os.path.join(root, name))
			fnameList.append(name)
	return fileList , fnameList

def trim(data,sr,end,start=0,unit_seconds=True):
	if unit_seconds:
		end = int(end*sr)  #else end is assumed to be a sample number
	if end > len(data):
		return data[int(start*sr):]
	return data[int(start*sr):end]

def load_trim_save(file,outdir,sr,end,start=0,unit_seconds=True):
	if unit_seconds:
		end = int(end*sr)  #else end is assumed to be a sample number
		start = int(start*sr)
	y,samplerate = sf.read(file,start=start,stop=end)
	if samplerate != sr:
		raise ValueError("The samplerate given is not correct!")	
	try:
		os.stat(outdir) # test for existence
	except:
		os.mkdir(outdir) # create if necessary   
	basename = os.path.basename(file)
	return sf.write(outdir + '/' + basename, y, samplerate)


if __name__ == '__main__':
	if FLAGS.units is 'sec':
		unit_seconds = True
	elif FLAGS.units is 'sample':
		unit_seconds = False
	if (FLAGS.filename is not None) and (FLAGS.rootdir is None):
		print("Converting the following:")
		print(FLAGS.filename)
		load_trim_save(FLAGS.filename,FLAGS.outdir,FLAGS.sr,FLAGS.end,FLAGS.start,unit_seconds)
	elif (FLAGS.rootdir is not None) and (FLAGS.filename is None):
		folder, _ = listDirectory(FLAGS.rootdir,'.wav')
		if FLAGS.recursive:
			folder, _ = listDirectory_all(FLAGS.rootdir)
		print("Converting the following:")
		print(folder)
		for file in folder:
			load_trim_save(file,FLAGS.outdir,FLAGS.sr,FLAGS.end,FLAGS.start,unit_seconds)
	elif (FLAGS.rootdir is None) and (FLAGS.filename is None):
		raise ValueError("Please enter a filename or directory!")  