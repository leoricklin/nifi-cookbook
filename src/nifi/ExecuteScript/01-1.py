from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import InputStreamCallback
from org.apache.nifi.processor.io import OutputStreamCallback

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
  global outputs
  outputs = inputs
  # write
  flowFile = session.write(flowFile, PyOutputStreamCallback())
  # Last operation is transfer to success (failures handled in the catch block)
  session.transfer(flowFile, REL_SUCCESS)
# implicit return at the end
