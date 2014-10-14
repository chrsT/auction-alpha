import Genetics, Agents, Simulation, Transactions, PARAMETERS, ENUMS
import os, sys, datetime, time

class TransactionList(list):
	"""
	Class: TransactionList

	"""
	def get_transactions(self,agent):
		ret_val = []
		for t in self:
			if t.agent_1 == agent or t.agent_2 == agent:
				ret_val.append(t)
		return ret_val

	def get_score(self,agent):
		transactions = self.get_transactions(agent)
		score = 0
		for t in self:
			score += t.get_score(agent)
		return score

class Transaction:
	"""
	Class: Transaction

	"""
	def __init__(self,agent1,agent2):
		self.agent_1 = agent1
		self.agent_2 = agent2
		self.transaction_state = ENUMS.TransactionState.initialised

	def other_agent(self,agent):
		if self.agent_1 == agent:
			return self.agent_2
		elif self.agent_2 == agent:
			return self.agent_1
		else:
			raise

	def get_decision(self,agent):
		if self.agent_1 == agent:
			return self.decision_1
		elif self.agent_2 == agent:
			return self.decision_2
		else:
			raise

	def execute_transaction(self):
		if self.transaction_state != ENUMS.TransactionState.initialised:
			raise
		self.decision_1 = self.agent_1.AUT_transaction_decision(self.agent_2)
		self.decision_2 = self.agent_2.AUT_transaction_decision(self.agent_1)
		self.transaction_state = ENUMS.TransactionState.executed

		if self.decision_1 == ENUMS.TransactionDecision.decline or self.decision_2 == ENUMS.TransactionDecision.decline:
			self.agent_1.new_transaction(self)
			self.agent_2.new_transaction(self)
			self.transaction_state = ENUMS.TransactionState.completed
		else:
			self.execute_feedback()

	def execute_feedback(self):
		if self.transaction_state != ENUMS.TransactionState.executed:
			raise
		a1f = self.agent_1.AUT_leave_feedback(self)
		a2f = self.agent_2.AUT_leave_feedback(self)
		
		self.agent_2.new_transaction(self,feedback_value=a1f)
		self.agent_1.new_transaction(self,feedback_value=a2f)

		self.transaction_state = ENUMS.TransactionState.completed

	def get_score(self,agent):
		if self.transaction_state == ENUMS.TransactionState.initialised:
			raise			
		if self.agent_1 == agent:
			a1d = self.decision_1
			a2d = self.decision_2
		elif self.agent_2 == agent:
			a1d = self.decision_2
			a2d = self.decision_1
		else:
			raise

		if a1d == ENUMS.TransactionDecision.decline or a2d == ENUMS.TransactionDecision.decline:
			return PARAMETERS.PAYOFF_DECL
		elif a1d == ENUMS.TransactionDecision.cooperate and a2d == ENUMS.TransactionDecision.cooperate:
			return PARAMETERS.PAYOFF_COOP
		elif a1d == ENUMS.TransactionDecision.cooperate and a2d == ENUMS.TransactionDecision.defect:
			return PARAMETERS.PAYOFF_DAGA
		elif a1d == ENUMS.TransactionDecision.defect and a2d == ENUMS.TransactionDecision.cooperate:
			return PARAMETERS.PAYOFF_DDON
		elif a1d == ENUMS.TransactionDecision.defect and a2d == ENUMS.TransactionDecision.defect:
			return PARAMETERS.PAYOFF_DBOT
