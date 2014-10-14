''' Auction Simulation Version V10 '''
import random
import PARAMETERS
def binary_random_decision(threshold,below,above): #below, above inclusive
	random.seed()
	n = random.randint(0,1023)
	if n <= threshold:
		return below
	else:
		return above

def random_int(lower,upper): #inclusive
	random.seed()
	return random.randint(lower,upper)
