import itertools
from dataclasses import dataclass, field
from typing import List, Dict, Set, Any, Optional, Union, Tuple
import networkx as nx
import time


@dataclass()
class ActionInstance:
    action: str
    start: int
    end: int


@dataclass(unsafe_hash=True)
class ActionCandidate:
    action: str
    duration: int



def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

def create_action_conflict(precedence_relations):
    if type(precedence_relations) == list:
        G = nx.DiGraph()
        for a, b in precedence_relations:
            G.add_edge(a, b)
    elif type(precedence_relations) == nx.DiGraph:
        G = precedence_relations
    return G

@timing
def instantiate_action_conflict(action_candidates, action_conflict):
    G = nx.DiGraph()
    G.add_nodes_from(action_candidates)
    for a, b in itertools.permutations(action_candidates, 2):
        if (a.action, b.action) in action_conflict.edges():
            G.add_edge(a, b)
    return G


def complete(scheduled,t):
    return [a for a, finish in scheduled if finish <= t]

def compute_total_waiting_time(action_instances: List[ActionInstance]):
    return sum([ai.start-1 for ai in action_instances])

def compute_total_flow_time(action_instances: List[ActionInstance]):
    return sum([ai.end-1 for ai in action_instances])

def plan_actions(action_candidates, action_conflict):
    action_instances = []
    scheduled = []
    t = 0
    # we don't need to instantiate action_conflict as we pass already instantiated action_conflict in the experiments
    # instantiated_action_conflict = instantiate_action_conflict(action_candidates,action_conflict)
    time1 = time.time()
    while len(action_candidates) != 0:
        for can in action_candidates[:]:
            required = set([a for a, b in action_conflict.in_edges(can)])
            completed = set(complete(scheduled,t+1))
            proceed = required.issubset(completed)
            if proceed:
                action_candidates.remove(can)
                scheduled.append((can, can.duration+t+1))
                action_instances.append(ActionInstance(can.action, t+1, t+1+can.duration))
        t += 1
    time2 =  time.time()
    time_performance = round((time2 - time1)*1000.0,3)
    if len(action_instances) >0:
        makespan = max([ai.end for ai in action_instances])
    else:
        makespan = 0
    total_waiting_time = compute_total_waiting_time(action_instances)
    total_flow_time = compute_total_flow_time(action_instances)
    print('planning took {:.3f} ms'.format((time_performance)))
    print(f'makespan: {makespan}')
    print(f'total waiting time: {total_waiting_time}')
    print(f'total flow time: {total_flow_time}')
    return action_instances, time_performance, makespan, total_waiting_time, total_flow_time
