String msg = "";
String action = "";
float Vx = 0;
float Vy = 0;
float W = 0;

void setup() {
  // Iniciar la comunicación serial a 9600 baudios
  Serial.begin(115200);
  while (!Serial) {
    ;
  }
}

void processMsg(){
  int i = 0;
  action = "";
  while (msg[i] != ';') {
    action += msg[i];
    i++;
  }
  msg = msg.substring(i + 1);
}

void sendMsg() {
  Serial.println("available");
}

void receiveData() {
  if (Serial.available() > 0) {
    msg = Serial.readStringUntil('\n');
  }
}

void moveBase() {
  String la = String(Vx) + ";" + String(Vy) + ";" + String(W);
  Serial.println(la);
}

void getAction() {
  // Suponiendo que 'action' es un String y contiene "0.000,0.000,0.000"
  // String action = "0.000,0.000,0.000";  // Ejemplo de string para procesar

  int commaIndex1 = action.indexOf(',');
  int commaIndex2 = action.indexOf(',', commaIndex1 + 1);

  Vx = action.substring(0, commaIndex1).toFloat();
  Vy = action.substring(commaIndex1 + 1, commaIndex2).toFloat();
  w = action.substring(commaIndex2 + 1).toFloat();

  action = "";
}

void loop() {
  
  if (msg == "") {
    // sendMsg();
    receiveData();
  }
  else {
    processMsg(); // action = 'Vx,Vy,W'
    getAction();
    moveBase();
  }
}
