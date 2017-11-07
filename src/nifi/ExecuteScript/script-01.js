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
  text = text + "qazwsx";
  flowFile = session.write(flowFile,
    new OutputStreamCallback(function(outputStream) {
        outputStream.write(text.getBytes(StandardCharsets.UTF_8))
    }));
  session.transfer(flowFile, REL_SUCCESS)
  } catch(e) {
    log.error('Something went wrong', e)
    session.transfer(flowFile, REL_FAILURE)
  }
}