from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import InputStreamCallback
from org.apache.nifi.processor.io import OutputStreamCallback
import time
import socket


# Define a subclass of InputStreamCallback for use in session.read()
class PyInputStreamCallback(InputStreamCallback):
  def __init__(self):
    pass
  def process(self, inputStream):
    global inputs
    inputs = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
    # Do something with text here
# end class


# Define a subclass of OutputStreamCallback for use in session.write()
class PyOutputStreamCallback(OutputStreamCallback):
  def __init__(self):
    pass
  def process(self, outputStream):
    outputStream.write(bytearray(outputs.encode('utf-8')))
# end class

flowFile = session.get()
if(flowFile != None):
  # read
  session.read(flowFile, PyInputStreamCallback())
  # process
  who = feedname.getValue()
  what = actionname.getValue()
  when = int(time.time())
  where = socket.gethostname()
  inlines = inputs.strip().splitlines()
  metrics = [ inlines[-3] , inlines[-2] , inlines[-1] ]
  successRate = metrics[0].split(":")
  avgDuration = metrics[1].split(":")
  overwriteRate = metrics[2].split(":")
  sqltemplate = "insert into tab (who, what, when, where, key, value) values ('{}','{}','{}','{}','{}','{}');"
  outlines =     [ sqltemplate.format( who, what, when, where, successRate[0].strip() , successRate[1].strip() ) ]
  outlines.append( sqltemplate.format( who, what, when, where, avgDuration[0].strip() , (":".join(list(map(lambda x: x.strip(), avgDuration[1:])))) ) )
  outlines.append( sqltemplate.format( who, what, when, where, overwriteRate[0].strip() , overwriteRate[1].strip() ) )
  global outputs
  outputs = "\n".join(outlines)
  # write
  flowFile = session.write(flowFile, PyOutputStreamCallback())
  # Last operation is transfer to success (failures handled in the catch block)
  session.transfer(flowFile, REL_SUCCESS)
# implicit return at the end
