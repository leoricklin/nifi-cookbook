var InputStreamCallback =  Java.type("org.apache.nifi.processor.io.InputStreamCallback");
var OutputStreamCallback =  Java.type("org.apache.nifi.processor.io.OutputStreamCallback");
var IOUtils = Java.type("org.apache.commons.io.IOUtils");
var StandardCharsets = Java.type("java.nio.charset.StandardCharsets");
 
var flowFile = session.get();
if(flowFile != null) {
  try {
  // Create a new InputStreamCallback, passing in a function to define the interface method
  var text = "";
  session.read(flowFile,
    new InputStreamCallback(function(inputStream) {
        text = IOUtils.toString(inputStream, StandardCharsets.UTF_8);
        // Do something with text here
    }));
  var lines = text.split("\n");
  var output = lines[lines.length-4] +","+lines[lines.length-3] +","+lines[lines.length-2];
    new OutputStreamCallback(function(outputStream) {
        outputStream.write(output.getBytes(StandardCharsets.UTF_8))
    }));
  session.transfer(flowFile, REL_SUCCESS)
  } catch(e) {
    log.error('Parsing flow file NG', e)
    session.transfer(flowFile, REL_FAILURE)
  }
}