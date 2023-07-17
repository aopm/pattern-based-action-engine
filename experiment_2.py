import random
from algorithm import ActionInstance, ActionCandidate
from algorithm import plan_actions
import networkx as nx
import pandas as pd
import csv

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
    output_filename = './data/exp-2.csv'
    header = ['repetition', 'NUM_ACTIONS', 'OCCURRENCE_RATIO', 'conflct_ratio', 'time_performance', 'makespan', 'total_waiting_time', 'total_flow_time']
    with open(output_filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

    records = []
    NUM_ACTIONS = 500
    NUM_EXECUTION = 3
    OCCURRENCE_RATIO = 1
    actions = generate_actions(NUM_ACTIONS)
    
    for i in range(1,100):
        conflict_ratio = i/100
        for rep in range(1,11):
            action_candidates = generate_action_candidates(actions,OCCURRENCE_RATIO)
            action_conflict = generate_action_conflict(action_candidates, conflict_ratio)
            time_performance_list = []
            makespan_list = []
            total_waiting_time_list = []
            total_flow_time_list = []
            for i in range(NUM_EXECUTION):
                # as action_candidates are emptied after plan_actions, we need to copy it
                action_instances, time_performance, makespan, total_waiting_time, total_flow_time = plan_actions(action_candidates.copy(),action_conflict)
                time_performance_list.append(time_performance)
                makespan_list.append(makespan)
                total_waiting_time_list.append(total_waiting_time)
                total_flow_time_list.append(total_flow_time)
            # compute average time performance
            time_performance = sum(time_performance_list)/len(time_performance_list)
            makespan = sum(makespan_list)/len(makespan_list)
            total_waiting_time = sum(total_waiting_time_list)/len(total_waiting_time_list)
            total_flow_time = sum(total_flow_time_list)/len(total_flow_time_list)

            row = {'repetition': rep, 'NUM_ACTIONS': NUM_ACTIONS, 'OCCURRENCE_RATIO': OCCURRENCE_RATIO, 'conflct_ratio': conflict_ratio, 'time_performance': time_performance, 'makespan': makespan, 'total_waiting_time': total_waiting_time, 'total_flow_time': total_flow_time}
            
            # Write the row to your csv file
            with open(output_filename, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writerow(row)
            
            records.append(row)
