import canmatrix.formats
import os
import sys
import yaml
cm = canmatrix.CanMatrix()

#
# create frame Node604
#

#for debug -- make proper later :)
try:
  single=sys.argv[1]
except:
  single=None

def loadYamls():
  yamlDict=dict()
  for filename in os.scandir("pids"):
    if filename.is_file():
      pid=filename.name.strip('.yaml')
      with open(filename.path, 'r') as stream:
        yamlDict[pid]=yaml.FullLoader(stream).get_data()
  #print(yamlDict)
  return yamlDict


def hexToDecimal(hex):
  return(int(hex))


def createFrame(canId, comment):
  frame = canmatrix.Frame(str(hex(canId)), arbitration_id=canId,  comment = comment, size=8)
  return frame


def testSignal(testFrame, name):

  decoded=frame.decode(testFrame)
#  decoded=frame.decode(bytearray.fromhex("27102E0000000022"))
  #print decoded signals
  for (signal, value) in decoded.items():
    val_string=value.phys_value
    val=int(value.phys_value)
#    print(val)
#    print(hex(val))
#    print("%s | %s | %s | %s | %s | %s | %s" % (val_string, hex(val),val,start_bit,size, offset, scale))
    if -5 <= val <= -4:
      print("%s | %s | %s | %s | %s | %s | %s | %s | %s" % (val_string, hex(val),val,start_bit,size, offset, scale, is_little_endian, is_signed))
   # if 300 <= val <= 420:
   #   print("FOUND IT: %s | %s | %s | %s" % (hex(val),val,start_bit,size))
#  for (signal, value) in decoded.items():
#      print("Test for PID: %s" % name)
#      print (signal + "\t" + hex(value.raw_value) + "\t(" + str(value.phys_value)+ ")")
#      print("")


def saveDBC(cm):
  # save dbc
  cm.recalc_dlc("force")
  canmatrix.formats.dumpp({"":cm}, "imiev.dbc")

global lowVal
lowVal=10000000

testF="0499024A080226FB"
testFrame=bytearray.fromhex(testF)
#testFrame=bytearray.fromhex("0596E7546D58006F")
arbitration_id=0x99
name="Test"
is_signed=False
for i in range(46,52):
  start_bit=i
  for i in range(14,17):
    size=i
    if size+start_bit > 63:
      continue
    for i in range(1,1500):
      offset=-i
      for i in range(1,200):
        scale=i*.01
        for i in range(1,3):
          if i == 1:
            is_little_endian=False
          if i == 2:
            is_little_endian=True
#            print(start_bit,size,offset,scale,is_little_endian,is_signed)
          frame = canmatrix.Frame(name, arbitration_id=arbitration_id, size=8)
          signal = canmatrix.Signal(name, size = size,  start_bit = start_bit, is_little_endian=is_little_endian, is_signed=True,offset=offset, factor=scale)
          frame.add_signal(signal)
          cm.add_frame(frame)
          testSignal(testFrame, name)
          cm.remove_frame(frame)

#for i in range(1,1500):
#  print(i)
#  print(0xb6+i*-.1)



