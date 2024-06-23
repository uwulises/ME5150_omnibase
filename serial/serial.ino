
SerialPIO serial2(16, 17);
byte msg = 0;
String str_msg = "";
String formatted_msg = "";

void setup(){
  serial2.begin(115200);
  delay(1000);
}

void loop(){
  msg =  serial2.read();
  //from binary to string
  str_msg = AsciiToChar(msg);
  formatted_msg =  "received:"+str_msg+"\n";
  serial2.write(formatted_msg.c_str());
  delay(1000);
}

char AsciiToChar( byte asciiCode )   { return (asciiCode +'\0' ); }