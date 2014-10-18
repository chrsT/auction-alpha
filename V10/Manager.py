import Genetics, Agents, Simulation, Transactions, PARAMETERS, ENUMS, RANDOMS
import os, sys, datetime, time

import statistics
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import threading, multiprocessing

def write_out(line):
	print("[{}] {}".format(datetime.datetime.now(),line))

class Generation:
	def __init__(self,ID,agents):
		self.generation_id = ID
		self.agents = agents

	def run(self):
		write_out("Generation {}".format(self.generation_id))
		sim = Simulation.Simulation(agents=self.agents)
		sim.run_simulation()
		self.agents = sim.agent_list
		write_out("Finish Generation {}\n---------\n".format(self.generation_id))

	def get_stats(self):
		self.stats = GenerationStatistics(self.generation_id)
		self.stats.fill_stats(self)
		return self.stats

	def ordered_agents(self):
		return sorted(self.agents,key=lambda agent: agent.score,reverse=True)

	def next_generation(self):
		new_generation = []
		ordered = self.ordered_agents()
		multiplication_list = ordered[:PARAMETERS.TOP_X]
		for i in range(0,PARAMETERS.N_AGENTS):
			a1, a2 = RANDOMS.two_random_agents(multiplication_list)
			new_generation.append(Agents.Agent.CLASS_breed(a1,a2))
		return new_generation
			
			
		
class GenerationStatistics:
	def __init__(self,generation_id):
		self.generation_id = generation_id
		self.stats = {}

	def fill_stats(self,generation):
		self.stats["strategy-stats"] = self.strategy_stats(generation)
		self.stats["score-stats"] = self.score_stats(generation)
		self.stats["gene-stats"] = self.gene_stats(generation)
		self.stats["strategy-score-correlation"] = self.strategy_score_correlation(generation)
		self.stats["gene-score-correlation"] = self.gene_score_correlation(generation)

	def strategy_stats(self,generation):
		n_hawks = 0
		n_doves = 0
		for a in generation.agents:
			if a.get_gene("strategy") == ENUMS.StrategyEnum.hawk:
				n_hawks += 1
			elif a.get_gene("strategy") == ENUMS.StrategyEnum.dove:
				n_doves += 1
		return {"n_hawks" : n_hawks, "n_doves" : n_doves}

	def score_stats(self,generation):
		d = {"top" : {}, "doves" : {}, "hawks" : {}}
		d["top"]["TOP_X"] = PARAMETERS.TOP_X
		hawks = []
		doves = []
		agents = generation.ordered_agents()[:PARAMETERS.TOP_X]
		for a in agents:
			if a.get_gene("strategy") == ENUMS.StrategyEnum.dove:
				doves.append(a.score)
			else:
				hawks.append(a.score)
		
		d["top"]["hawks-top"] = len(hawks)
		d["top"]["doves-top"] = len(doves)

		agents = generation.ordered_agents()
		for a in agents:
			if a.get_gene("strategy") == ENUMS.StrategyEnum.dove:
				doves.append(a.score)
			else:
				hawks.append(a.score)

		d["doves"] = doves
		d["hawks"] = hawks
		
		return d
		

	def gene_stats(self,generation):
		return None

	def strategy_score_correlation(self,generation):
		return None

	def gene_score_correlation(self,generation):
		return None
		
class ThreadingManager:
	def __init__(self,n_simulations=PARAMETERS.N_SIMULATIONS,n_cores=multiprocessing.cpu_count()):
		self.n_simulations = n_simulations
		self.n_cores = n_cores

	def run(self):
		pool = multiprocessing.Pool(processes=self.n_cores)
		self.managers = []
		for i in range(0,self.n_simulations):
			self.managers.append(pool.apply_async(individual_thread,(i,)))


	
def individual_thread(thread):
	write_out("Beginning thread, ID = {}".format(thread))
	man = Manager(ID=thread)
	man.run()
	write_out("Ending thread, ID = {}".format(thread))
	return [a.stats for a in man.stats]
	
class Manager:
	def __init__(self,n_generations=PARAMETERS.GENERATIONS_TO_DO,n_agents=PARAMETERS.N_AGENTS,ID=None):
		self.n_generations = n_generations
		self.n_agents = n_agents
		self.stats = []
		self.begin_time = datetime.datetime.now()
		if ID is None:
			self.ID = datetime.datetime.now()
		else:
			self.ID = ID
		

	def run(self):
		agents = None
		for i in range(0,self.n_generations):
			gen = Generation(i,agents)
			gen.run()
			self.stats.append(gen.get_stats())
			agents = gen.next_generation()

	def show_graph(self):
		doves = []
		hawks = []
		for a in self.stats:
			doves.append(a.stats["score-stats"]["doves"])
			hawks.append(a.stats["score-stats"]["hawks"])

		width = 0.5*0.9
		bar_doves = plt.bar([a-width for a in list(range(1,len(self.stats)+1))],[len(a) for a in doves],width,color="blue")
		bar_hawks = plt.bar([a for a in list(range(1,len(self.stats)+1))],[len(a) for a in hawks],width,color="red")
		bxp_doves = plt.boxplot(doves,widths=width,positions=[a-((51/100)*width) for a in list(range(1,len(self.stats)+1))])
		bxp_hawks = plt.boxplot(hawks,widths=width,positions=[a+((51/100)*width) for a in list(range(1,len(self.stats)+1))])

		plt.setp(bxp_doves["boxes"],color="#191970")
		plt.setp(bxp_doves["whiskers"],color="#191970")
		plt.setp(bxp_doves["fliers"],marker="None")
		plt.setp(bxp_doves["medians"],color="#191970")

		plt.setp(bxp_hawks["boxes"],color="#960018")
		plt.setp(bxp_hawks["whiskers"],color="#960018")
		plt.setp(bxp_hawks["fliers"],marker="None")
		plt.setp(bxp_hawks["medians"],color="#960018")

		plt.xticks(list(range(1,len(self.stats)+1)))

		plt.show()
		
			
if __name__ == "__main__":
	man = Manager(PARAMETERS.GENERATIONS_TO_DO,PARAMETERS.N_AGENTS)
	man.run()
