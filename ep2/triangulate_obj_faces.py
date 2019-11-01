import argparse
from tqdm import tqdm
from shutil import copyfile
import os 

def processFace(infile, outfile, scale):
	fout = open(outfile, "w")
	with open(infile, "r") as fin:
		for line in fin:
			data = line.split()
			if len(data) < 1:
				pass
			elif data[0] == "f":
				if len(data[1:]) == 4: # quad face
					fout.write("f " + data[1] + " " + data[2] + " " + data[3] + "\n")
					fout.write("f " + data[3] + " " + data[4] + " " + data[1] + "\n")
				else:    # triangle face
					fout.write(line)
			elif data[0] == "v":
				fout.write("v " + str(float(data[1])*scale) + " " + 
					                str(float(data[2])*scale) + " " +
					                str(float(data[3])*scale) + "\n")
			else:
				fout.write(line)
	fout.close()

