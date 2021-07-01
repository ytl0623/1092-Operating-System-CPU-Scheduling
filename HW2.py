import copy

class Process() :
  def __init__( self, id, CPU_burst, arrivalTime, priority ) :
    self.ID = id
    self.CPU_Burst = CPU_burst
    self.Arrival_Time = arrivalTime
    self.Priority = priority

    self.Complete_Time = 0
    self.Waiting_Time = 0
    self.Turnaround_Time = 0

    self.Time_Slice = 0  # RR, PPRR
    self.CPU_Burst_Remaining = 0
    self.Time_Slice_Limit = False  # PPRR
    self.Has_Use_CPU = False  # PPRR
    self.Response_Ratio = 0.0  # HRRN

class FCFS() :
  def __init__( self, processList ) :
    self.Method_Name = "FCFS"
    self.Process_List = processList
    self.Gantt_Chart = ""
    self.Running_Process = None
    self.Waiting_Queue = []
    self.Done_List = []
    self.Process_Quantity = len( processList )
    self.Current_Time = 0

  def CheckProcess( self ) :
    for process in self.Process_List :
      if process.Arrival_Time <= self.Current_Time :
        self.Waiting_Queue.append( process )

    for waiting in self.Waiting_Queue :
      try :  # try to remove the past copied process
        self.Process_List.pop( self.Process_List.index( waiting ) )
      except :
        pass

  def RunProcess( self ) :
    if not self.Running_Process :  # None
      if len( self.Waiting_Queue ) > 0 :
        self.Running_Process = self.Waiting_Queue.pop( 0 )
      else :   # there's no waiting process in queue
        self.Gantt_Chart += "-"
        return

    self.Running_Process.CPU_Burst_Remaining -= 1

    if self.Running_Process.ID <= 16 :
      self.Gantt_Chart += hex( self.Running_Process.ID )[2:].upper()
    else :
      self.Gantt_Chart += chr( self.Running_Process.ID + 55 )

    if self.Running_Process.CPU_Burst_Remaining == 0 :  # process completed
      self.Running_Process.Complete_Time = self.Current_Time
      self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time
      self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst
      self.Done_List.append( self.Running_Process )
      self.Running_Process = None

  def Start ( self ) :
    self.Process_List.sort( key = lambda process : ( process.Arrival_Time, process.ID ) )  # sorted by 1.arrivalTime 2.PID

    for process in self.Process_List :
      process.CPU_Burst_Remaining = process.CPU_Burst

    while len( self.Done_List ) < self.Process_Quantity :
      self.CheckProcess()
      self.Current_Time += 1
      self.RunProcess()

    self.Done_List.sort( key = lambda process : process.ID )

class RR() :
  def __init__( self, processList, timeSlice ) :
    self.Method_Name = "RR"
    self.Process_List = processList
    self.Time_Slice = timeSlice
    self.Gantt_Chart = ""
    self.Running_Process = None
    self.Waiting_Queue = []
    self.Done_List = []
    self.Process_Quantity = len( processList )
    self.Current_Time = 0

  def CheckProcess( self ) :
    for process in self.Process_List :
      if process.Arrival_Time <= self.Current_Time :
          self.Waiting_Queue.append( process )

    for waiting in self.Waiting_Queue :
      try :  # try to remove the past copied process
        self.Process_List.pop( self.Process_List.index( waiting ) )
      except :
        pass

    if self.Running_Process and self.Running_Process.Time_Slice == 0 :  # process not completed but timeout
      self.Running_Process.Time_Slice = self.Time_Slice  # reset
      self.Waiting_Queue.append( self.Running_Process )  # go back go back
      self.Running_Process = None

  def RunProcess( self ) :
    if not self.Running_Process :  # None
      if len( self.Waiting_Queue ) > 0 :
        self.Running_Process = self.Waiting_Queue.pop( 0 )
      else :   # there's no waiting process in queue
        self.Gantt_Chart += "-"
        return

    self.Running_Process.CPU_Burst_Remaining -= 1
    self.Running_Process.Time_Slice -= 1

    if self.Running_Process.ID <= 16 :
      self.Gantt_Chart += hex( self.Running_Process.ID )[2:].upper()
    else :
      self.Gantt_Chart += chr( self.Running_Process.ID + 55 )

    if self.Running_Process.Time_Slice == 0 :
      if self.Running_Process.CPU_Burst_Remaining == 0 :  # process completed
        self.Running_Process.Complete_Time = self.Current_Time
        self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time
        self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst
        self.Done_List.append( self.Running_Process )
        self.Running_Process = None
        return
      else :  # process not completed
        return  # go back go back
    elif self.Running_Process.CPU_Burst_Remaining == 0 :  # but timeSlice > 0
      self.Running_Process.Complete_Time = self.Current_Time
      self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time
      self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst
      self.Done_List.append( self.Running_Process )
      self.Running_Process = None

  def Start( self ) :
    self.Process_List.sort( key = lambda process : ( process.Arrival_Time, process.ID ) )  # sorted by 1.arrivalTime 2.PID

    for process in self.Process_List :
      process.CPU_Burst_Remaining = process.CPU_Burst

    while len( self.Done_List ) < self.Process_Quantity :
      self.CheckProcess()
      self.Current_Time += 1
      self.RunProcess()

    self.Done_List.sort( key = lambda process : process.ID )

class SRTF() :
  def __init__( self, processList ) :
    self.Method_Name = "SRTF"
    self.Process_List = processList
    self.Gantt_Chart = ""
    self.Running_Process = None
    self.Waiting_Queue = []
    self.Done_List = []
    self.Process_Quantity = len( processList )
    self.Current_Time = 0

  def CheckProcess( self ) :
    for process in self.Process_List :
      if process.Arrival_Time <= self.Current_Time :
        if self.Running_Process :
          if process.CPU_Burst_Remaining < self.Running_Process.CPU_Burst_Remaining :  # CPU_Burst_Remaining Preemptive
            self.Waiting_Queue.append( self.Running_Process )  # go back go back
            self.Running_Process = process
          elif process.CPU_Burst_Remaining == self.Running_Process.CPU_Burst_Remaining :
            if ( process.Arrival_Time < self.Running_Process.Arrival_Time ) :  # Arrival_Time Preemptive
              self.Waiting_Queue.append( self.Running_Process )  # go back go back
              self.Running_Process = process
            elif ( process.Arrival_Time == self.Running_Process.Arrival_Time ) :
              if ( process.ID < self.Running_Process.ID ) :  # PID Preemptive
                self.Waiting_Queue.append( self.Running_Process )  # go back go back
                self.Running_Process = process
              else :
                self.Waiting_Queue.append( process )
            else :
              self.Waiting_Queue.append( process )
          else :
            self.Waiting_Queue.append( process )
        else :
          self.Waiting_Queue.append( process )

    try :  # try to remove the unpoped process due to the snatching, cuz Preemptive occured.
      self.Process_List.pop( self.Process_List.index( self.Running_Process ) )
    except :
      pass

    for waiting in self.Waiting_Queue :
      try : # try to remove the past copied process
        self.Process_List.pop( self.Process_List.index( waiting ) )
      except :
        pass

  def RunProcess( self ) :
    if not self.Running_Process :
      if len( self.Waiting_Queue ) > 0 :
        self.Running_Process = self.Waiting_Queue.pop( 0 )
      else :
        self.Gantt_Chart += "-"
        return

    self.Running_Process.CPU_Burst_Remaining -= 1

    if self.Running_Process.ID <= 16 :
      self.Gantt_Chart += hex( self.Running_Process.ID)[2:].upper()
    else :
      self.Gantt_Chart += chr( self.Running_Process.ID + 55 )

    if self.Running_Process.CPU_Burst_Remaining == 0 :
      self.Running_Process.Complete_Time = self.Current_Time
      self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time
      self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst
      self.Done_List.append( self.Running_Process )
      self.Running_Process = None

  def Start( self ) :
    self.Process_List.sort( key = lambda process : ( process.Arrival_Time, process.CPU_Burst, process.ID ) )  # sorted by 1.cpu burst 2.arrivalTime 3.PID

    for process in self.Process_List :
      process.CPU_Burst_Remaining = process.CPU_Burst

    while len( self.Done_List ) < self.Process_Quantity :
      self.CheckProcess()
      self.Waiting_Queue.sort( key = lambda process : ( process.CPU_Burst_Remaining, process.Arrival_Time, process.ID ) )  # cuz SRTF changed by CPU_Burst_Remaining, so u need to sorted Waiting_Queue again.
      self.Current_Time += 1
      self.RunProcess()

    self.Done_List.sort( key = lambda process : process.ID )

class PPRR() :
  def __init__( self, processList, timeSlice ) :
    self.Method_Name = "PPRR"
    self.Process_List = processList
    self.Time_Slice = timeSlice
    self.Gantt_Chart = ""
    self.Running_Process = None
    self.Waiting_Queue = []
    self.Done_List = []
    self.Process_Quantity = len( processList )
    self.Current_Time = 0
    self.Same_Priority_Queue = []

  def CheckProcess( self ) :
    self.Waiting_Queue.sort( key = lambda process : ( process.Priority, process.Has_Use_CPU, process.Arrival_Time, process.ID ) )

    if self.Running_Process :   # before be preemptived, we need to do this first
      for waiting in self.Waiting_Queue :
        if waiting.Priority == self.Running_Process.Priority :
          self.Same_Priority_Queue.append( waiting )

      if self.Same_Priority_Queue :
        for waiting in self.Same_Priority_Queue :
          try :  # try to remove the past copied process
            self.Waiting_Queue.pop( self.Waiting_Queue.index( waiting ) )
          except :
            pass

    for process in self.Process_List :
      if process.Arrival_Time <= self.Current_Time :
        if self.Running_Process :
          if process.Priority < self.Running_Process.Priority :  # Priority Preemptive
            self.Running_Process.Time_Slice = self.Time_Slice  # reset
            self.Waiting_Queue.append( self.Running_Process )
            self.Running_Process = process
          elif process.Priority == self.Running_Process.Priority :
            if process.Arrival_Time < self.Running_Process.Arrival_Time :  # Arrival_Time Preemptive
              self.Running_Process.Time_Slice = self.Time_Slice  # reset
              self.Waiting_Queue.append( self.Running_Process )  # go back go back
              self.Running_Process = process
            elif process.Arrival_Time == self.Running_Process.Arrival_Time :
              if process.ID < self.Running_Process.ID :  # PID Preemptive
                self.Running_Process.Time_Slice = self.Time_Slice  # reset
                self.Waiting_Queue.append( self.Running_Process )  # go back go back
                self.Running_Process = process
              else :
                self.Waiting_Queue.append( process )
            else :
              self.Waiting_Queue.append( process )
          else :
            self.Waiting_Queue.append ( process )
        else :
          self.Waiting_Queue.append( process )

    try :
      self.Process_List.pop( self.Process_List.index( self.Running_Process ) )  # remove the unpoped process due to the snatching
    except :
      pass

    for waiting in self.Waiting_Queue :
      try :  # try to remove the past copied process
        self.Process_List.pop( self.Process_List.index( waiting ) )
      except :
        pass

    if self.Running_Process :
      for waiting in self.Waiting_Queue :
        self.Running_Process.Time_Slice_Limit = False
        if waiting.Priority == self.Running_Process.Priority :
          self.Running_Process.Time_Slice_Limit = True
          break

      for priority in self.Same_Priority_Queue :
        if priority.Priority == self.Running_Process.Priority :
          self.Running_Process.Time_Slice_Limit = True
          break

    if self.Running_Process and self.Running_Process.Time_Slice_Limit and self.Running_Process.Time_Slice == 0 :  # process not completed but timeout
      self.Running_Process.Time_Slice = self.Time_Slice  # reset
      self.Waiting_Queue.append( self.Running_Process )  # go back go back
      self.Running_Process = None

  def RunProcess( self ) :
    if not self.Running_Process :
      if len( self.Same_Priority_Queue ) > 0 :
        self.Running_Process = self.Same_Priority_Queue.pop( 0 )
      elif len( self.Waiting_Queue ) > 0 :
        self.Running_Process =  self.Waiting_Queue.pop( 0 )
      else :
        self.Gantt_Chart += "-"
        return

    self.Running_Process.CPU_Burst_Remaining -= 1
    self.Running_Process.Time_Slice -= 1
    self.Running_Process.Has_Use_CPU = True

    if self.Running_Process.ID <= 16 :
      self.Gantt_Chart += hex( self.Running_Process.ID )[2:].upper()
    else :
      self.Gantt_Chart += chr( self.Running_Process.ID + 55 )

    if self.Running_Process.CPU_Burst_Remaining == 0 :
      self.Running_Process.Complete_Time = self.Current_Time
      self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time
      self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst
      self.Done_List.append( self.Running_Process )
      self.Running_Process = None

  def Start( self ) :
    self.Process_List.sort( key = lambda process : ( process.Arrival_Time, process.Priority, process.ID ) )  # sorted by 1.arrivalTime 2.priority 3.PID

    for process in self.Process_List :
      process.CPU_Burst_Remaining = process.CPU_Burst

    while len( self.Done_List ) < self.Process_Quantity :
      self.CheckProcess()
      self.Current_Time += 1
      self.RunProcess()

    self.Done_List.sort( key = lambda process : process.ID )

class HRRN() :
  def __init__( self, processList ) :
    self.Method_Name = "HRRN"
    self.Process_List = processList
    self.Gantt_Chart = ""
    self.Running_Process = None
    self.Waiting_Queue = []
    self.Done_List = []
    self.Process_Quantity = len( processList )
    self.Current_Time = 0

  def CheckProcess( self ) :
    for process in self.Process_List :
      if process.Arrival_Time <= self.Current_Time :
        self.Waiting_Queue.append( process )

    for waiting in self.Waiting_Queue :
      waiting.Response_Ratio = ( self.Current_Time - waiting.Arrival_Time + waiting.CPU_Burst ) /  waiting.CPU_Burst

      try :  # try to remove the past copied process
        self.Process_List.pop( self.Process_List.index( waiting ) )
      except :
        pass

  def RunProcess( self ) :
    if not self.Running_Process :  # None
      if len( self.Waiting_Queue ) > 0 :
        self.Running_Process = self.Waiting_Queue.pop( 0 )
      else :   # there's no waiting process in queue
        self.Gantt_Chart += "-"
        return

    self.Running_Process.CPU_Burst_Remaining -= 1

    if self.Running_Process.ID <= 16 :
      self.Gantt_Chart += hex( self.Running_Process.ID )[2:].upper()
    else :
      self.Gantt_Chart += chr( self.Running_Process.ID + 55 )

    if self.Running_Process.CPU_Burst_Remaining == 0 :  # process completed
      self.Running_Process.Complete_Time = self.Current_Time
      self.Running_Process.Turnaround_Time = self.Running_Process.Complete_Time - self.Running_Process.Arrival_Time
      self.Running_Process.Waiting_Time = self.Running_Process.Turnaround_Time - self.Running_Process.CPU_Burst
      self.Done_List.append( self.Running_Process )
      self.Running_Process = None

  def Start ( self ) :
    self.Process_List.sort( key = lambda process : ( process.Arrival_Time, process.ID ) )  # sorted by 1.arrivalTime 2.PID

    for process in self.Process_List :
      process.CPU_Burst_Remaining = process.CPU_Burst

    while len( self.Done_List ) < self.Process_Quantity :
      self.CheckProcess()
      self.Waiting_Queue.sort( key = lambda process : ( 1 / process.Response_Ratio, process.Arrival_Time, process.ID ) )  # cuz HRRN changed by Response_Ratio, so u need to sorted Waiting_Queue again.
      self.Current_Time += 1
      self.RunProcess()

    self.Done_List.sort( key = lambda process : process.ID )

def ReadProcess( inFile, processList ) :
  inFile.readline()  # title (ID, CPU Burst...)
  temp = inFile.readline().split()

  while temp != [] :
    process = Process( int(temp[0]), int(temp[1]), int(temp[2]), int(temp[3]) )
    processList.append(process)
    temp = inFile.readline().split()

def PrintResult( simulate, inFile ) :
  outFile = open( "out_" + inFile.name, 'w' )

  outFile.write( simulate.Method_Name + "\n" )
  outFile.write( simulate.Gantt_Chart )
  outFile.write( "\n===========================================================\n\n" )

  outFile.write( "waiting\nID\t" + simulate.Method_Name + "\n===========================================================\n")
  for index in range( len( simulate.Done_List ) ) :
    outFile.write( str( simulate.Done_List[index].ID ) )
    outFile.write( "\t" )
    outFile.write( str( simulate.Done_List[index].Waiting_Time ) )
    outFile.write( "\n" )
  outFile.write( "===========================================================\n\n" )

  outFile.write( "Turnaround Time\nID\t" + simulate.Method_Name + "\n===========================================================\n" )
  for index in range( len( simulate.Done_List ) ) :
    outFile.write( str( simulate.Done_List[index].ID ) )
    outFile.write( "\t" )
    outFile.write( str( simulate.Done_List[index].Turnaround_Time ) )
    outFile.write( "\n" )

def PrintAllResult( inFile, FCFS_Simulate, RR_Simulate, SRTF_Simulate, PPRR_Simulate, HRRN_Simulate ) :
  outFile = open( "out_" + inFile.name, 'w' )
  outFile.write( "All\n" )

  outFile.write( "==        " + FCFS_Simulate.Method_Name + "==\n" )
  outFile.write( FCFS_Simulate.Gantt_Chart + "\n" )

  outFile.write( "==          " + RR_Simulate.Method_Name + "==\n" )
  outFile.write( RR_Simulate.Gantt_Chart + "\n" )

  outFile.write( "==        " + SRTF_Simulate.Method_Name + "==\n" )
  outFile.write( SRTF_Simulate.Gantt_Chart + "\n" )

  outFile.write( "==        " + PPRR_Simulate.Method_Name + "==\n" )
  outFile.write( PPRR_Simulate.Gantt_Chart + "\n" )

  outFile.write( "==        " + HRRN_Simulate.Method_Name + "==\n" )
  outFile.write( HRRN_Simulate.Gantt_Chart )
  outFile.write( "\n===========================================================\n\n" )

  outFile.write( "waiting\nID\tFCFS\tRR\tSRTF\tPPRR\tHRRN\n===========================================================\n")
  for index in range( len( FCFS_Simulate.Done_List ) ) :
    outFile.write( str( FCFS_Simulate.Done_List[ index ].ID ) )
    outFile.write( "\t" )
    outFile.write( str( FCFS_Simulate.Done_List[ index ].Waiting_Time ) )
    outFile.write( "\t" )
    outFile.write( str( RR_Simulate.Done_List[ index ].Waiting_Time ) )
    outFile.write( "\t" )
    outFile.write( str( SRTF_Simulate.Done_List[ index ].Waiting_Time ) )
    outFile.write( "\t" )
    outFile.write( str( PPRR_Simulate.Done_List[ index ].Waiting_Time ) )
    outFile.write( "\t" )
    outFile.write( str( HRRN_Simulate.Done_List[ index ].Waiting_Time ) )
    outFile.write( "\n" )
  outFile.write( "===========================================================\n\n" )

  outFile.write( "Turnaround Time\nID\tFCFS\tRR\tSRTF\tPPRR\tHRRN\n===========================================================\n" )
  for index in range( len( FCFS_Simulate.Done_List ) ) :
    outFile.write( str( FCFS_Simulate.Done_List[ index ].ID ) )
    outFile.write( "\t" )
    outFile.write( str( FCFS_Simulate.Done_List[ index ].Turnaround_Time ) )
    outFile.write( "\t" )
    outFile.write( str( RR_Simulate.Done_List[ index ].Turnaround_Time ) )
    outFile.write( "\t" )
    outFile.write( str( SRTF_Simulate.Done_List[ index ].Turnaround_Time ) )
    outFile.write( "\t" )
    outFile.write( str( PPRR_Simulate.Done_List[ index ].Turnaround_Time ) )
    outFile.write( "\t" )
    outFile.write( str( HRRN_Simulate.Done_List[ index ].Turnaround_Time ) )
    outFile.write( "\n" )
  outFile.write( "===========================================================\n\n" )

def main() :
  while 1 :
    inFile = open( input( "Please enter the filename (e.g., input.txt) : " ), 'r' )
    method, timeSlice = [ int( token ) for token in inFile.readline().split() ]

    processList = []
    ReadProcess( inFile, processList )

    for process in processList :
      process.Time_Slice = timeSlice

    if method == 1 :  # FCFS
      FCFS_Process_List = copy.deepcopy( processList )  # import copy
      FCFS_Simulate = FCFS( FCFS_Process_List )
      FCFS_Simulate.Start()
      PrintResult( FCFS_Simulate, inFile )

    elif method == 2 :  # RR
      RR_Process_List = copy.deepcopy( processList )
      RR_Simulate = RR( RR_Process_List, timeSlice )
      RR_Simulate.Start()
      PrintResult( RR_Simulate, inFile )

    elif method == 3 :  # SRTF
      SRTF_Process_List = copy.deepcopy( processList )
      SRTF_Simulate = SRTF( SRTF_Process_List )
      SRTF_Simulate.Start()
      PrintResult( SRTF_Simulate, inFile )

    elif method == 4 :  # PP
      PPRR_Process_List = copy.deepcopy( processList )
      PPRR_Simulate = PPRR( PPRR_Process_List, timeSlice )
      PPRR_Simulate.Start()
      PrintResult( PPRR_Simulate, inFile )

    elif method == 5 : # HRRN
      HRRN_Process_List = copy.deepcopy( processList )
      HRRN_Simulate = HRRN( HRRN_Process_List )
      HRRN_Simulate.Start()
      PrintResult( HRRN_Simulate, inFile )

    elif method == 6 :  # ALL
      FCFS_Process_List = copy.deepcopy( processList )
      FCFS_Simulate = FCFS( FCFS_Process_List )
      FCFS_Simulate.Start()

      RR_Process_List = copy.deepcopy( processList )
      RR_Simulate = RR( RR_Process_List, timeSlice )
      RR_Simulate.Start() # start the RR class

      SRTF_Process_List = copy.deepcopy( processList )
      SRTF_Simulate = SRTF( SRTF_Process_List )
      SRTF_Simulate.Start()

      PPRR_Process_List = copy.deepcopy( processList )
      PPRR_Simulate = PPRR( PPRR_Process_List, timeSlice )
      PPRR_Simulate.Start()

      HRRN_Process_List = copy.deepcopy( processList )
      HRRN_Simulate = HRRN( HRRN_Process_List )
      HRRN_Simulate.Start()

      PrintAllResult( inFile, FCFS_Simulate, RR_Simulate, SRTF_Simulate, PPRR_Simulate, HRRN_Simulate )

if __name__ == "__main__" :
  main()