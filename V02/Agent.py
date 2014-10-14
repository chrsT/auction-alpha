''' Auction Simulation Version 0.2 (V02) '''
from enum import Enum
import random
import PARAMETERS
import random_functions

class TransactionDecision(Enum):
	cooperate = 1
	defect = 2
	decline = 3

class StrategyEnum(Enum):
	hawk = 1
	dove = 2

class GeneTypeEnum(Enum):
	binary_decision = 1
	prob_var = 2

class Gene:
	def __init__(self):
		raise NotImplementedError()
	
	def breed(val_1,val_2):
		raise NotImplementedError()

class StrategyGene(Gene):
	@classmethod
	def breed(self,val_1,val_2):
		val = 0
		if val_1 == StrategyEnum.hawk and val_2 == StrategyEnum.hawk:
			val = StrategyGene(StrategyEnum.hawk)
		elif val_1 == StrategyEnum.hawk and val_2 == StrategyEnum.dove or val_1 == StrategyEnum.dove and val_2 == StrategyEnum.hawk:
			val = random_functions.binary_random_decision(PARAMETERS.HAWK_DOMINANCE,StrategyGene(StrategyEnum.hawk),StrategyGene(StrategyEnum.dove))
		else:
			val = StrategyGene(StrategyEnum.dove)
		mutate = random_functions.binary_random_decision(PARAMETERS.MUTATE_BINARY,True,False)
		if mutate:
			if str(val) == "H":
				val = StrategyGene(StrategyEnum.dove)
			else:
				val = StrategyGene(StrategyEnum.hawk)
		return val

	@classmethod
	def letter_to_number(self,val):
		if val == "D":
			return StrategyEnum.dove
		else:
			return StrategyEnum.hawk
	def __init__(self,value):
		self.gene_type = GeneTypeEnum.binary_decision
		values = StrategyEnum
		self.value = value

	def __str__(self):
		if self.value == StrategyEnum(1):
			return "H"
		if self.value == StrategyEnum(2):
			return "D"
		
class RepWeightingGene(Gene):
	@classmethod
	def breed(self,value1,value2):
		val = (int(value1)+int(value2))/2
		val += random_functions.random_int(PARAMETERS.MUTATE_PROB_LOWER,PARAMETERS.MUTATE_PROB_UPPER)
		if val > 1023:
			val = 1023
		if val < 0:
			val = 0
		return int(val)
		
	def __init__(self,value):
		self.gene_type = GeneTypeEnum.prob_var
		values = 0,1023
		self.value = value

	def __str__(self):
		return "{val:04d}".format(val=self.value)

class ProbDefectGene(Gene):
	@classmethod
	def breed(self,value1,value2):
		val = (int(value1)+int(value2))/2
		val += random_functions.random_int(PARAMETERS.MUTATE_PROB_LOWER,PARAMETERS.MUTATE_PROB_UPPER)
		if val > 1023:
			val = 1023
		if val < 0:
			val = 0

		return int(val) 

	def __init__(self,value):
		self.gene_type = GeneTypeEnum.prob_var
		values = 0,1023
		self.value = value

	def __str__(self):
		return "{val:04d}".format(val=self.value)	

class Genome:
	''' Specification for version 0.2 genome '''
	''' V02-[strategy]-[rep-weighting]-[prob-defect] '''
	''' strategy - Either "H" or "D", for Hawk or Dove '''
	''' rep-weighting - How much a dove places on past transactions when deciding whether to trade 4 digit number, 0000-1023 '''
	version = "V02"
	def __init__(self,genome_string):
		self.genes = {}
		genome_list = genome_string.split("-")
		if genome_list[0] != Genome.version:
			raise
	
		if genome_list[1] == "H":
			self.genes["strategy"] = StrategyGene(StrategyEnum.hawk)
		elif genome_list[1] == "D":
			self.genes["strategy"] = StrategyGene(StrategyEnum.dove)

		#genome_list[2] -- rep-weighting
		self.genes["rep-weighting"] = int(genome_list[2])

		#genome_list[3] -- prob-defect
		self.genes["prob-defect"] = int(genome_list[3])

	def __str__(self):
		return "{}-{}-{}-{}".format(Genome.version,self.genes["strategy"],self.genes["rep-weighting"],self.genes["prob-defect"])
		
	@classmethod
	def breed(self,genomeA,genomeB):
		child = ""+Genome.version

		genomeA_list = genomeA.split("-")
		genomeB_list = genomeB.split("-")

		child += "-{}".format(StrategyGene.breed(StrategyGene.letter_to_number(genomeA_list[1]),StrategyGene.letter_to_number(genomeB_list[1])))
		
		child += "-{num:04d}".format(num=RepWeightingGene.breed(genomeA_list[2],genomeB_list[2]))
		child += "-{num:04d}".format(num=ProbDefectGene.breed(genomeA_list[3],genomeB_list[3]))
		return child

class Agent:
	version = "V02"
	N_ID = 0

	@classmethod
	def CreateAgent(self,genome_string): #Returns a HawkAgent with Genome as defined by genome_string 
		genome_list = genome_string.split("-")
		if genome_list[0] != Agent.version:
			raise
	
		if genome_list[1] == "H":
			agent = HawkAgent()
		elif genome_list[1] == "D":
			agent = DoveAgent()

		agent.genome = Genome(genome_string)
		return agent	
		
	def __init__(self):
		self.id = Agent.N_ID
		Agent.N_ID += 1
		self.transaction_list = []

	@property
	def score(self):
		score = 0
		for t in self.transaction_list:
			score += t.get_payoff(self)
		return score

	def transaction_decision(self,other_agent):
		'''Needs to decide whether or not to trade with said agent'''
		raise NotImplementedError()

	def get_feedback(self):
		pos = 0
		neu = 0
		neg = 0
		for t in self.transaction_list:
			decision = t.spec_agent_decision(self)
			other = t.other_agent_decision(self)
			#if other == TransactionDecision.decline:
			#	neu += 1
			if decision == TransactionDecision.cooperate:
				pos += 1
			elif decision == TransactionDecision.defect:
				neg += 1
			#else:
			#	neu += 1
		return pos,neu,neg

	def get_decisions(self):
		coop = 0
		defe = 0
		decl = 0
		for t in self.transaction_list:
			decision = t.spec_agent_decision(self)
			if decision == TransactionDecision.cooperate:
				coop += 1
			elif decision == TransactionDecision.defect:
				defe += 1
			else:
				decl += 1

		return coop,decl,defe
class HawkAgent(Agent):
	def __init__(self):
		super().__init__()
	
	def transaction_decision(self,other_agent):
		if random_functions.random_int(0,1024) < self.genome.genes["prob-defect"]:
			return TransactionDecision.defect
		else:
			return TransactionDecision.cooperate

class DoveAgent(Agent):
	def __init__(self):
		super().__init__()

	def transaction_decision(self,other_agent):
		feedback_tuple = other_agent.get_feedback()
		pos = feedback_tuple[0]
		neu = feedback_tuple[1]
		neg = feedback_tuple[2]
		total = pos+neu+neg
		if True:
			P_defect = neg/(neg+pos+1) #not counting neutrals
			weighted_P_defect = (self.genome.genes["rep-weighting"]/768) * P_defect
			if (weighted_P_defect*PARAMETERS.PAYOFF_DAGA)+((1-weighted_P_defect)*PARAMETERS.PAYOFF_COOP) > 0:
				return TransactionDecision.cooperate
			else:
				return TransactionDecision.decline
		return TransactionDecision.cooperate
