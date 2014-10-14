import Genetics, Agents, Simulation, Transactions, PARAMETERS, ENUMS
import os, sys, datetime, time

from enum import Enum

class TransactionDecision(Enum):
	cooperate = 1
	defect = 2
	decline = 3

class StrategyEnum(Enum):
	dove = 1
	hawk = 2

class GeneTypeEnum(Enum):
	distinct = 1
	int_val = 2

class FeedbackValue(Enum):
	positive = 1
	negative = 2

class SimulationState(Enum):
	new = 1
	init = 2
	run = 3
	
class TransactionState(Enum):
	initialised = 1
	executed = 2
	feedback = 3
	completed = 4
