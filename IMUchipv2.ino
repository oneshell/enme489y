// ENME 489Y: Remote Sensing
// Spring 2017

// ADXL327 Accelerometer
// http://www.analog.com/media/en/technical-documentation/data-sheets/ADXL327.pdf

// Note: 3.3V required to power the accelerometer chip!

// ADC map
const int x = A1;          // x-axis yellow
const int y = A2;          // y-axis green
const int z = A3;          // z-axis white wire
const int samples = 400;   // number of samples averaged per 100ms
const int gap = 100;       // time for each reading

void setup() {
  Serial.begin(1200);
}

void loop() {

  // initialize voltage sum variables 
  float totalx = 0;
  float totaly = 0;
  float totalz = 0;
  // initialize angle variables
  int xAngle = 0;
  int yAngle = 0;
  int zAngle = 0;
  
  // loop and record voltages 
  for (int i =1; i<= samples; i++)
  {
   
     int xAngleRead = analogRead(x); // angle for x
     int yAngleRead = analogRead(y); // angle for y
     int zAngleRead = analogRead(z); // angle for z
     
   //first number of map is 0 degrees, second number is at 90 degrees; less than 0 is negative degrees
    // x
    // adds up all the voltages
    totalx = xAngleRead + totalx;
    totaly = yAngleRead + totaly;
    totalz = zAngleRead + totalz;
    
    
    delay(gap / samples); // loop delay
  }
  
  // average voltages 
int xAngleAve = totalx / samples;
int yAngleAve = totaly / samples;
int zAngleAve = totalz / samples;
  
  // convert average voltages to angles, given calibration map
xAngle = map( xAngleAve, 342, 435, 0, 90); //angle for x
yAngle = map( yAngleAve, 333, 425, 0, 90); //angle for y
zAngle = map( zAngleAve, 333, 425, 0, 90); //angle for z 

// Send angle measurements to the serial stream to be read by the Raspberry Pi
// Format: x y z
String xyzString = String(xAngle) + " " + String(yAngle) + " " + String(zAngle);
//Serial.print(xyzString);
Serial.println(xyzString);

// The following code can be uncommented to print analog measurements to the screen
// This information is useful when performing the initial angle calibration
// Otherwise, leave this section commented out
//String xyzString = String(analogRead(x)) + "," + String(analogRead(y)) + "," + String(analogRead(z));
//Serial.print(xyzString);
//Serial.println();

}
