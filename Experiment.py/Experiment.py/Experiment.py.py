#########################################################################
#
#     Dynamic Round-Robin CPU Scheduling Algorithm Experiment
#     Austin Edwards & William Spear 
#     April 21,  2023
#     CSCE 321 - Operating Systems
#
#     Features Efficient Dynamic Round Robin
#              Smart Dynamic Round Robin
#              Modified Median Round-Robin Algorithm
#              Standard Rounbd Robin (used as a baseline)
#
#########################################################################

import math
from math import sqrt
import random
import copy
from statistics import median, mean
import random


# Process class to represent each process
class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = None
        self.turnaround_time = None
        self.first_accessed = False
        self.first_time = None
    
    def execute(self, quantum):
        if self.remaining_time <= quantum:
            time_executed = self.remaining_time
            self.remaining_time = 0
        else:
            time_executed = quantum
            self.remaining_time -= quantum
        return time_executed
    
    def is_completed(self):
        return self.remaining_time == 0

#########################################################
#
#     Implementation of Round Robin Algorithm
#
#########################################################
def round_robin(processes, quantum):
    quantum = 2
    context_switches = 0
    time = 0
    completed_processes = []
    ready_queue = []
    n = len(processes)
    last_run_process = None;
    
    while len(completed_processes) < n:

        # adds arriving processes to the ready queue
        processes_to_remove = []
        for process in processes:
            if process.arrival_time <= time:
                ready_queue.append(process)
                processes_to_remove.append(process)
                added_process = True
        for process in processes_to_remove:
            processes.remove(process)
        if last_run_process:
            ready_queue.append(last_run_process)

        # if no processes are in the ready queue, increment the time and continue
        if not ready_queue:
            time += 1
            continue

        # completes a time slice from the next avaliable process
        process = ready_queue.pop(0)
        time_executed = process.execute(quantum)
        if not process.first_accessed:
            process.first_time = time
            process.first_accessed = True
        if process != last_run_process:
            context_switches += 1
        if process.is_completed():
            process.completion_time = time + time_executed
            process.turnaround_time = process.completion_time - process.arrival_time;
            completed_processes.append(process)
            last_run_process = None;
        else:
            last_run_process = process
        
        # increment the time appropriatly
        time += time_executed
    
    return completed_processes, context_switches




#################################################################
#
#     Implementation of Efficient Dynamic Round Robin Algorithm
#
#################################################################
def efficient_dynamic_round_robin(processes):
    context_switches = 0
    time = 0
    completed_processes = []
    ready_queue = []
    n = len(processes)
    last_run_process = None;
    added_process = False;

    # adds arriving processes to the ready queue
    while len(completed_processes) < n:
        added_process = False
        processes_to_remove = []
        for process in processes:
            if process.arrival_time <= time:
                ready_queue.append(process)
                processes_to_remove.append(process)
                added_process = True

        for process in processes_to_remove:
            processes.remove(process)

        # if no processes are in the ready queue, increment the time and continue
        if not ready_queue:
            time += 1
            continue

        # dynamically set the time quantum
        BTmax = 0
        if added_process:
            for process in ready_queue:
                if process.remaining_time > BTmax:
                    BTmax = process.remaining_time
                    quantum = BTmax * 0.8

        # if all processes burt times are greater than the time quantum, set the time quantum to the max
        if all(process.remaining_time > quantum for process in ready_queue):
            quantum = max(process.remaining_time for process in ready_queue)
        
        # Execute each process in the ready queue for the quantum time slice
        processes_to_move_to_back = []
        for process_index, process in enumerate(ready_queue):
            if len(ready_queue) == 1:
                if process != last_run_process:
                    context_switches += 1
                time_executed = process.execute(quantum)
                if not process.first_accessed:
                    process.first_time = time
                    process.first_accessed = True
                if process.is_completed():
                    process.completion_time = time + time_executed
                    process.turnaround_time = process.completion_time - process.arrival_time;
                    completed_processes.append(process)
                    ready_queue.pop(process_index)
                    last_run_process = None;
                    break
                else:
                    last_run_process = process
                    break
         
            elif process.remaining_time <= quantum:
                if process != last_run_process:
                    context_switches += 1
                time_executed = process.execute(quantum)
                if not process.first_accessed:
                    process.first_time = time
                    process.first_accessed = True
                process.completion_time = time + time_executed
                process.turnaround_time = process.completion_time - process.arrival_time
                completed_processes.append(process)
                ready_queue.pop(process_index)
                last_run_process = None
                break
            else:
                processes_to_move_to_back.append(process)

        # append uncompleted processes to the ready queue
        for process in processes_to_move_to_back:
            ready_queue.remove(process)
        for process in processes_to_move_to_back:
            ready_queue.append(process)

        # increment the time appropriatly
        time += time_executed
    
    return completed_processes, context_switches


#################################################################
#
#     Implementation of Smart Dynamic Round Robin Algorithm
#
#################################################################
def smart_dynamic_round_robin(processes):
    context_switches = 0
    time = 0
    completed_processes = []
    ready_queue = []
    n = len(processes)
    restart_cycle = False
    last_run_process = None;
    added_process = False;

    while len(completed_processes) < n:
        added_process = False
        processes_to_remove = []

        # adds arriving processes to the ready queue
        for process in processes:
            if process.arrival_time <= time:
                ready_queue.append(process)
                processes_to_remove.append(process)
                added_process = True
        for process in processes_to_remove:
            processes.remove(process)
            first_process = ready_queue[0]
            count = 0

        # if no processes are in the ready queue, increment the time and continue
        if not ready_queue:
            time += 1
            continue

        # sort the processes and dynamically calculate the time quantum
        ready_queue = sorted(ready_queue, key=lambda process: process.remaining_time)
        first_process = ready_queue[0]
        differences = [ready_queue[i+1].remaining_time - ready_queue[i].remaining_time for i in range(len(ready_queue)-1)]
        if len(differences) > 0:
            STQ = round(sum(differences) / len(differences))
            Delta = STQ // 2
            if STQ == 0:
                STQ += 1

        # Execute each process in the ready queue for the quantum time slice
        process_index = 0
        actual_index = 0
        number_of_processes = len(ready_queue)
        while process_index < number_of_processes:
            process = ready_queue[actual_index]
            if (len(ready_queue) == 1) or (process.remaining_time <= (STQ + Delta)):
                quantum = process.remaining_time
                time_executed = process.execute(quantum)
                if not process.first_accessed:
                    process.first_time = time
                    process.first_accessed = True
                if process != last_run_process:
                    context_switches += 1
                process.completion_time = time + time_executed
                process.turnaround_time = process.completion_time - process.arrival_time;
                completed_processes.append(process)
                ready_queue.pop(actual_index)
                process_index += 1
                last_run_process = None
            else:
                quantum = STQ
                if process != last_run_process:
                    context_switches += 1
                time_executed = process.execute(quantum)
                if not process.first_accessed:
                    process.first_time = time
                    process.first_accessed = True
                process_index += 1
                actual_index += 1

            # increment the time appropriatly
            time += time_executed
    
    return completed_processes, context_switches


#################################################################
#
#     Implementation of Modified Median Round Robin Algorithm
#
#################################################################
def modified_median_dynamic_round_robin(processes):
    context_switches = 0
    time = 0
    completed_processes = []
    ready_queue = []
    n = len(processes)
    restart_cycle = False
    last_run_process = None;
    added_process = False;

    while len(completed_processes) < n:
        added_process = False
        processes_to_remove = []

        # adds arriving processes to the ready queue
        for process in processes:
            if process.arrival_time <= time:
                ready_queue.append(process)
                processes_to_remove.append(process)
                added_process = True
        for process in processes_to_remove:
            processes.remove(process)
            first_process = ready_queue[0]
            count = 0

        # if no processes are in the ready queue, increment the time and continue
        if not ready_queue:
            time += 1
            continue

        # sort the ready queue and dynamically calculate the time quantum
        ready_queue = sorted(ready_queue, key=lambda process: process.remaining_time)
        remaining_times = [process.remaining_time for process in ready_queue]
        median_BT = median(remaining_times)
        max_BT = ready_queue[-1:][0].remaining_time
        TQ = round(sqrt(median_BT*max_BT))
        threshold = .2
        

        process_index = 0
        actual_index = 0
        # completes a time slice from the next avaliable process
        number_of_processes = len(ready_queue)
        while process_index < number_of_processes:
            process = ready_queue[actual_index]
            if (len(ready_queue) == 1) or (process.remaining_time <= (process.burst_time*threshold)) or (process.remaining_time <= TQ):
                quantum = process.remaining_time
                time_executed = process.execute(quantum)
                if not process.first_accessed:
                    process.first_time = time
                    process.first_accessed = True
                if process != last_run_process:
                    context_switches += 1
                process.completion_time = time + time_executed
                process.turnaround_time = process.completion_time - process.arrival_time;
                completed_processes.append(process)
                ready_queue.pop(actual_index)
                process_index += 1
                last_run_process = None
            else:
                quantum = TQ
                if process != last_run_process:
                    context_switches += 1
                time_executed = process.execute(quantum)
                if not process.first_accessed:
                    process.first_time = time
                    process.first_accessed = True
                process_index += 1
                actual_index += 1

            # increment the time appropriatly
            time += time_executed
    
    return completed_processes, context_switches


#################################################################
#
#     Generates random processes
#
#################################################################
def generate_processes(num_processes, min_burst_time, max_burst_time, min_arrival_time, max_arrival_time):
    processes = []
    for i in range(num_processes):
        name = f"Process {i+1}"
        arrival_time = random.randint(min_arrival_time, max_arrival_time)
        burst_time = random.randint(min_burst_time, max_burst_time)
        process = Process(name, arrival_time, burst_time)
        processes.append(process)
    
    # Append a process that starts at time 0
    process_zero = Process("Process 0", 0, random.randint(min_burst_time, max_burst_time))
    processes.append(process_zero)
    
    return processes

# generate 50 processes with burst times between 0-40 and arrival times between 0-1,000
processes = generate_processes(50, 0, 40, 0, 1000)


quantum = 20

print("15 processes with 20-50ms burst time ariving from 0-1,000ms")
print()
print("Round Robin Algorithm")
temp_processes = copy.deepcopy(processes)
completed_processes, context_switches = round_robin(temp_processes, quantum)
total_turnaround_time = 0
total_waiting_time = 0
total_response_time = 0
for process in completed_processes:
    total_turnaround_time += process.turnaround_time
    total_waiting_time += process.completion_time - process.arrival_time - process.burst_time
    total_response_time += process.first_time - process.arrival_time

average_turnaround_time = total_turnaround_time / len(completed_processes)
average_waiting_time = total_waiting_time / len(completed_processes)
average_response_time = total_response_time / len(completed_processes)
print(f"context switches: {context_switches}     Average turnaround time: {average_turnaround_time}     Average waiting time: {average_waiting_time}     Average response time: {average_response_time}\n")
print()


print("Efficient Dynamic Round Robin Algorithm")
temp_processes = copy.deepcopy(processes)
completed_processes, context_switches = efficient_dynamic_round_robin(temp_processes)
total_turnaround_time = 0
total_waiting_time = 0
total_response_time = 0
for process in completed_processes:
    total_turnaround_time += process.turnaround_time
    total_waiting_time += process.completion_time - process.arrival_time - process.burst_time
    total_response_time += process.first_time - process.arrival_time


average_turnaround_time = total_turnaround_time / len(completed_processes)
average_waiting_time = total_waiting_time / len(completed_processes)
average_response_time = total_response_time / len(completed_processes)
print(f"context switches: {context_switches}     Average turnaround time: {average_turnaround_time}     Average waiting time: {average_waiting_time}     Average response time: {average_response_time}\n")
print()

print("Smart Dynamic Round Robin Algorithm")
temp_processes = copy.deepcopy(processes)
completed_processes, context_switches = smart_dynamic_round_robin(temp_processes)
total_turnaround_time = 0
total_waiting_time = 0
total_response_time = 0
for process in completed_processes:
    total_turnaround_time += process.turnaround_time
    total_waiting_time += process.completion_time - process.arrival_time - process.burst_time
    total_response_time += process.first_time - process.arrival_time

maximum_turnaround_time = max(process.turnaround_time for process in completed_processes)
maximum_wait_time = max((process.completion_time - process.arrival_time - process.burst_time) for process in completed_processes)
average_turnaround_time = total_turnaround_time / len(completed_processes)
average_waiting_time = total_waiting_time / len(completed_processes)
average_response_time = total_response_time / len(completed_processes)
print(f"context switches: {context_switches}     Average turnaround time: {average_turnaround_time}     Average waiting time: {average_waiting_time}     Average response time: {average_response_time}\n")
print()


print("Modified Median Dynamic Round Robin")
temp_processes = copy.deepcopy(processes)
completed_processes, context_switches = modified_median_dynamic_round_robin(temp_processes)
total_turnaround_time = 0
total_waiting_time = 0
total_response_time = 0
for process in completed_processes:
    total_turnaround_time += process.turnaround_time
    total_waiting_time += process.completion_time - process.arrival_time - process.burst_time
    total_response_time += process.first_time - process.arrival_time

maximum_turnaround_time = max(process.turnaround_time for process in completed_processes)
maximum_wait_time = max((process.completion_time - process.arrival_time - process.burst_time) for process in completed_processes)
average_turnaround_time = total_turnaround_time / len(completed_processes)
average_waiting_time = total_waiting_time / len(completed_processes)
average_response_time = total_response_time / len(completed_processes)
print(f"context switches: {context_switches}     Average turnaround time: {average_turnaround_time}     Average waiting time: {average_waiting_time}     Average response time: {average_response_time}\n")
print()

