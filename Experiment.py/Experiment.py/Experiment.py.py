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
                process.completion_time = time
                process.turnaround_time = process.completion_time - process.arrival_time + 1
                completed_processes.append(process)
                last_run_process = None;
                break
            else:
                last_run_process = process
                break
        
        time += quantum
    
    return completed_processes, context_switches


# Example usage
processes = [
    Process("A", 0, 3),
    Process("B", 2, 6),
    Process("C", 4, 4),
    Process("D", 6, 5),
    Process("E", 8, 2)]
quantum = 1

completed_processes, context_switches = round_robin(processes, quantum)

# Print the completion order and turnaround time for each process
for process in processes:
    print(f"{process.name}: Turnaround time = {process.turnaround_time}")

print(f"context switches: {context_switches}")
