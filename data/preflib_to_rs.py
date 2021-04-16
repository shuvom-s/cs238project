'''
	File: 	preflib_to_rs.py
	Author:	Sahana Srinivasan and Shuvom Sadhuka
	Date:	April 10, 2021
About
--------------------
	This file contains a set of useful modules for converting PrefLib files 
	to ballots accepted by the Rivest and Shen's voting systems code.

'''

import operator
import itertools
import math
import copy
import glob


def convert(filename, ext):
	"""
	Converts the preflib toc file to a file in the format that Rivest and Shen's
	GT code will accept. 

    Examples of line conversion within the file:
	   "3358,1,{2,3,4,5,6,7,8,9,10}"       returns "(3358) 1 2 = 3 = 4 = 5 = 6 = 7 = 8 = 9 = 10"
	   "17,2,3,1,4,5,6,10,8,9,7"		   returns "(17) 2 3 1 4 5 6 10 8 9 7"
	   "1,2,3,4,1,6,10,{8,9,5},7"		   returns "(1) 2 3 4 1 6 10 8 = 0 = 5 7"
    """

	input = open(filename + "." + ext, "r")
	text = input.read()
	lines = text.split("\n")

	out = open(filename + "-converted." + ext, "x")

	# Skip over list of canidates, other metadata
	num_alts = lines[0]
	lines = lines[int(num_alts)+2:len(lines)-1]


	for line in lines:
		#print(line)
		seen = []
		newline = ""
		# first element is count then stricly ranked candidates, every element after is a candidate 
		# or several equally-ranked candidates
		ranks = line.split('{')
		for rank in ranks:
			if newline == "":
				cands = rank.split(",")
				newline += "(" + str(cands[0]) + ") "
				for cand in cands[1:len(cands)]:
					if cand not in seen and cand != "":
						seen.append(cand)
						newline += cand + " "
			elif '}' in rank:
				bipart = rank.split('}')
				equal_cands = bipart[0].split(",")
				for cand in equal_cands:
					if cand not in seen:
						seen.append(cand)
						if (newline[-1] != " "):
							newline += " "
						newline += cand + " = "
				if newline[len(newline) - 3:] == " = ":
					newline = newline[:len(newline) - 3]
				cands = bipart[1].split(",")
				for cand in cands:
					if cand not in seen and cand != "":
						seen.append(cand)
						if (newline[-1] != " "):
							newline += " "
						newline += cand + " "

		out.write(newline)
		out.write("\n")

	out.close()



def convert_files(path, ext):
	"""
	Converts all the preflib files along the path to the format that 
	Rivest and Shen's GT code will accept. 
    """

	for fn in glob.glob(path):
		print(fn)
		convert(fn[:-4], ext)

convert_files("**/*.toc", "toc")
