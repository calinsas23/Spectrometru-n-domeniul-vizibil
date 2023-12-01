Codul pentru controlul motorului pas cu pas
#include Stepper.h
#define STEPS 32
Stepper stepper(STEPS, 8, 10, 9, 11);
int valoare_curenta = 0;
void setup() {
Serial.begin(9600);
stepper.setSpeed(400);
}
void loop()
{
valoare_curenta = map(analogRead(A0),0,1024,0,900);
if (valoare_curenta600)
stepper.step(1);
if (valoare_curenta=300)
stepper.step(-1);
delay(2000);
Serial.println(valoare_curenta);
}
folosim potentiometrul pe post de buton
impartim 1000 in 3 intervale 0-300 face rotatii in stanga cu 301-700 off 700-999 face deplasari dreapta