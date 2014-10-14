import Genetics, Agents, Simulation, Transactions, PARAMETERS, ENUMS, RANDOMS
import os, sys, datetime, time

class AgentList(list):
	def get_two_random(self):
		n = len(self)
		if n < 2:
			raise
		n1 = RANDOMS.random_int(0,n-1)
		n2 = RANDOMS.random_int(0,n-1)
		while n1 == n2:
			n2 = RANDOMS.random_int(0,n-1)

		return self[n1],self[n2]
			

class Agent:
	"""
	Class Agent:
		Abstract Class

	"""
	CLASS_N_ID = 0

	@classmethod
	def CLASS_generate_random_agent(self):
		genome_dict = 	{"strategy" : RANDOMS.binary_random_decision(100,"H","D"),
				"prob-defect" : RANDOMS.random_int(0,1023),
				"rep-weighting" : RANDOMS.random_int(0,1023)}

		return Agent.CLASS_create_agent(PARAMETERS.GENOME_STRING.format(**genome_dict))
	
	@classmethod
	def CLASS_create_agent(self,genome_string):
		genome = Genetics.Genome(genome_string)
		if str(genome.get("strategy")) == "D":
			agent = DoveAgent(genome)
		elif str(genome.get("strategy")) == "H":
			agent = HawkAgent(genome)
		else:
			raise

		return agent
		

	def __init__(self,genome):
		self.genome = genome
		self.ID = self.CLASS_N_ID
		Agent.CLASS_N_ID += 1

		self.transaction_list = Transactions.TransactionList()
		
		self.feedback_value_pos = 0
		self.feedback_value_neg = 0

	def AUT_transaction_decision(self,other_agent):
		""" Returns ENUMS.ENUMS.TransactionDecision """
		raise NotImplementedError
	
	def AUT_leave_feedback(self,transaction):
		""" Returns ENUMS.FeedbackValue """
		raise NotImplementedError

	def get_feedback(self):
		""" Returns a tuple: (positive,negative) """
		return self.feedback_value_pos,self.feedback_value_neg

	def new_transaction(self,transaction,feedback_value=0):
		""" Updates internal state with new transaction """
		self.transaction_list.append(transaction)
		if feedback_value == ENUMS.FeedbackValue.positive:
			self.feedback_value_pos += 1
		elif feedback_value == ENUMS.FeedbackValue.negative:
			self.feedback_value_neg += 1

	def get_score(self):
		""" Returns agent's score """
		score = 0
		for t in self.transaction_list:
			score += t.get_score(self)
		return score

	def get_decisions(self):
		coop = 0
		defe = 0
		decl = 0
		for t in self.transaction_list:
			if t.get_decision(self) == ENUMS.TransactionDecision.cooperate:
				coop += 1
			elif t.get_decision(self) == ENUMS.TransactionDecision.defect:
				defe += 1
			elif t.get_decision(self) == ENUMS.TransactionDecision.decline:
				decl += 1
			else:
				raise
		return coop,defe,decl
			

	@property
	def score(self):
		return self.get_score()
		
	def __str__(self):
		raise NotImplementedError

class DoveAgent(Agent):
	"""
	Class DoveAgent(Agent):

	"""
	def __init__(self,genome):
		super().__init__(genome)
	
	def AUT_transaction_decision(self,other_agent):
		pos,neg = other_agent.get_feedback()
		if True:
			P_defect = neg/(neg+pos+1) #not counting neutrals
			weighted_P_defect = (self.genome.get_value("rep-weighting")/768) * P_defect
			if (weighted_P_defect*PARAMETERS.PAYOFF_DAGA)+((1-weighted_P_defect)*PARAMETERS.PAYOFF_COOP) > 0:
				return ENUMS.TransactionDecision.cooperate
			else:
				return ENUMS.TransactionDecision.decline
		return ENUMS.TransactionDecision.cooperate
	
	def AUT_leave_feedback(self,transaction):
		""" Returns ENUMS.FeedbackValue """
		other_agent = transaction.other_agent(self)
		decision = transaction.get_decision(other_agent)
		my_decision = transaction.get_decision(self)
		if decision == ENUMS.TransactionDecision.decline or my_decision == ENUMS.TransactionDecision.decline:
			return 0
		elif decision == ENUMS.TransactionDecision.cooperate:
			return ENUMS.FeedbackValue.positive
		elif decision == ENUMS.TransactionDecision.defect:
			return ENUMS.FeedbackValue.negative
		else:
			return 0
		
	def __str__(self):
		return "Dove Agent. ID: {}. Genome: {}".format(self.ID,self.genome)

class HawkAgent(Agent):
	"""
	Class HawkAgent(Agent):
	"""
	def __init__(self,genome):
		super().__init__(genome)

	def AUT_transaction_decision(self,other_agent):
		pos,neg = self.get_feedback()
		if (neg/(neg+pos+1))*1024 < self.genome.get_value("prob-defect"):
			return ENUMS.TransactionDecision.defect
		else:
			return ENUMS.TransactionDecision.cooperate	
	def AUT_leave_feedback(self,transaction):
		""" Returns ENUMS.FeedbackValue """
		return 0
		
	def __str__(self):
		return "Hawk Agent. ID: {}. Genome: {}".format(self.ID,self.genome)
