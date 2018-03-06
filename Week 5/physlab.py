#
# Python script to read Oscilloscope binary files
# Barry Smalley January 2014 (last updated November 2016)
# b.smalley@keele.ac.uk
#
# January 2018: Modified to run under Python 3.
#
# OWON
#
# Inspired by and using parts from owonreader_01.zip by Fabio Eboli 
# http://www.eevblog.com/forum/testgear/review-of-owon-sds7102/525/
# and information given in
# http://bikealive.nl/owon-bin-file-format.html
#
# see also OWON Oscilloscope PC Guidance Manual.pdf 
#
# bin file format: (big endian)   # LITTLE ENDIAN (BS)
# meaning, size, type, abs.offset, rel.offset to channel string
# preamble:
#   model signature string, 6 bytes, string, 0x00,-0x0A   #  "SPBxxx"
#   unknown, int, 4bytes, 0x06, -0x04    FILE LENGTH (BS)
# first trace:
#   channel string, 3 bytes, string, 0x0A, 0x00      "CHx"  x (1,2,A,B,C,D)
#   trace data size, 4 bytes, int,0x0D, 0x03       LENGTH OF BLOCK
#   unknown, 4 bytes, int, 0x11, 0x07  # WHOLE SCREEN COLLECTING POINTS
#   First Point to screen, 4 bytes, int, 0x15, 0x0B   # NUMBER OF COLLECTING POINTS
#   Number of point to screen, 4 bytes, int, 0x19, 0x0F  # SLOW MOVING NUMBER
#   Memory depth, 4 bytes, int, 0x1D, 0x13  # TIME BASE
#   slow scan, 4 bytes, int, 0x21, 0x17  # ZERO POINT
#   T/div, 4 bytes, int, 0x25, 0x1B   # VOLTAGE LEVEL 
#   Zero, 4 bytes, int, 0x29, 0x1F   # ATTENUATION
#   V/Div, 4 bytes, int, 0x2D, 0x23   # TIME INTERVAL (FLOAT)
#   Probe attn, 4 bytes, int, 0x31, 0x27 # FREQUENCY 
#   unknown, 4 bytes, float, 0x35, 0x2B # CYCLE
#   frequency, 4 bytes, float, 0x39, 0x2F # VOLTAGE PER POINT
#   period, 4 bytes, float, 0x3D, 0x33
#   mV per bit, 4 bytes, float, 0x41, 0x37
#   data,1 byte*Memory depth,0x45,0x3B  # 0x33 
# second trace (eventual):
#   ... like first trace, change only abs. offsets

def owonread(filename):

  from struct import unpack
  import numpy as np
  import os
  import sys

  blocks=[]
  SeqT=[1,2.5,5,10,25,50,100,250,500]
  LabT=['nS','uS','mS','S']
  SeqTs=[0.000000001,0.000001,0.001,1]
  SeqV=[1,2,5,10,20,50,100,200,500]
  LabV=['mV','V']
  SeqVv=[0.001,1]
  PrAttn=[1,10,100,1000]

  f=open(filename,'rb')

  DsoStr=f.read(6).decode("ascii")
#  print(DsoStr)
  if DsoStr!="SPBV01": #Check dso model signature
    print("wrong data file type")
    f.close()
    return(-1)
  
  BlockNumber=0
  BlockStart=0x0A   #first "CHx" string
  f.seek(BlockStart)
  CHStr=f.read(3).decode("ascii")
#  print(CHStr)
  if CHStr=="CH1":# till the EOF
    BlockNumber=BlockNumber+1
    f.seek(BlockStart)
    Channel=str(f.read(3).decode("ascii"))
    f.seek(0x03+BlockStart)
    BlockSize=unpack('i',f.read(4))[0] #block size 
    if BlockSize<0:
      BlockSize=-BlockSize
    BlockSize=BlockSize+3  #including "CHx"
    f.seek(0x0B+BlockStart)
    NumSamples=unpack('i',f.read(4))[0] # Number of Collecting Points
    f.seek(0x13+BlockStart)
    Tdiv=unpack('i',f.read(4))[0]       # Time Per division
    TimePerDivStr=str(SeqT[(Tdiv+2)%9])+LabT[(Tdiv+2)//9]+"/div"
    TimePerDiv=float(SeqT[(Tdiv+2)%9])*(SeqTs[(Tdiv+2)//9]) #numeric format
    ZeroLev=unpack('i',f.read(4))[0]        # zero voltage
#    f.seek(0x1B+BlockStart)
    Vdiv=unpack('i',f.read(4))[0]       # Voltage per division
    VoltPerDivStr=str(SeqV[(Vdiv+1)%9])+LabV[(Vdiv+1)//9]+"/div"
    VoltPerDiv=float(SeqV[(Vdiv+1)%9])*(SeqVv[(Vdiv+1)//9])
    ProbeAttn=PrAttn[unpack('i',f.read(4))[0]]  # probe attenuation
    f.seek(0x27+BlockStart)
    Freq=unpack('i',f.read(4))[0]        # frequency
#    f.seek(0x2B+BlockStart)
    Period=unpack('i',f.read(4))[0]      # period
    mVperBit=unpack('f',f.read(4))[0]      # Voltage multipier mV per LSB
    SperSample=TimePerDiv/NumSamples*10
#    f.seek(BlockStart+0x33)
#    CHStr=f.read(2)
    x1 = np.empty(NumSamples)
    y1 = np.empty(NumSamples)
    for i in range(NumSamples):
      y1[i] = unpack('h',f.read(2))[0]*mVperBit/1000*ProbeAttn
      x1[i] = SperSample*i
    BlockStart=BlockStart+BlockSize
    f.seek(BlockStart)
#  print('-------Parameters-----------')
#  print("Device code: ",DsoStr)
#  print("---------Block ",BlockNumber,"----------")
    print(Channel,":")
#  print("Block start: ",BlockStart)
#  print("Block Length: ",BlockSize)
    print("Number of Samples: ",NumSamples)
    print("Time per division: ",TimePerDivStr)
    print("Volt per division: ",VoltPerDivStr)
#  print("Frequency: ",Freq)
#  print("Period: ",Period)
#  print("mVperBit: ",mVperBit)
#  print("Attenuation: ",ProbeAttn)
  else:
    print("CH1 is OFF")
#    f.close()
    x1 = np.zeros(1)
    y1 = np.zeros(1)
#    return(-1)

  
  f.seek(BlockStart)
  CHStr=f.read(3).decode("ascii") 
#  print CHStr
  if CHStr=="CH2":# till the EOF
    BlockNumber=BlockNumber+1
    f.seek(BlockStart)
    Channel=str(f.read(3).decode("ascii"))
    f.seek(0x03+BlockStart)
    BlockSize=unpack('i',f.read(4))[0] #block size 
    if BlockSize<0:
      BlockSize=-BlockSize
    BlockSize=BlockSize+3  #including "CHx"
    f.seek(0x0B+BlockStart)
    NumSamples=unpack('i',f.read(4))[0] # Number of Collecting Points
    f.seek(0x13+BlockStart)
    Tdiv=unpack('i',f.read(4))[0]       # Time Per division
    TimePerDivStr=str(SeqT[(Tdiv+2)%9])+LabT[(Tdiv+2)//9]+"/div"
    TimePerDiv=float(SeqT[(Tdiv+2)%9])*(SeqTs[(Tdiv+2)//9]) #numeric format
    ZeroLev=unpack('i',f.read(4))[0]        # zero voltage
#    f.seek(0x1B+BlockStart)
    Vdiv=unpack('i',f.read(4))[0]       # Voltage per division
    VoltPerDivStr=str(SeqV[(Vdiv+1)%9])+LabV[(Vdiv+1)//9]+"/div"
    VoltPerDiv=float(SeqV[(Vdiv+1)%9])*(SeqVv[(Vdiv+1)//9])
    ProbeAttn=PrAttn[unpack('i',f.read(4))[0]]  # probe attenuation
    f.seek(0x27+BlockStart)
    Freq=unpack('i',f.read(4))[0]        # frequency
#    f.seek(0x2B+BlockStart)
    Period=unpack('i',f.read(4))[0]      # period
    mVperBit=unpack('f',f.read(4))[0]      # Voltage multipier mV per LSB
    SperSample=TimePerDiv/NumSamples*10
#    BlockStart=BlockStart+BlockSize
#    f.seek(BlockStart)
#    f.seek(BlockStart+0x33)
#    CHStr=f.read(2)
    x2 = np.empty(NumSamples)
    y2 = np.empty(NumSamples)
    for i in range(NumSamples):
      y2[i] = unpack('h',f.read(2))[0]*mVperBit/1000*ProbeAttn
      x2[i] = SperSample*i
    f.close()
#  print('-------Parameters-----------')
#  print("Device code: ",DsoStr)
#  print("---------Block ",BlockNumber,"----------")
    print(Channel,":")
#  print("Block start: ",BlockStart)
#  print("Block Length: ",BlockSize)
    print("Number of Samples: ",NumSamples)
    print("Time per division: ",TimePerDivStr)
    print("Volt per division: ",VoltPerDivStr)
#  print("Frequency: ",Freq)
#  print("Period: ",Period)
#  print("mVperBit: ",mVperBit)
#  print("Attenuation: ",ProbeAttn)
  else:
    print("CH2 is OFF")
    x2 = np.zeros(1)
    y2 = np.zeros(1)
#    f.close()
#    return(-1)

  if (len(x1) == 1):
   x1 = x2
   y1 = np.zeros(len(x2))
  if (len(x2) == 1):
   x2 = x1
   y2 = np.zeros(len(x1))
  
  return(x1,y1,x2,y2)


#
# TENMA
#

def tenmaread(filename):
  from struct import unpack
  import numpy as np
  import os
  import sys

  LabT=['nS','uS','mS','S']
  LabV=['mV','V']

  f=open(filename,'rb')

  FileSize = os.path.getsize(filename)
#  print "file size = ", FileSize

#  data=np.zeros(FileSize)
#  for i in range(FileSize):
#    data[i] = unpack('B',f.read(1))[0]

  head=np.zeros(FileSize)
#  f.seek(0)

#  return(data)
  
# MAIN HEADER 124 bytes
# 
# 0  170
# 1  85
# 2  1
# 3-6 ".SAV"
# 7-9  2  1  13
# 10-16 "72-8705"
# 17-19 0 0 0
# 20-29 "0140319012" "0134613003"   Serial Number (?)
# 30-35 0 0 0 0 0 0
# 36: 1  (0 when CH2 off)
# 37: 25
# 38-39 0 25
# 40-41 0 12
# 42-43 0 8
# 44-45 0 1
# 46-47 0 1
# 48: 66
# 49-50: e.g. 123 1  approx SampleLength/16+(4 or 5)
# 51-52: 0 0
# 53-59: all 255 ? [except 57 251 on some data]
#    60: Average: normal (0) peak (1) average (2)
#    61: 1 for 2ns/10ns otherwise 0 ??
# 62-63: 0 1
# 64: 80    (Hold Off value default 80.00 ns) ?
# 65-72: all 0
# 73: trigger DC (0) AC (1) HF reject (2) LF reject (3)
# 74: trigger rise (0) fall (1) risefall (2)
# 75: 20 with 2ns/10ns otherwise 25 or 28  ??
# 76-86: all 0
# 87-88: 1 0
# 89-96: signed long long: trigger level [micro volts]
# 97: number of channels? 2 (was 1 when CH1 or CH2 off)
# 98: 1 = RUN, 0 = STOP
# 99-123: All 255 ?

  f.seek(10)
  DsoStr=f.read(7).decode("ascii")
  if DsoStr!="72-8705": #Check dso model signature
    print("wrong data file type")
    f.close()
    return(-1)
  f.seek(0)

  HeaderSize = 124
  for i in range(HeaderSize):
    j = f.tell()
    byte = f.read(1)
#    print j,i,unpack('c',byte)[0],unpack('B',byte)[0]
    head[j] = unpack('B',byte)[0]

  numChannels = head[97]

# time base /div
# 2ns, 5ns, 10ns, 20ns,50ns,100ns,200ns,500ns
# 1us, 2us, 5us, 10us, 20us, 50us, 100us, 200us, 500us
# 1ms, 2ms, 5ms, 10ms, 20ms, 50ms, 100ms, 200ms, 500ms
# 1s, 2s, 5s, 10s, 20s, 50s

# volts/div
# 1mV ... 20V/div
# 1mV, 2mV, 5mV, 10mv, 20mV, 50mV, 100mV, 200mV, 500mV,
# 1V, 2V, 5V, 10V, 20V


# CHANNEL HEADER (62 bytes)
# Usually starts at 124(Ch1) and SampleLength*2+186 (Ch2)
# Offsets:
#     0: Channel number: Ch1 = 0, Ch2 = 1
#     1: Coupling: DC (0) AC (1) GND (2)
#     2: BW on (1) off (0)
# 3-10: ?
#    11: Probe: x1 (0) x10 (1) x100 (4) x1000 (3)
#    12: Invert: on (1) off (0)
# 13-14: 2-bytes: zero volt point (vpos = 0 gives 128) 
# 15-22: 8-byte long long: volts per division [micro volts]
# 23-30: 8-byte signed long long: hpos offset [pico seconds]
# 31-38: 8-byte long long: time per division [pico seconds]
# 39-46: 8-byte long long: timestep per point [pico seconds]
# 47-50: 4-byte long: sample length
# 51-54: 4-byte long: hpos offset point
# 55-61: ? All 255 (Ch1)?  All 15 (Ch2)?

#
# Ch 1
# header 62 bytes
# data SampleLength*2 bytes
  Channel = unpack('B',f.read(1))[0]
  Coupling = unpack('B',f.read(1))[0]
  BWLimit = unpack('B',f.read(1))[0]
  f.seek(8,1)
  Probe = unpack('B',f.read(1))[0]
  Invert = unpack('B',f.read(1))[0]
  VoltZeroPoint = unpack('<H',f.read(2))[0]
  VoltPerDiv = unpack('<Q',f.read(8))[0]
  HorPos = unpack('<q',f.read(8))[0]
  TimePerDiv = unpack('<Q',f.read(8))[0]
  TimePerPoint = unpack('<Q',f.read(8))[0]
  SampleLength = unpack('<L',f.read(4))[0]
  HorPosPoint = unpack('<L',f.read(4))[0]
  f.seek(7,1)

#  print(f.tell())

#  print(Channel," ",Coupling," ",BWLimit," ",Probe," ",Invert)
#  print(VoltZeroPoint," ",VoltPerDiv)
#  print(HorPos)
#  print(TimePerDiv," ",TimePerPoint)
#  print(SampleLength," ",HorPosPoint)

  print("Channel: ",Channel+1)
  print("Number of Samples: ",SampleLength)
  
  if (TimePerDiv < 1e3):
    print("Time per division: ",TimePerDiv," pS")
  elif (TimePerDiv < 1e6):
    print("Time per division: ",TimePerDiv/1e3," nS")
  elif (TimePerDiv < 1e9):
    print("Time per division: ",TimePerDiv/1e6," uS")
  elif (TimePerDiv < 1e12):
    print("Time per division: ",TimePerDiv/1e9," mS")
  else:
    print("Time per division: ",TimePerDiv/1e12, " S")
    
  if (VoltPerDiv < 1e3):
    print("Volt per division: ",VoltPerDiv," uV")
  elif (VoltPerDiv < 1e6):
    print("Volt per division: ",VoltPerDiv/1e3," mV")
  else:
    print("Volt per division: ",VoltPerDiv/1e6," V")

  x1 = np.empty(SampleLength)
  y1 = np.empty(SampleLength)
  j = 0
  for i in range(SampleLength):
    value = unpack('<H',f.read(2))[0]
    if (value != 65535):
      y1[j] = value
      x1[j] = i*1.
      y1[j] = y1[j]-VoltZeroPoint
      y1[j] = y1[j]*VoltPerDiv/256/1E5
      x1[j] = x1[j]*TimePerPoint/1E12
      j = j + 1

  if (j < SampleLength):
    x1.resize(j)
    y1.resize(j)
    

  if (numChannels == 2):
#
# Ch 2
# header 62 bytes
# data SampleLength*2 bytes
   Channel = unpack('B',f.read(1))[0]
   Coupling = unpack('B',f.read(1))[0]
   BWLimit = unpack('B',f.read(1))[0]
   f.seek(8,1)
   Probe = unpack('B',f.read(1))[0]
   Invert = unpack('B',f.read(1))[0]
   VoltZeroPoint = unpack('<H',f.read(2))[0]
   VoltPerDiv = unpack('<Q',f.read(8))[0]
   HorPos = unpack('<Q',f.read(8))[0]
   TimePerDiv = unpack('<Q',f.read(8))[0]
   TimePerPoint = unpack('<Q',f.read(8))[0]
   SampleLength = unpack('<L',f.read(4))[0]
   HorPosPoint = unpack('<L',f.read(4))[0]
   f.seek(7,1)

#  print(f.tell())

#  print(Channel," ",Coupling," ",BWLimit," ",Probe," ",Invert)
#  print(VoltZeroPoint," ",VoltPerDiv)
#  print(HorPos)
#  print(TimePerDiv," ",TimePerPoint)
#  print(SampleLength," ",HorPosPoint)

   print("Channel: ",Channel+1)
   print("Number of Samples: ",SampleLength)
  
   if (TimePerDiv < 1e3):
     print("Time per division: ",TimePerDiv," pS")
   elif (TimePerDiv < 1e6):
     print("Time per division: ",TimePerDiv/1e3," nS")
   elif (TimePerDiv < 1e9):
     print("Time per division: ",TimePerDiv/1e6," uS")
   elif (TimePerDiv < 1e12):
     print("Time per division: ",TimePerDiv/1e9," mS")
   else:
     print("Time per division: ",TimePerDiv/1e12, " S")
     
   if (VoltPerDiv < 1e3):
     print("Volt per division: ",VoltPerDiv," uV")
   elif (VoltPerDiv < 1e6):
     print("Volt per division: ",VoltPerDiv/1e3," mV")
   else:
     print("Volt per division: ",VoltPerDiv/1e6," V")

   x2 = np.empty(SampleLength)
   y2 = np.empty(SampleLength)
   j = 0
   for i in range(SampleLength):
     value = unpack('<H',f.read(2))[0]
     if (value != 65535):
       y2[j] = value
       x2[j] = i*1.
       y2[j] = y2[j]-VoltZeroPoint
       y2[j] = y2[j]*VoltPerDiv/256/1E5
       x2[j] = x2[j]*TimePerPoint/1E12
       j = j + 1

   if (j < SampleLength):
     x2.resize(j)
     y2.resize(j)

#  print(f.tell(),FileSize-f.tell())
  else:
   x2 = x1
   if (Channel == 1):
    y2 = y1
    y1 = np.zeros(len(x1))
   else:
    y2 = np.zeros(len(x2)) 

# TRAILER (8 bytes)
# all 15

  TrailerSize = 8
  for i in range(TrailerSize):
    j = f.tell()
    byte = f.read(1)
#    print(j,i,unpack('c',byte)[0],unpack('B',byte)[0])
    head[j] = unpack('B',byte)[0]

  return(x1,y1,x2,y2)
