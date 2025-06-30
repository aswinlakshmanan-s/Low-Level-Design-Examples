from abc import ABC, abstractmethod
from typing import List, Dict
from collections import defaultdict
from threading import Lock
import random

# Simple Agent class
class Agent:
    def __init__(self, agent_id: int, name: str):
        self.agent_id = agent_id
        self.name = name
        self.open_issues = 0
        self.resolved_issues = 0

    def __repr__(self):
        return f"{self.name}(Open: {self.open_issues}, Resolved: {self.resolved_issues})"

# Simple Issue class
class Issue:
    def __init__(self, issue_id: int, description: str):
        self.issue_id = issue_id
        self.description = description
        self.assigned_to = None
        self.resolved = False

# Strategy Interface
class AssignmentStrategy(ABC):
    @abstractmethod
    def assign(self, agents: List[Agent], issue: Issue) -> Agent:
        pass

    # Observer method — get notified when issue is resolved
    def on_issue_resolved(self, agent: Agent):
        pass

# Example Strategy: assign agent with least open issues
class LeastLoadedStrategy(AssignmentStrategy):
    def assign(self, agents: List[Agent], issue: Issue) -> Agent:
        return min(agents, key=lambda a: a.open_issues)

# Main Support System (Observer + Strategy holder)
class CustomerSupportSystem:
    def __init__(self, strategy: AssignmentStrategy):
        self.agents: List[Agent] = []
        self.issues: Dict[int, Issue] = {}
        self.strategy = strategy
        self.lock = Lock()
        self.issue_counter = 1

    def add_agent(self, name: str):
        agent = Agent(agent_id=len(self.agents)+1, name=name)
        self.agents.append(agent)

    def create_issue(self, description: str) -> int:
        with self.lock:
            issue_id = self.issue_counter
            issue = Issue(issue_id, description)
            agent = self.strategy.assign(self.agents, issue)
            issue.assigned_to = agent
            agent.open_issues += 1
            self.issues[issue_id] = issue
            print(f"Issue {issue_id} assigned to {agent.name}")
            self.issue_counter += 1
            return issue_id

    def resolve_issue(self, issue_id: int):
        with self.lock:
            if issue_id in self.issues:
                issue = self.issues[issue_id]
                if not issue.resolved and issue.assigned_to:
                    issue.resolved = True
                    agent = issue.assigned_to
                    agent.open_issues -= 1
                    agent.resolved_issues += 1
                    self.strategy.on_issue_resolved(agent)
                    print(f"Issue {issue_id} resolved by {agent.name}")

    def list_agents(self):
        for a in self.agents:
            print(a)
