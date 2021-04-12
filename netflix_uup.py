import glob

def mle_soc(filename):
	"""
	Converts the preflib soc file to a dictionary where the key is the vector and the value
    is the number of people whose vote was that vector. Assumes strict complete ordering,
    which is advertised as true of all soc files.

    """
	input = open(filename, "r")
	text = input.read()
	lines = text.split("\n")

	# Skip over list of canidates, other metadata
	num_alts = lines[0]
	lines = lines[int(num_alts)+1:]
	metadata = lines[0].split(",")
	n = float(metadata[0])
	lines = lines[1:-1]

	mle = {}

	for line in lines:
		votes = line.split(",")
		val = votes[0]
		mle[tuple(votes[1:])] = float(val)/n

	return mle

def netflix_mles():
	"""
	Returns a list of dicts, where each dict holds the MLE of one of the "elections" from
	the Netflix Prize dataset. In each dict, the keys are tuples of vote vectors, and the values
	are the proportion of voters in that election that picked the corresponding vote vector.

    """
	mles = []
	for fn in glob.glob("**/*.soc"):
		mles.append(mle_soc(fn))

	return mles
