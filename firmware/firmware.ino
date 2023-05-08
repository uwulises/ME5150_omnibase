#include <Servo.h>
String inputString = "";
bool stringComplete = false;

// MOTOR A -> A-1A A-1B
// RIGHT MOTOR FRONT
#define FR1 4    //1A
#define FR2 5    //1B

// MOTOR B -> B 1A B 1B
// RIGHT MOTOR BACK
#define BR1 6    //1A
#define BR2 7    //1B

// MOTOR A -> A-1A A-1B
//LEFT MOTOR FRONT
#define FL1 8    //1A
#define FL2 9   //1B

// MOTOR B -> B 1A B 1B
//LEFT MOTOR BACK
#define BL1 10    //1A
#define BL2 11   //1B



void setup()
{
  pinMode(BR1, OUTPUT);
  pinMode(BR2, OUTPUT);
  pinMode(BL1, OUTPUT);
  pinMode(BL2, OUTPUT);
  pinMode(FR1, OUTPUT);
  pinMode(FR2, OUTPUT);
  pinMode(FL1, OUTPUT);
  pinMode(FL2, OUTPUT);

  //softspeed();
  Serial.begin(9600);
  delay(1000);
  Serial.println("----");
  Serial.println("READY");
  Serial.println("----");
  delay(200);
}

void serialEvent()
{
  while (Serial.available())
  {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n')
    {
      stringComplete = true;
    }
  }
}


void FW()
{

}
void BW()
{


}

void TL()
{


}

void DL()
{


}
void DR()
{


}

void TR()
{

}

void STOP()
{

}

void loop()
{

  if (stringComplete)
  {
    Serial.println(inputString);
    if (inputString == "FW\n")
    {
      FW();
    }

    if (inputString == "BW\n")
    {
      BW();
    }
    if (inputString == "TR\n")
    {
      TR();
    }

    if (inputString == "TL\n")
    {
      TL();
    }
    if (inputString == "STOP\n")
    {
      STOP();
    }
    else
    {
      inputString = "";
    }

    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}