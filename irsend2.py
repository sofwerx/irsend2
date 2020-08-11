#!/usr/bin/env python3

import fcntl
import array
import os
import struct
import select
import threading
import subprocess
import decode
import logging
import sys

logging.basicConfig(filename='irsend.log', filemode= 'a', level=logging.DEBUG, format= '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)20s() ] - %(message)s')
logger = logging.getLogger()
  
LIRC_GET_REC_MODE = 0x80046902 # _IOR('i', 0x00000002, __u32)
LIRC_GET_LENGTH = 0x8004690F # _IOR('i', 0x0000000f, __u32)
LIRC_MODE_MODE2 = 0x00000004
PULSE_BIT = 0x01000000
PULSE_MASK = 0x00FFFFFF

result = array.array("I", [0])
lirc_t = "i"
dataSequenceThread = []

##########################################################################
def readLine(fd, interval):
  data = []
  # wait for up to <interval> milliseconds
  readable,_,_ = select.select([fd],[],[], interval)

  if fd in readable:
    rawbuf = os.read(fd, struct.calcsize(lirc_t))
    #print("read")
    rawvalue, = struct.unpack(lirc_t, rawbuf)
    pulseflag = rawvalue & PULSE_BIT
    duration = rawvalue & PULSE_MASK

    if pulseflag != 0:
      data.append("pulse")
      data.append(duration)
    else:
      data.append("space")
      data.append(duration)

  return data

##########################################################################
def readSequence(fd, interval):
  dataSequence = []
  isReceiving = True
  while isReceiving:
    dataDict = readLine(fd, interval)
    #print( data )
    if len(dataDict) == 0:
      isReceiving = False
    else:
      dataSequence.append(dataDict)

  return dataSequence
  
##########################################################################
def readSequenceThread(fd, interval):
  global dataSequenceThread
  
  dataSequenceThread = readSequence( fd, interval )

##########################################################################
def openDevice( devicePath ):
  fd = os.open(devicePath, os.O_RDONLY)
  if fcntl.ioctl(fd, LIRC_GET_REC_MODE, result, True) == -1:
    raise IOError("cannot use {!r} as a raw LIRC device. Is it a LIRC device?".format(self.device))
  if result[0] != LIRC_MODE_MODE2:
    raise IOError("cannot use {!r} as a raw LIRC device. Is it a raw (!) LIRC device?".format(self.device))
   
  return fd
    
##########################################################################
def irsend(deviceName, keyName):    
  global dataSequenceThread
  isMatch = True
    
  deviceConfig = decode.readConf()

  fd = openDevice( "/dev/lirc1" )
  if ( fd ):

    # start the receiving thread
    x = threading.Thread(target=readSequenceThread, args=(fd, 0.100,))
    x.start()
        
    # push the "button"
    os.system("irsend SEND_ONCE %s %s" %(deviceName, keyName))

    # wait for the thread to finish reading the sequence
    x.join()
    
    logger.debug(dataSequenceThread)
    
    keyReceived = decode.decode(dataSequenceThread, deviceName, deviceConfig)
    if keyReceived != keyName:
      isMatch = False
  return isMatch

##########################################################################
def main(argv) :   
  global dataSequenceThread
  
  keyName = sys.argv[1]
  isMatch = irsend("lircd.conf", keyName)  
  print( "isMatch = " + str(isMatch))

##########################################################################
if __name__ == "__main__":
  main(sys.argv[1:])
