import Genetics, Agents, Simulation, Transactions, PARAMETERS, ENUMS
import os, sys, datetime, time

def write_out(line):
	print("[{}] {}".format(datetime.datetime.now(),line))

class Simulation:
	"""
	Class Simulation
	
	"""
	def __init__(self):
		self.transaction_list = Transactions.TransactionList()
		self.agent_list = Agents.AgentList()
		for a in self.generate_random_agents(PARAMETERS.N_AGENTS):
			self.agent_list.append(a)

	def run_simulation(self):
		write_out("Simulation running")
		self.n_transactions = PARAMETERS.N_AGENTS * PARAMETERS.TRANS_PER_AGENT
		for roun in range(0,self.n_transactions):
			if PARAMETERS.DEBUG and PARAMETERS.VERBOSE_SIMULATION and (roun % PARAMETERS.VERBOSE_SIMULATION_N == 0):
				write_out("{}/{}".format(roun,self.n_transactions))
			a1,a2 = self.agent_list.get_two_random()
			transaction = Transactions.Transaction(a1,a2)
			transaction.execute_transaction()
			self.transaction_list.append(transaction)
		write_out("Simulation finished.")

	def ordered_agents(self):
		return sorted(self.agent_list,key=lambda agent: agent.score)

	def print_leaderboard(self):
		ordered = self.ordered_agents()
		for o in ordered:
			print("{} - Score: {} - Decisions: {} - Feedback: {}".format(o,o.get_score(),o.get_decisions(),o.get_feedback()))

	@classmethod
	def generate_random_agents(self,n):
		ret_val = []
		for i in range(0,n):
			ret_val.append(Agents.Agent.CLASS_generate_random_agent())

		return ret_val
