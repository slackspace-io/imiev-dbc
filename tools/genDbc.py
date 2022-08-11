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
  i=0
  for f in testFrame:
    print("%s: %s" % (i,hex(f)))
    i+=1
  decoded=frame.decode(testFrame)
#  decoded=frame.decode(bytearray.fromhex("27102E0000000022"))
  #print decoded signals
  for (signal, value) in decoded.items():
      print("Test for PID: %s" % name)
      print (signal + "\t" + hex(value.raw_value) + "\t(" + str(value.phys_value)+ ")")
      print("")


def saveDBC(cm):
  # save dbc
  cm.recalc_dlc("force")
  canmatrix.formats.dumpp({"":cm}, "imiev.dbc")
 


yamlDict=loadYamls()
for yaml in yamlDict:
  if single:
    if single not in yaml:
      continue
  fail = False
  for item in yamlDict[yaml]:
    if "Frame" in item:
      print("Found the frame")
      frameParamDict={"name": None, "size": 8, "arbitration_id": None, "comment": "None"}
      for param in yamlDict[yaml][item]:
        frameParamDict[param]=yamlDict[yaml][item][param]
      name=frameParamDict["name"]
      size=frameParamDict["size"]
      arbitration_id=frameParamDict["arbitration_id"]
      comment=frameParamDict["comment"]
#      canId=yamlDict[yaml][item]["can_id"]
#      comment=yamlDict[yaml][item]["comment"]
#      print(canId,comment,str(hex(canId)))
      for k,v in frameParamDict.items():
        if not v:
          print("Missing parameter: %s for frame: %s, skipping" % (k, yaml))
          fail=True
      if fail:
        continue
      frame = canmatrix.Frame(name, arbitration_id=arbitration_id,  comment = comment, size=size)
      #frame=createFrame(canId, comment)
      try:
        testFrameList=yamlDict[yaml][item]["test_frame"]
        doTest=True
      except:
        doTest=False
        pass
    if "Signal" in item:
      if fail:
        continue
      print("Found the signal: %s" % item)
      signalParamDict={"name": "None", "size": 8, "start_bit": 0, "unit": "None", "offset": 0, "factor": 1.0, "is_float": False, "values": {}, "is_little_endian": True, "is_signed": True}
      for param in yamlDict[yaml][item]:
        signalParamDict[param]=yamlDict[yaml][item][param]
      name=signalParamDict["name"]
      size=signalParamDict["size"]
      start_bit=signalParamDict["start_bit"]
      unit=signalParamDict["unit"]
      factor="{:.{i}f}".format(signalParamDict["factor"], i=len(str(signalParamDict["factor"]).split('.')[1]))
      print(factor)
      is_float=signalParamDict["is_float"]
      offset=signalParamDict["offset"]
      print(offset)
      values=signalParamDict["values"]
      is_signed=signalParamDict["is_signed"]
      print(is_signed)
      is_little_endian=signalParamDict["is_little_endian"]
      print(start_bit)
      signal = canmatrix.Signal(name, size = size,  start_bit = start_bit, unit=unit, factor=factor, offset=offset, values=values, is_little_endian=is_little_endian, is_signed=is_signed)
      frame.add_signal(signal)
  if fail:
    continue
  cm.add_frame(frame)
  if doTest:
    for testFrameString in testFrameList:
      testFrame=bytearray.fromhex(testFrameString)
      testSignal(testFrame, name)
  signalParamDict.clear()





saveDBC(cm)
