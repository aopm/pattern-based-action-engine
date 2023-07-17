import random
from algorithm import ActionInstance, ActionCandidate
from algorithm import plan_actions
import networkx as nx
import pandas as pd

def generate_actions(n):
    return [f'a{i}' for i in range(1,n,1)]

def generate_action_candidates(actions,prob):
    action_candidates = []
    for action in actions:
        if random.uniform(0, 1) <= prob:
            action_candidates.append(ActionCandidate(action,1))
    return action_candidates

def generate_action_conflict(actions, prob):
    G = nx.DiGraph()
    G.add_nodes_from(actions)
    nodes = list(G.nodes)
    for i in range(len(nodes)):
        for j in range(i+1,len(nodes)):
            if random.uniform(0, 1) <= prob:
                G.add_edge(nodes[i],nodes[j])
    return G


if __name__ == "__main__":
    # records = []
    # num_actions = 100
    # occurrence_ratio = 1
    # conflict_ratio = 0.1
    # actions = generate_actions(num_actions)
    # action_candidates = generate_action_candidates(actions,occurrence_ratio)
    # action_conflict = generate_action_conflict(actions, conflict_ratio)
    # action_instances, time_performance, makespan, total_waiting_time, total_flow_time = plan_actions(action_candidates,action_conflict)
    # records.append({'repetition': 0, 'num_actions': num_actions, 'occurrence_ratio': occurrence_ratio, 'conflct_ratio': conflict_ratio, 'time_performance': time_performance, 'makespan': makespan, 'total_waiting_time': total_waiting_time, 'total_flow_time': total_flow_time})
    # print(action_conflict)
    # print(action_instances)

    records = []
    occurrence_ratio = 1
    for i in range(1,10):
        for num_actions in range(100,1100,100):
            actions = generate_actions(num_actions)
            action_candidates = generate_action_candidates(actions,occurrence_ratio)
            conflict_ratio = i/10
            action_conflict = generate_action_conflict(action_candidates, conflict_ratio)
            action_instances, time_performance, makespan, total_waiting_time, total_flow_time = plan_actions(action_candidates,action_conflict)
            records.append({'repetition': 0, 'num_actions': num_actions, 'occurrence_ratio': occurrence_ratio, 'conflct_ratio': conflict_ratio, 'time_performance': time_performance, 'makespan': makespan, 'total_waiting_time': total_waiting_time, 'total_flow_time': total_flow_time})
    df = pd.DataFrame(records)
    df.to_csv('./data/exp-1.csv')
