import canmatrix.formats
import os
import yaml
cm = canmatrix.CanMatrix()

#
# create frame Node604
#


def loadYamls():
  yamlDict=dict()
  for filename in os.scandir("pids"):
    if filename.is_file():
      pid=filename.name.strip('.yaml')
      with open(filename.path, 'r') as stream:
        yamlDict[pid]=yaml.FullLoader(stream).get_data()
  print(yamlDict)
  return yamlDict


def hexToDecimal(hex):
  return(int(hex))


def createFrame(canId, comment):
  frame = canmatrix.Frame(str(hex(canId)), arbitration_id=canId,  comment = comment, size=8)
  return frame


def testSignal(frame):
  decoded=frame.decode(bytearray.fromhex("27102E0000000022"))
  #print decoded signals
  for (signal, value) in decoded.items():
      print("hi")
      print (signal + "\t" + hex(value.raw_value) + "\t(" + str(value.phys_value)+ ")")


def saveDBC(cm):
  # save dbc
  cm.recalc_dlc("force")
  canmatrix.formats.dumpp({"":cm}, "imiev.dbc")
 


yamlDict=loadYamls()
for yaml in yamlDict:
  for item in yamlDict[yaml]:
    if "Frame" in item:
      print("Found the frame")
      canId=yamlDict[yaml][item]["can_id"]
      comment=yamlDict[yaml][item]["comment"]
      print(canId,comment,str(hex(canId)))
      frame=createFrame(canId, comment)
    if "Signal" in item:
      print("Found the signal: %s" % item)
      signalParamDict={"name": "None", "size": 8, "start_bit": 0, "unit": "None", "offset": 0, "factor": 1.0}
      for param in yamlDict[yaml][item]:
        signalParamDict[param]=yamlDict[yaml][item][param]

      name=signalParamDict["name"]
      size=signalParamDict["size"]
      start_bit=signalParamDict["start_bit"]
      unit=signalParamDict["unit"]
      factor=signalParamDict["factor"]
      offset=signalParamDict["offset"]

      signal = canmatrix.Signal(name, size = size,  start_bit = start_bit, unit=unit, factor=factor, offset=offset)
      frame.add_signal(signal)
  cm.add_frame(frame)
  signalParamDict.clear()
saveDBC(cm)
