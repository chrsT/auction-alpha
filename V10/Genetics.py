import Genetics, Agents, Simulation, Transactions, PARAMETERS, ENUMS, RANDOMS
import os, sys, datetime, time

class Genome:
	"""
	Class Genome:

	"""
	
	def __init__(self,genome_string):
		self.genes = {}
		genes_list = genome_string.split("-")
		
		#Version Check
		if genes_list[0] != PARAMETERS.VERSION:
			raise
		
		#Strategy
		self.genes["strategy"] = StrategyGene(StrategyGene.str_to_enum(genes_list[1]))

		#RepWeighting
		self.genes["rep-weighting"] = RepWeightingGene(genes_list[2])

		#ProbDefect
		self.genes["prob-defect"] = ProbDefectGene(genes_list[3])
		
	@classmethod
	def CLASS_breed(self,Genome1,Genome2):
		""" Takes Genome1 and Genome2, returns new genome string"""
		new_gen = {}
		for key in ["strategy","rep-weighting","prob-defect"]:
			gene1 = Genome1.get(key)
			gene2 = Genome2.get(key)
			new_gen[key] = gene1.CLASS_breed(gene1,gene2)

		gen_string = PARAMETERS.GENOME_STRING.format(**new_gen)
		return gen_string

	def get(self,key):
		return self.genes.get(key,None)

	def get_value(self,key):
		return self.genes.get(key,None).get_value()

	def __str__(self):
		""" Returns string representation of Genome """
		return PARAMETERS.GENOME_STRING.format(**self.genes)

class Gene:
	"""
	Class Gene:
		Abstract Class.
	
	"""
	@classmethod
	def CLASS_breed(self,gene_1,gene_2):
		raise NotImplementedError

	def __init__(self,value):
		self.value = value
		raise NotImplementedError

	def __str__(self):
		raise NotImplementedError

	def get_value(self):
		return self.value

class DistinctGene(Gene):
	"""
	Class DistinctGene(Gene):
		Abstract Class.

	"""
	@classmethod
	def CLASS_breed(self,gene_1,gene_2):
		raise NotImplementedError

	def __init__(self,value):
		self.possible_values = None
		self.value = value
		raise NotImplementedError
				
	
	def __str__(self):
		raise NotImplementedError

class IntGene(Gene):
	"""
	Class IntGene(Gene):
		Abstract Class
	"""
	@classmethod
	def CLASS_breed(gene_1,gene_2):
		raise NotImplementedError

	def __init__(self,value):
		self.range = None,None	
		self.value = value
		raise NotImplementedError
	
	def __str__(self):
		raise NotImplementedError

class StrategyGene(DistinctGene):
	"""
	Class StrategyGene(DistinctGene):
	
	"""
	@classmethod
	def CLASS_breed(self,gene_1,gene_2):
		if gene_1.get_value() == ENUMS.StrategyEnum.hawk and gene_2.get_value() == ENUMS.StrategyEnum.hawk:
			val =  ENUMS.StrategyEnum.hawk
		elif gene_1.get_value() == ENUMS.StrategyEnum.dove and gene_2.get_value() == ENUMS.StrategyEnum.dove:
			val = ENUMS.StrategyEnum.dove
		else:
			val = RANDOMS.binary_random_decision(PARAMETERS.GENETICS_STRATEGY_HAWK_DOM,ENUMS.StrategyEnum.hawk,ENUMS.StrategyEnum.dove)

		if RANDOMS.binary_random_decision(PARAMETERS.GENETICS_STRATEGY_MUTATE,True,False):
			if val == ENUMS.StrategyEnum.hawk:
				val = ENUMS.StrategyEnum.dove
			elif val == ENUMS.StrategyEnum.dove:
				val = ENUMS.StrategyEnum.hawk
		return StrategyGene(val)
				
	@classmethod
	def str_to_enum(self,value):
		if value == "H":
			return ENUMS.StrategyEnum.hawk
		elif value == "D":
			return ENUMS.StrategyEnum.dove
		else:
			raise
	
	def __init__(self,value):
		self.possible_values = ENUMS.StrategyEnum
		self.value = value
	
	def __str__(self):
		if self.value == ENUMS.StrategyEnum.dove:
			return "D"
		elif self.value == ENUMS.StrategyEnum.hawk:
			return "H"
		else:
			raise

class ProbDefectGene(IntGene):
	"""
	Class ProbDefectGene(IntGene):
	
	"""
	@classmethod
	def CLASS_breed(self,gene_1,gene_2):
		val = int((gene_1.get_value() + gene_2.get_value())/2)
		val += RANDOMS.random_int(PARAMETERS.GENETICS_PROB_DEFECT_RAND_MIN,PARAMETERS.GENETICS_PROB_DEFECT_RAND_MAX)
		if val < 0:
			val = 0
		if val > 1023:
			val = 1023

		return val

	def __init__(self,value):
		self.range = 0,1023
		if int(value) < self.range[0] or int(value) > self.range[1]:
			raise
		self.value = int(value)

	def __str__(self):
		return str(self.value)

class RepWeightingGene(IntGene):
	"""
	Class RepWeightingGene(IntGene):

	"""
	@classmethod
	def CLASS_breed(self,gene_1,gene_2):
		val = int((gene_1.get_value() + gene_2.get_value())/2)
		val += RANDOMS.random_int(PARAMETERS.GENETICS_REP_WEIGHTING_RAND_MIN,PARAMETERS.GENETICS_REP_WEIGHTING_RAND_MAX)
		if val < 0:
			val = 0
		if val > 1023:
			val = 1023

		return val

	def __init__(self,value):
		self.range = 0,1023
		if int(value) < self.range[0] or int(value) > self.range[1]:
			raise
		self.value = int(value)

	def __str__(self):
		return str(self.value)
