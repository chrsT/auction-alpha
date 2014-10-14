import Genetics, Agents, Simulation, Transactions, PARAMETERS, ENUMS
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
		""" Takes Genome1 and Genome2, returns new Genome object """
		pass

	def get(self,key):
		return self.genes.get(key,None)

	def get_value(self,key):
		return self.genes.get(key,None).value

	def __str__(self):
		""" Returns string representation of Genome """
		return PARAMETERS.GENOME_STRING.format(**self.genes)

class Gene:
	"""
	Class Gene:
		Abstract Class.
	
	"""
	@classmethod
	def CLASS_breed(gene_1,gene_2):
		raise NotImplementedError

	def __init__(self,value):
		self.value = value
		raise NotImplementedError

	def __str__(self):
		raise NotImplementedError

class DistinctGene(Gene):
	"""
	Class DistinctGene(Gene):
		Abstract Class.

	"""
	@classmethod
	def CLASS_breed(gene_1,gene_2):
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
	def CLASS_breed(gene_1,gene_2):
		pass

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
	def CLASS_breed(gene_1,gene_2):
		pass

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
	def CLASS_breed(gene_1,gene_2):
		pass

	def __init__(self,value):
		self.range = 0,1023
		if int(value) < self.range[0] or int(value) > self.range[1]:
			raise
		self.value = int(value)

	def __str__(self):
		return str(self.value)
