import math

# Process class to represent each process
class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = None
        self.turnaround_time = None
    
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



# Round-robin scheduling algorithm
def round_robin(processes, quantum):
    context_switches = 0
    time = 0
    completed_processes = []
    ready_queue = []
    n = len(processes)
    last_run_process = None;
    
    while len(completed_processes) < n:
        # Add arriving processes to the ready queue
        for i in range(n):
            if processes[i].arrival_time == time:
                ready_queue.append(processes[i])
        if last_run_process:
            ready_queue.append(last_run_process)
        
        # Print the current status of the ready queue
        print(f"Time {time}: [", end="")
        for process in ready_queue:
            print(process.name, end=", ")
        print("]")
        
        # Execute each process in the ready queue for the quantum time slice
        while ready_queue:
            process = ready_queue.pop(0)
            time_executed = process.execute(quantum)
            if process != last_run_process:
                context_switches += 1
            if process.is_completed():
                process.completion_time = time + time_executed
                process.turnaround_time = process.completion_time - process.arrival_time;
                completed_processes.append(process)
                last_run_process = None;
                break
            else:
                last_run_process = process
                break
        
        time += quantum
    
    return completed_processes, context_switches


# Round-robin scheduling algorithm
def efficient_dynamic_round_robin():
    processes = [
    Process("P1", 0, 45),
    Process("P2", 5, 90),
    Process("P3", 8, 70),
    Process("P4", 15, 38),
    Process("P5", 20, 55)]
    context_switches = 0
    time = 0
    completed_processes = []
    ready_queue = []
    n = len(processes)
    last_run_process = None;
    added_process = False;

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

             
        # set the time quantum
        BTmax = 0
        if added_process:
            for process in ready_queue:
                if process.burst_time > BTmax:
                    BTmax = process.burst_time
                    quantum = BTmax * 0.8
        elif all(process.burst_time > quantum for process in ready_queue):
                    quantum = max(process.burst_time for process in ready_queue)
        
                            # Print the current status of the ready queue
        print(f"Time {time}: [", end="")
        for process in ready_queue:
            print(process.name, end=", ")
        print("]")
        processes_to_move_to_back = []
        # Execute each process in the ready queue for the quantum time slice
        for process_index, process in enumerate(ready_queue):
            if len(ready_queue) == 1:
                if process != last_run_process:
                    context_switches += 1
                time_executed = process.execute(quantum)
                if process.is_completed():
                    process.completion_time = time + time_executed
                    process.turnaround_time = process.completion_time - process.arrival_time;
                    completed_processes.append(process)
                    last_run_process = None;
                    break
                else:
                    last_run_process = process
                    break
        
            elif process.burst_time <= quantum:
                if process != last_run_process:
                    context_switches += 1
                time_executed = process.execute(quantum)
                process.completion_time = time + time_executed
                process.turnaround_time = process.completion_time - process.arrival_time
                completed_processes.append(process)
                ready_queue.pop(process_index)
                last_run_process = None
                break
            else:
                processes_to_move_to_back.append(process)

        for process in processes_to_move_to_back:
            ready_queue.remove(process)
        for process in processes_to_move_to_back:
            ready_queue.append(process)


        time += time_executed
    
    return completed_processes, context_switches


def smart_dynamic_round_robin():
    processes = [
    Process("P0", 0, 8),
    Process("P1", 2, 6),
    Process("P2", 7, 11),
    Process("P3", 0, 5)]
    context_switches = 0
    time = 0
    completed_processes = []
    ready_queue = []
    n = len(processes)
    last_run_process = None;
    added_process = False;

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

        if added_process:
            # sort the processes
            ready_queue = sorted(ready_queue, key=lambda process: process.remaining_time)
            # calculate the differences between adjacent burst times
            differences = [ready_queue[i+1].remaining_time - ready_queue[i].remaining_time for i in range(len(ready_queue)-1)]
            # calculate the average of the differences
            STQ = sum(differences) / len(differences)
            Delta = STQ//2
            STQ = STQ // 1
        
        # Print the current status of the ready queue
        print(f"Time {time}: [", end="")
        for process in ready_queue:
            print(process.name, end=", ")
        print("]")
        processes_to_move_to_back = []



        for process_index, process in enumerate(ready_queue):
            if (process.remaining_time <= (STQ + Delta) or (len(ready_queue) == 1)):
                quantum = process.remaining_time
                time_executed = process.execute(quantum)
                if process != last_run_process:
                    context_switches += 1
                process.completion_time = time + time_executed
                process.turnaround_time = process.completion_time - process.arrival_time;
                completed_processes.append(process)
                last_run_process = None;
            else:
                quantum = STQ
                if process != last_run_process:
                    context_switches += 1
                time_executed = process.execute(quantum)
                if process.is_completed():
                    process.completion_time = time + time_executed
                    process.turnaround_time = process.completion_time - process.arrival_time;
                    completed_processes.append(process)
                    last_run_process = None;
                else:
                    last_run_process = process
        
            time += quantum

        for process in completed_processes:
            if process in ready_queue:
                ready_queue.remove(process)

    
    return completed_processes, context_switches

# Example usage
processes = [
    Process("A", 0, 3),
    Process("B", 2, 6),
    Process("C", 4, 4),
    Process("D", 6, 5),
    Process("E", 8, 2)]
quantum = 1

#completed_processes, context_switches = efficient_dynamic_round_robin()
completed_processes, context_switches = smart_dynamic_round_robin()
#completed_processes, context_switches = round_robin(processes, quantum)

# Print the completion order and turnaround time for each process
for process in completed_processes:
    print(f"{process.name}: Arrival time = {process.arrival_time}, Burst time = {process.burst_time}, Turnaround time = {process.turnaround_time}, Waiting time = {process.completion_time - process.arrival_time - process.burst_time}")

print(f"context switches: {context_switches}")