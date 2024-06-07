String msg = "";
String action = "";
float Vx = 0;
float Vy = 0;
float W = 0;

void setup() {
  // Iniciar la comunicación serial a 9600 baudios
  Serial.begin(115200);
  while (!Serial) {
    ; // Esperar a que se inicie la conexión serial
  }
}

void process_msg(){
  int i = 0;
  action = "";
  // Serial.println(msg);
  while (msg[i] != ';') {
    action += msg[i];
    i++;
  }
  msg = msg.substring(i + 1);
}

void receiveData() {
  if (Serial.available() > 0) {
    msg = Serial.readStringUntil('\n');
  }
}

void move_base() {
  Serial.println("Move base");
  Serial.print("Vx: ");
  Serial.print(Vx);
  Serial.print(" Vy: ");
  Serial.print(Vy);
  Serial.print(" W: ");
  Serial.println(W);
  Serial.println("Move base end");
}

void getAction() {
  // split the string into three variables
  int i = 0;
  
  for (int j = 0; j < 3; j++) {
    String value = "";
    while (action[i] != ',' && i < action.length()) {
      value += action[i];
      i++;
    }
    i++;
    if (j == 0) {
      Vx = value.toFloat();
    }
    else if (j == 1) {
      Vy = value.toFloat();
    }
    else {
      W = value.toFloat();
    }
  }

  // unir las tres variables en una sola cadena
  String la = String(Vx) + ";" + String(Vy) + ";" + String(W);
  Serial.println(la);
  action = "";
}
void loop() {
  
  // If msg is empty, read the next message
  if (msg == "") {
    receiveData();
  }
  else {
    process_msg(); // action = 'Vx,Vy,W'
    
    // Serial.println(action);
    // Serial.println("Process message");
    // Serial.println(action);
    getAction();
  //   move_base();
  }
}
