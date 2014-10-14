''' Auction Simulation Version 0.2 (V02) '''
from random_functions import *
from Agent import *
from enum import Enum
import datetime

def write_out(line):
	print("[{}] {}".format(datetime.datetime.now(),line))

class ReputationAction(Enum):
	positive = 1
	negative = 2
	neutral = 3
class Transaction:
	def __init__(self,ID,agent_1,agent_1_choice,agent_2,agent_2_choice):
		self.id = ID
		self.agent_1 = agent_1
		self.agent_1_choice = agent_1_choice
		self.agent_2 = agent_2
		self.agent_2_choice = agent_2_choice

	def get_payoff(self,agent):
		if agent == self.agent_1:
			return self.payoff_matrix(self.agent_1_choice,self.agent_2_choice)
		elif agent == self.agent_2:
			return self.payoff_matrix(self.agent_2_choice,self.agent_1_choice)
		else:
			return 0

	def spec_agent_decision(self,agent):
		if agent == self.agent_1:
			return self.agent_1_choice
		elif agent == self.agent_2:
			return self.agent_2_choice
		return 0

	def other_agent_decision(self,agent):
		if agent == self.agent_2:
			return self.agent_1_choice
		elif agent == self.agent_1:
			return self.agent_2_choice
		return 0

	def payoff_matrix(self,a1d,a2d):
		if a1d == TransactionDecision.decline or a2d == TransactionDecision.decline:
			return PARAMETERS.PAYOFF_DECL
		elif a1d == TransactionDecision.cooperate and a2d == TransactionDecision.cooperate:
			return PARAMETERS.PAYOFF_COOP
		elif a1d == TransactionDecision.cooperate and a2d == TransactionDecision.defect:
			return PARAMETERS.PAYOFF_DAGA
		elif a1d == TransactionDecision.defect and a2d == TransactionDecision.cooperate:
			return PARAMETERS.PAYOFF_DDON
		elif a1d == TransactionDecision.defect and a2d == TransactionDecision.defect:
			return PARAMETERS.PAYOFF_DBOT
class Simulation:
	def print_scoreboard(self,agent_list=None):
		scoreboard_string = ""
		if agent_list is None:
			agent_list = self.agents_list
		sorted_list = sorted(agent_list,key=lambda agent: agent.score)
		for a in sorted_list:
			scoreboard_string += "Agent ID: {}, Score: {}, Genome: {}, Decisions: {}\n".format(a.id,a.score,a.genome,a.get_decisions())
		return scoreboard_string

	def generate_random_agents(self,n_agents):
		l = []
		for i in range(0,n_agents):
			agent_string = "V02-{}-{}-{}".format(binary_random_decision(PARAMETERS.INITIAL_HAWK,"H","D"),random_int(0,1023),random_int(0,1023))
			l.append(Agent.CreateAgent(agent_string))
		return l
			
	def __init__(self,agent_strings=None,n_transactions=None):
		self.n_agents = None	
		self.n_transactions = None
		self.transaction_list = []
		self.agents_list = []
		self.simulation_run = None

		if agent_strings is None:
			self.n_agents = PARAMETERS.N_AGENTS
			self.agents_list = self.generate_random_agents(self.n_agents)
		else:
			for s in agent_strings:
				self.agents_list.append(Agent.CreateAgent(s))
			self.n_agents = len(self.agents_list)
		if n_transactions is None:
			self.n_transactions = self.n_agents * PARAMETERS.TRANS_PER_AGENT
		else:
			self.n_transactions = n_transactions
		self.simulation_run = False

	def run_simulation(self):
		if self.simulation_run:
			raise
		for roun in range(0,self.n_transactions):
			if PARAMETERS.VERBOSE_SIM:
				if (roun % PARAMETERS.VERBOSE_SIM_N) == 0:
					write_out("{}/{}".format(roun,self.n_transactions))
			agent_one, agent_two = two_random_agents(self.agents_list)
			self.process_transaction(agent_one,agent_two,roun)
		#self.print_scoreboard(self.agents_list)
		self.simulation_run = True

	def next_generation(self):
		top_list = self.get_top_x_agents(PARAMETERS.TOP_X)
		new_generation = self.breed_up(top_list)
		return new_generation

	def get_top_x_agents(self,x):
		sorted_list = sorted(self.agents_list,key=lambda agent: agent.score,reverse=True)
		cut_list = sorted_list[:x]
		return cut_list

	def breed_up(self,start_list,n=PARAMETERS.N_AGENTS):
		children = []
		for i in range(0,n):
			parent1,parent2 = two_random_agents(start_list)
			children.append(Genome.breed(str(parent1.genome),str(parent2.genome)))
		return children

	def process_transaction(self,agent_one,agent_two,roun):
		'''TODO: Transaction logging, feedback '''
		a1d = agent_one.transaction_decision(agent_two)
		a2d = agent_two.transaction_decision(agent_one)
		transaction = Transaction(roun,agent_one,a1d,agent_two,a2d)
		agent_one.transaction_list.append(transaction)
		agent_two.transaction_list.append(transaction)
		self.transaction_list.append(transaction)


