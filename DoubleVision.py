import hashlib
import os
from tkinter import *
import tkinter
from tkinter import filedialog


def filehash(fname):
	hash = hashlib.md5()
	with open(fname, 'rb') as f:
		for chunk in iter(lambda: f.read(4096), b''):
			hash.update(chunk)
	return hash.hexdigest()

def findDuplicates(root): 	# Traversal is depth first
	hashes = {} 	# The dictionary of hashes (keys) for corresponding paths to files (values)
	f_cnt = 0
	f_size = 0
	for root, subdirs, files in os.walk(root):
		for f in files:
			f_path = root + '/' + f
			fhash = filehash(f_path)
			f_cnt += 1
			f_size += os.path.getsize(f_path)
			if fhash in hashes: 	# This file already exists, append it to the list
				plist = hashes[fhash]
				plist.append(root + '/' + f) 	#*** try subdirs here
				hashes[fhash] = plist
			else: 	# This file is unique, add it to the dictionary as a new entry
				hashes[fhash] = [root + '/' + f]
	return hashes, f_cnt, f_size

def searchFiles():
	global dirname
	global resultprint

	startDir = dirname.get()

	if startDir == '':
		startDir = os.path.dirname(os.path.realpath(__file__))
	elif startDir[0:2] != 'C:':
		startDir = os.path.abspath(startDir)

	if os.path.isdir(startDir):
		print('\nThe duplicate file check will begin at: ' + startDir + '\n')
		hashes, f_cnt, f_size = findDuplicates(startDir)
		print("Number of files: " + str(f_cnt))
		print("Total size: " + str(f_size))
		results = ''
		for e in hashes:
			if len(hashes[e]) > 1: 	# found a duplicate file
				print(e + ': ')
				results += e + ':\n'
				for p in hashes[e]:
					print('\t' + p)
					results += '\t' + p + '\n'
				print('')
				results += '\n'
		if results == '':
			results = 'No duplicate files found.'
		resultprint.set(results)
	else:
		print('The specified path is either not a valid path to a directory, or does not exist.')

def askdirectory():
	global window
	global dirname

	dirname.set(tkinter.filedialog.askdirectory(parent=window, mustexist=True))

#Create GUI
window = tkinter.Tk()
window.title("DoubleVision")
window.config(bg="white", width=1000, height=700)
#Welcome********************************************************************************************   

namelabel = tkinter.Label(window, width = 35, text="Welcome to DoubleVision",font="Times 16", foreground="black", background="white", relief='groove', borderwidth=0)
namelabel.grid(row=0, column=0, columnspan=4, rowspan=2, padx=5, pady=5)

#Directions********************************************************************************************   
directions=tkinter.StringVar()
directions.set("This program allows you to search for duplicate files recusively in a directory.\n" +
	"Please enter the name of the directory you wish to begin the search from: ")
directions2 = tkinter.Label(window, width = 70, textvariable=directions, foreground="black", background="white", font='Times 12',
                            relief='groove', borderwidth=0)
directions2.grid(row=10,column=0, columnspan=4, rowspan=2, padx=5, pady=5)
#Selected directory name********************************************************************************************   
dirname=tkinter.StringVar()
dirname.set("<No Directory Set>")
dirname2 = tkinter.Label(window, width = 70, textvariable=dirname, foreground="black", background="white", font='Times 12',
                            relief='groove', borderwidth=0)
dirname2.grid(row=20,column=1)
#Buttons*********************************************************************************************************
selectfolder = tkinter.Button(window, text="Choose\nDirectory", font="Times 12",
                              foreground="black", background="light gray", width=8, height=2, relief="groove", command=askdirectory)
selectfolder.grid(row=20, column=2, pady=10, sticky="E")

executebtn = tkinter.Button(window, text="Execute\nSearch", font="Times 12",
                              foreground="black", background="light gray", width=8, height=2, relief="groove", command=searchFiles)
executebtn.grid(row=20, column=3, pady=10, sticky="E")
#Results********************************************************************************************   
results=tkinter.StringVar()
results.set("Duplicates found:")
results2 = tkinter.Label(window, width = 50, textvariable=results, foreground="black", background="white", font='Times 12',
                            relief='groove', borderwidth=0)
results2.grid(row=30,column=0, columnspan=4, rowspan=2, padx=5, pady=5)
'''
# make a canvas here
scrollbar = Scrollbar(canvas)
scrollbar.pack(side=RIGHT, fill=Y)
'''
canvas = tkinter.Canvas(window, width=70, height=40, background='#ffffff', borderwidth=0)

resultprint=tkinter.StringVar()
resultprint.set("")
resultprint2 = tkinter.Label(window, width = 70, textvariable=resultprint, foreground="black", background="white", font='Times 12',
                            relief='groove', borderwidth=0)
resultprint2.grid(row=35,column=1)

tkinter.mainloop()
