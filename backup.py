
# OS Project 2: CPU Scheduling
# 10627130 資訊三甲 林冠良
# DEAD LINE -> 6/12

import copy

class Process(): # process data structure
    def __init__(self, ID, CPU_Burst, arrivalTime, priority):
        self.ID = ID
        self.CPU_Burst = CPU_Burst
        self.CPU_Burst_Minus = 0
        self.Arrival_Time = arrivalTime
        self.Priority = priority
        self.Time_Slice = 0
        self.Complete_Time = 0
        self.Waiting_Time = 0
        self.Turnaround_Time = 0
        self.Has_Use_CPU = False

class FCFS(): # done
    def __init__(self, processList):
        self.Process_List = processList
        self.Gantt_Chart = "-"
        self.Running_Process = None
        self.Waiting_Queue = []
        self.Done_List = []
        self.Process_Quantity = len(processList)
        self.Current_Time = 1

    def CheckProcess(self):
        for process in self.Process_List: # search the process list
            if process.Arrival_Time <= self.Current_Time: # if the process have arrived
                self.Waiting_Queue.append(process) # put the process in the waiting queue
        for waiting in self.Waiting_Queue: # search through the waiting queue
            try: # try to remove the past copied process
                print(len(self.Process_List))
                self.Process_List.pop(self.Process_List.index(waiting)) # if yes, pop out
            except: # if can't find
                pass # pass

    def RunProcess(self):
        if not self.Running_Process: # if there's no current running process
            if len(self.Waiting_Queue) > 0: # if there's next process in queue
                self.Running_Process = self.Waiting_Queue.pop(0) # get the first process in waiting queue
            else: return # if there's no more process in queue
        self.Running_Process.CPU_Burst_Minus -= 1 # run the process and minus the cpu bust time
        if self.Running_Process.ID <= 16: self.Gantt_Chart += hex(self.Running_Process.ID)[2:].upper() # add the process ID in hexidecimal into the gantt chart string <=16
        else: self.Gantt_Chart += chr(self.Running_Process.ID+55) # add the process ID in hexidecimal into the gantt chart string >16
        if self.Running_Process.CPU_Burst_Minus == 0: # if the process has complete
            self.Running_Process.Complete_Time = self.Current_Time # assign the complete time
            self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
            self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time
            self.Done_List.append(self.Running_Process) # append the complete process into done list
            self.Running_Process = None # set running process to none

    def Start(self):
        self.Process_List.sort(key=lambda process: (process.Arrival_Time, process.ID)) # sort the process first by arrival time second by process ID
        for process in self.Process_List: process.CPU_Burst_Minus = process.CPU_Burst # add cpu burst minus
        while len(self.Done_List) < self.Process_Quantity: # while length of done list is less than the length of process list
            self.CheckProcess() # check the upcoming process
            self.Current_Time += 1 # current time + 1
            self.RunProcess() # run the current process or dispatch from waiting queue
        self.Done_List.sort(key=lambda process: process.ID) # sort done list by PID

class RR(): # done
    def __init__(self, processList, timeSlice):
        self.Process_List = processList
        self.Time_Slice = timeSlice
        self.Gantt_Chart = "-"
        self.Running_Process = None
        self.Waiting_Queue = []
        self.Done_List = []
        self.Process_Quantity = len(processList)
        self.Current_Time = 1

    def CheckProcess(self):
        for process in self.Process_List: # search the process list
            if process.Arrival_Time <= self.Current_Time: # if the process have arrived
                self.Waiting_Queue.append(process) # put the process in the waiting queue
        for waiting in self.Waiting_Queue: # search through the waiting queue
            try: # try to remove the past copied process
                self.Process_List.pop(self.Process_List.index(waiting)) # if yes, pop out
            except: pass # if can't find
        if self.Running_Process and self.Running_Process.Time_Slice == 0:
            self.Running_Process.Time_Slice = self.Time_Slice # reset the time slice
            self.Waiting_Queue.append(self.Running_Process) # put the process back to the waiting queue
            self.Running_Process = None # set running process to none

    def RunProcess(self):
        if not self.Running_Process: # if there's no current running process
            if len(self.Waiting_Queue) > 0: # if there's next process in queue
                self.Running_Process = self.Waiting_Queue.pop(0) # get the first process in waiting queue
            else: return # if there's no more process in queue
        self.Running_Process.CPU_Burst_Minus -= 1 # run the process and minus the cpu burst time
        self.Running_Process.Time_Slice -= 1 # minus the time slice by one
        if self.Running_Process.ID <= 16: self.Gantt_Chart += hex(self.Running_Process.ID)[2:].upper() # add the process ID in hexidecimal into the gantt chart string <=16
        else: self.Gantt_Chart += chr(self.Running_Process.ID+55) # add the process ID in hexidecimal into the gantt chart string >16
        if self.Running_Process.Time_Slice == 0: # if the current running process has run out of time slice
            if self.Running_Process.CPU_Burst_Minus == 0: # if the process has complete
                self.Running_Process.Complete_Time = self.Current_Time # assign the complete time
                self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
                self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time
                self.Done_List.append(self.Running_Process) # append the complete process into done list
                self.Running_Process = None # set running process to none
                return # return
            return # else return
        if self.Running_Process.CPU_Burst_Minus == 0: # if the process has complete
            self.Running_Process.Complete_Time = self.Current_Time # assign the complete time
            self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
            self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time
            self.Done_List.append(self.Running_Process) # append the complete process into done list
            self.Running_Process = None # set running process to none

    def Start(self):
        self.Process_List.sort(key=lambda process: (process.Arrival_Time, process.ID)) # sort the process first by arrival time second by process ID
        for process in self.Process_List: process.CPU_Burst_Minus = process.CPU_Burst # add cpu burst minus
        while len(self.Done_List) < self.Process_Quantity: # while length of done list is less than the length of process list
            self.CheckProcess() # check the upcoming process
            self.Current_Time += 1 # current time + 1
            self.RunProcess() # run the current process or dispatch from waiting queue
        self.Done_List.sort(key=lambda process: process.ID) # sort done list by PID

class PSJF(): # done
    def __init__(self, processList):
        self.Process_List = processList
        self.Gantt_Chart = "-"
        self.Running_Process = None
        self.Waiting_Queue = []
        self.Done_List = []
        self.Process_Quantity = len(processList)
        self.Current_Time = 1

    def CheckProcess(self):
        for process in self.Process_List: # search the process list
            if process.Arrival_Time <= self.Current_Time: # if the process have arrived
                if self.Running_Process: # if there's a current running process
                    if process.CPU_Burst_Minus < self.Running_Process.CPU_Burst_Minus: # if the upcoming process cpu burst is smaller or equal to the current running process
                        self.Waiting_Queue.append(self.Running_Process) # append the current running process
                        self.Running_Process = process # snatched the current process
                    else: # if the upcoming process cpu burst is greater to the current running process
                        self.Waiting_Queue.append(process) # put the process in the waiting queue
                else: # no current running process
                    self.Waiting_Queue.append(process) # put the process in the waiting queue
        try: # try
            self.Process_List.pop(self.Process_List.index(self.Running_Process)) # remove the unpoped process due to the snatching
        except: pass # pass
        for waiting in self.Waiting_Queue: # search through the waiting queue
            try: # try to remove the past copied process
                self.Process_List.pop(self.Process_List.index(waiting)) # if yes, pop out
            except: pass # pass

    def RunProcess(self):
        if not self.Running_Process: # if there's no current running process
            if len(self.Waiting_Queue) > 0: # if there's next process in queue
                self.Running_Process = self.Waiting_Queue.pop(0) # get the first process in waiting queue
            else: # if there's no more process in queue
                return # return
        self.Running_Process.CPU_Burst_Minus -= 1 # run the process and minus the cpu bust time
        self.Running_Process.Has_Use_CPU = True
        if self.Running_Process.ID <= 16: self.Gantt_Chart += hex(self.Running_Process.ID)[2:].upper() # add the process ID in hexidecimal into the gantt chart string <=16
        else: self.Gantt_Chart += chr(self.Running_Process.ID+55) # add the process ID in hexidecimal into the gantt chart string >16
        if self.Running_Process.CPU_Burst_Minus == 0: # if the process has complete
            self.Running_Process.Complete_Time = self.Current_Time # assign the complete time
            self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
            self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time
            self.Done_List.append(self.Running_Process) # append the complete process into done list
            self.Running_Process = None # set running process to none

    def Start(self):
        self.Process_List.sort(key=lambda process: (process.Arrival_Time, process.CPU_Burst, process.ID)) # sort the process first by cpu burst second by arrival time third by PID
        for process in self.Process_List: process.CPU_Burst_Minus = process.CPU_Burst # add cpu burst minus
        while len(self.Done_List) < self.Process_Quantity: # while length of done list is less than the length of process list
            self.CheckProcess() # check the upcoming process
            self.Waiting_Queue.sort(key=lambda process: (process.CPU_Burst_Minus, process.Has_Use_CPU, process.Arrival_Time, process.ID)) # reorder the waiting queue
            self.Current_Time += 1 # current time + 1
            self.RunProcess() # run the current process or dispatch from waiting queue
        self.Done_List.sort(key=lambda process: process.ID) # sort done list by PID

class NPSJF(): # done
    def __init__(self, processList):
        self.Process_List = processList
        self.Gantt_Chart = "-"
        self.Running_Process = None
        self.Waiting_Queue = []
        self.Done_List = []
        self.Process_Quantity = len(processList)
        self.Current_Time = 1

    def CheckProcess(self):
        for process in self.Process_List: # search the process list
            if process.Arrival_Time <= self.Current_Time: # if the process have arrived
                self.Waiting_Queue.append(process) # put the process in the waiting queue
        for waiting in self.Waiting_Queue: # search through the waiting queue
            try: # try to remove the past copied process
                self.Process_List.pop(self.Process_List.index(waiting)) # if yes, pop out
            except: # if can't find
                pass # pass

    def RunProcess(self):
        if not self.Running_Process: # if there's no current running process
            if len(self.Waiting_Queue) > 0: # if there's next process in queue
                self.Running_Process = self.Waiting_Queue.pop(0) # get the first process in waiting queue
            else: return # if there's no more process in queue
        self.Running_Process.CPU_Burst_Minus -= 1 # run the process and minus the cpu bust time
        if self.Running_Process.ID <= 16: self.Gantt_Chart += hex(self.Running_Process.ID)[2:].upper() # add the process ID in hexidecimal into the gantt chart string <=16
        else: self.Gantt_Chart += chr(self.Running_Process.ID+55) # add the process ID in hexidecimal into the gantt chart string >16
        if self.Running_Process.CPU_Burst_Minus == 0: # if the process has complete
            self.Running_Process.Complete_Time = self.Current_Time # assign the complete time
            self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
            self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time
            self.Done_List.append(self.Running_Process) # append the complete process into done list
            self.Running_Process = None # set running process to none

    def Start(self):
        self.Process_List.sort(key=lambda process: (process.Arrival_Time, process.CPU_Burst, process.ID)) # sort the process first by cpu burst second by arrival time third by PID
        for process in self.Process_List: process.CPU_Burst_Minus = process.CPU_Burst # add cpu burst minus
        while len(self.Done_List) < self.Process_Quantity: # while length of done list is less than the length of process list
            self.CheckProcess() # check the upcoming process
            self.Waiting_Queue.sort(key=lambda process: (process.CPU_Burst, process.Arrival_Time, process.ID)) # reorder the waiting queue
            self.Current_Time += 1 # current time + 1
            self.RunProcess() # run the current process or dispatch from waiting queue
        self.Done_List.sort(key=lambda process: process.ID) # sort done list by PID

class PP(): # done
    def __init__(self, processList):
        self.Process_List = processList
        self.Gantt_Chart = "-"
        self.Running_Process = None
        self.Waiting_Queue = []
        self.Done_List = []
        self.Process_Quantity = len(processList)
        self.Current_Time = 1

    def CheckProcess(self):
        for process in self.Process_List: # search the process list
            if process.Arrival_Time <= self.Current_Time: # if the process have arrived
                if self.Running_Process: # if there's a current running process
                    if process.Priority < self.Running_Process.Priority: # if the upcoming process cpu burst is smaller or equal to the current running process
                        self.Waiting_Queue.append(self.Running_Process) # append the current running process
                        self.Running_Process = process # snatched the current process
                    else: # if the upcoming process cpu burst is greater to the current running process
                        self.Waiting_Queue.append(process) # put the process in the waiting queue
                else: # no current running process
                    self.Waiting_Queue.append(process) # put the process in the waiting queue
        try: # try
            self.Process_List.pop(self.Process_List.index(self.Running_Process)) # remove the unpoped process due to the snatching
        except: pass # pass
        for waiting in self.Waiting_Queue: # search through the waiting queue
            try: # try to remove the past copied process
                self.Process_List.pop(self.Process_List.index(waiting)) # if yes, pop out
            except: pass # pass

    def RunProcess(self):
        if not self.Running_Process: # if there's no current running process
            if len(self.Waiting_Queue) > 0: # if there's next process in queue
                self.Running_Process = self.Waiting_Queue.pop(0) # get the first process in waiting queue
            else: # if there's no more process in queue
                return # return
        self.Running_Process.CPU_Burst_Minus -= 1 # run the process and minus the cpu bust time
        self.Running_Process.Has_Use_CPU = True # set this process has used CPU
        if self.Running_Process.ID <= 16: self.Gantt_Chart += hex(self.Running_Process.ID)[2:].upper() # add the process ID in hexidecimal into the gantt chart string <=16
        else: self.Gantt_Chart += chr(self.Running_Process.ID+55) # add the process ID in hexidecimal into the gantt chart string >16
        if self.Running_Process.CPU_Burst_Minus == 0: # if the process has complete
            self.Running_Process.Complete_Time = self.Current_Time # assign the complete time
            self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time # calculate the turnaround time
            self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst # calculate the waiting time
            self.Done_List.append(self.Running_Process) # append the complete process into done list
            self.Running_Process = None # set running process to none

    def Start(self):
        self.Process_List.sort(key=lambda process: (process.Arrival_Time, process.Priority, process.ID)) # sort the process first by priority second by arrival time third by PID
        for process in self.Process_List: process.CPU_Burst_Minus = process.CPU_Burst # add cpu burst minus
        while len(self.Done_List) < self.Process_Quantity: # while length of done list is less than the length of process list
            self.CheckProcess() # check the upcoming process
            self.Waiting_Queue.sort(key=lambda process: (process.Priority, process.Has_Use_CPU, process.Arrival_Time, process.ID)) # reorder the waiting queue
            self.Current_Time += 1 # current time + 1
            self.RunProcess() # run the current process or dispatch from waiting queue
        self.Done_List.sort(key=lambda process: process.ID) # sort done list by PID

def ReadProcess(input, processList): # read process from imput
    input.readline() # read the labels
    tempArray = input.readline().split() # split every variables
    while tempArray != []: # while temp array is empty
        singleProcess = Process(int(tempArray[0]), int(tempArray[1]), int(tempArray[2]), int(tempArray[3])) # assign the four values
        processList.append(singleProcess) # append this process to process list
        tempArray = input.readline().split() # read next process

def PrintResult(simulate, inputFile): # print result for only one method
    output = open(inputFile.name+"_output.txt", 'w') # open file
    output.write("==Gantt_Ch==\n")
    output.write(simulate.Gantt_Chart)
    output.write("\n============\n\n") # print labels
    output.write("Waiting Time\nID      Time\n============\n") # print labels
    for index in range(len(simulate.Done_List)): # print waiting time
        output.write(str(simulate.Done_List[index].ID))
        output.write("\t\t")
        output.write(str(simulate.Done_List[index].Waiting_Time))
        output.write("\n")
    output.write("============\n\nTurnaround Time\nID      Time\n============\n") # print labels
    for index in range(len(simulate.Done_List)): # print waiting time
        output.write(str(simulate.Done_List[index].ID))
        output.write("\t\t")
        output.write(str(simulate.Done_List[index].Turnaround_Time))
        output.write("\n")
    output.write("============") # print labels

def PrintAllResult(inputFile, FCFS_Simulate, RR_Simulate, PSJF_Simulate, NPSJF_Simulate, PP_Simulate): # print every result
    output = open(inputFile.name+"_output.txt", 'w') # open output file
    output.write("==    FCFS==\n")
    output.write(FCFS_Simulate.Gantt_Chart)
    output.write("\n")
    output.write("==      RR==\n")
    output.write(RR_Simulate.Gantt_Chart)
    output.write("\n")
    output.write("==    PSJF==\n")
    output.write(PSJF_Simulate.Gantt_Chart)
    output.write("\n")
    output.write("==Non-PSJF==\n")
    output.write(NPSJF_Simulate.Gantt_Chart)
    output.write("\n")
    output.write("==      PP==\n")
    output.write(PP_Simulate.Gantt_Chart)
    output.write("\n")
    output.write("===========================================================\n\n") # print labels
    output.write("Waiting Time\nID      FCFS    RR      PSJF    NPSJF   Priority\n===========================================================\n") # print labels
    for index in range(len(FCFS_Simulate.Done_List)): # print waiting time
        output.write(str(FCFS_Simulate.Done_List[index].ID))
        output.write("\t\t")
        output.write(str(FCFS_Simulate.Done_List[index].Waiting_Time))
        output.write("\t\t")
        output.write(str(RR_Simulate.Done_List[index].Waiting_Time))
        output.write("\t\t")
        output.write(str(PSJF_Simulate.Done_List[index].Waiting_Time))
        output.write("\t\t")
        output.write(str(NPSJF_Simulate.Done_List[index].Waiting_Time))
        output.write("\t\t")
        output.write(str(PP_Simulate.Done_List[index].Waiting_Time))
        output.write("\n")
    output.write("===========================================================\n\nTurnaround Time\nID      FCFS    RR      PSJF    NPSJF   Priority\n===========================================================\n") # print labels
    for index in range(len(FCFS_Simulate.Done_List)): # print turnaround time
        output.write(str(FCFS_Simulate.Done_List[index].ID))
        output.write("\t\t")
        output.write(str(FCFS_Simulate.Done_List[index].Turnaround_Time))
        output.write("\t\t")
        output.write(str(RR_Simulate.Done_List[index].Turnaround_Time))
        output.write("\t\t")
        output.write(str(PSJF_Simulate.Done_List[index].Turnaround_Time))
        output.write("\t\t")
        output.write(str(NPSJF_Simulate.Done_List[index].Turnaround_Time))
        output.write("\t\t")
        output.write(str(PP_Simulate.Done_List[index].Turnaround_Time))
        output.write("\n")
    output.write("===========================================================") # print labels

def main():
    #inputFile = open(input("Please enter the file name you want to simulate the scheduling...\n"), 'r') # open file
    inputFile = open("input.txt", 'r')
    method, timeSlice = [int(token) for token in inputFile.readline().split()] # read method and time slice
    processList = [] # create an empty process list
    ReadProcess(inputFile, processList) # read the processes
    for process in processList: process.Time_Slice = timeSlice # add time slice to eash process
    if method == 1: # FCFS (First Come First Serve)
        FCFS_Process_List = copy.deepcopy(processList) # create a FCFS process list
        FCFS_Simulate = FCFS(FCFS_Process_List) # create a new FCFS class
        FCFS_Simulate.Start() # start the FCFS class
        PrintResult(FCFS_Simulate, inputFile) # print results
    elif method == 2: # RR (Round Robin)
        RR_Process_List = copy.deepcopy(processList) # create a RR process list
        RR_Simulate = RR(RR_Process_List, timeSlice) # create a new RR class
        RR_Simulate.Start() # start the RR class
        PrintResult(RR_Simulate, inputFile) # print results
    elif method == 3: # PSJF (Preemptive Shortest Job First)
        PSJF_Process_List = copy.deepcopy(processList) # create a PSJF process list
        PSJF_Simulate = PSJF(PSJF_Process_List) # create a new PSJF class
        PSJF_Simulate.Start() # start the PSJF class
        PrintResult(PSJF_Simulate, inputFile) # print results
    elif method == 4: # NSJF (Non-preemptive Shortest Job First)
        NPSJF_Process_List = copy.deepcopy(processList) # create a NSJF process list
        NPSJF_Simulate = NPSJF(NPSJF_Process_List) # create a new NSJF class
        NPSJF_Simulate.Start() # start the NJSF class
        PrintResult(NPSJF_Simulate, inputFile) # print results
    elif method == 5: # PP (Preemptive Priority)
        PP_Process_List = copy.deepcopy(processList) # create a PP process list
        PP_Simulate = PP(PP_Process_List)     # create a new PP class
        PP_Simulate.Start() # start the PP class
        PrintResult(PP_Simulate, inputFile) # print results
    elif method == 6: # ALL
        FCFS_Process_List  = copy.deepcopy(processList) # create a FCFS process list
        RR_Process_List    = copy.deepcopy(processList) # create a RR process list
        PSJF_Process_List  = copy.deepcopy(processList) # create a PSJF process list
        NPSJF_Process_List = copy.deepcopy(processList) # create a NSJF process list
        PP_Process_List    = copy.deepcopy(processList) # create a PP process list
        FCFS_Simulate  = FCFS(FCFS_Process_List)        # create a new FCFS class
        RR_Simulate    = RR(RR_Process_List, timeSlice) # create a new RR class
        PSJF_Simulate  = PSJF(PSJF_Process_List)        # create a new PSJF class
        NPSJF_Simulate = NPSJF(NPSJF_Process_List)      # create a new NSJF class
        PP_Simulate    = PP(PP_Process_List)            # create a new PP class
        FCFS_Simulate.Start()  # start the FCFS class
        RR_Simulate.Start()    # start the FCFS class
        PSJF_Simulate.Start()  # start the PSJF class
        NPSJF_Simulate.Start() # start the NJSF class
        PP_Simulate.Start()    # start the PP class
        PrintAllResult(inputFile, FCFS_Simulate, RR_Simulate, PSJF_Simulate, NPSJF_Simulate, PP_Simulate) # print all results

if __name__ == "__main__":
    main()