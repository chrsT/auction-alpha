import Simulation, Agent, PARAMETERS
import sys, time,os,datetime
def count_type(agent_list):
	h = 0; d = 0;
	for a in agent_list:
		if isinstance(a,Agent.HawkAgent):
			h += 1
		else:
			d += 1
	return h,d

def write_out(line):
	print("[{}] {}".format(datetime.datetime.now(),line))

if __name__ == "__main__":
	filename = "{}-time-{}".format(PARAMETERS.VERSION,time.time())
	os.system("mkdir dump/{}".format(filename))
	write_out("AUCTION SIMULATOR THING. ALPHA VERSION {}".format(PARAMETERS.VERSION))
	next = None
	for i in range(1,PARAMETERS.GENERATIONS_TO_DO):
		sim = Simulation.Simulation(agent_strings=next)
		sim.run_simulation()
		write_out("GENERATION {}".format(i))
		generation_breakdown = count_type(sim.agents_list)
		top_X = count_type(sim.get_top_x_agents(PARAMETERS.TOP_X))
		write_out("Whole population: H: {}, D: {}".format(generation_breakdown[0],generation_breakdown[1]))
		write_out("Top 20: H: {}, D: {}".format(top_X[0],top_X[1]))
		write_out("-----------------------\n\n")
		next = sim.next_generation()
		write_out("Dumping to file: dump/{}/gen-{}".format(filename,i))
		f = open("dump/{}/gen-{}".format(filename,i),"w")
		f.write("GENERATION {}\n----------\n".format(i))
		f.write(sim.print_scoreboard())
		f.close()
	write_out(sim.agents_list)
		
