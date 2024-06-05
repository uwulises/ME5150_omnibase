void setup() {
  // Iniciar la comunicación serial a 9600 baudios
  Serial.begin(9600);
  while (!Serial) {
    ; // Esperar a que se inicie la conexión serial
  }
  pinMode(25, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    // Leer la información enviada por la Raspberry Pi 4
    String message = Serial.readStringUntil('\n');
    // Mostrar el mensaje recibido en el monitor serial
    Serial.print("Recibido: ");
    Serial.println(message);
    // Activar el LED si se recibe un mensaje
    digitalWrite(25, HIGH);
    delay(1000); // Mantener el LED encendido por 1 segundo
    digitalWrite(25, LOW);
  }
  
}
