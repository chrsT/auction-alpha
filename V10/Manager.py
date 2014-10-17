import Genetics, Agents, Simulation, Transactions, PARAMETERS, ENUMS, RANDOMS
import os, sys, datetime, time

import statistics

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

		if len(doves) > 0:
			d["doves"]["mean"] = statistics.mean(doves)
			d["doves"]["stdev"] = statistics.stdev(doves)
			d["doves"]["median"] = statistics.median(doves) #Also need first and third quartiles for box plottings.
		else:
			d["doves"]["mean"] = 0
			d["doves"]["stdev"] = 0
			d["doves"]["median"] = 0			

		if len(hawks) > 0:
			d["hawks"]["mean"] = statistics.mean(hawks)
			d["hawks"]["stdev"] = statistics.stdev(hawks)
			d["hawks"]["median"] = statistics.median(hawks)
		else:
			d["hawks"]["mean"] = 0
			d["hawks"]["stdev"] = 0
			d["hawks"]["median"] = 0
		
		return d
		

	def gene_stats(self,generation):
		return None

	def strategy_score_correlation(self,generation):
		return None

	def gene_score_correlation(self,generation):
		return None
				
	
class Manager:
	def __init__(self,n_generations,n_agents):
		self.n_generations = n_generations
		self.n_agents = n_agents
		self.stats = []

	def run(self):
		agents = None
		for i in range(0,self.n_generations):
			gen = Generation(i,agents)
			gen.run()
			self.stats.append(gen.get_stats())
			agents = gen.next_generation()
			
if __name__ == "__main__":
	man = Manager(PARAMETERS.GENERATIONS_TO_DO,PARAMETERS.N_AGENTS)
	man.run()
