#include <Arduino_LSM6DS3.h>

unsigned long adjustUs = 260000; //this value has been found by measuring the error of timing vs frequency
volatile int rev = 0;
float RPM = 0;
volatile unsigned long startTime = 0; 
volatile unsigned long detectTime = 0; 

volatile unsigned long previousUsIMU = 0;             // will store last time imu checked.
volatile unsigned long previousUsRPMsent = 0;         // will store last time rpm was sent.
volatile unsigned long previousUsRPMcompute = 0;      // will store last time rpm was calculate.
volatile bool newMeasure = true;
volatile unsigned long numberOfTry = 0;

float x,y,z;

bool ping = false;
bool get_sensor_data = false;
bool start_stream = false;

void setup() {
  Serial.begin(9600);
  if(!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  pinMode(3, INPUT);
  attachInterrupt(digitalPinToInterrupt(3), ISR_rev, RISING);
  delay(200);//wait for initialisation

}

void loop() {

  imuRead(9000);
  rpmRead(9000); 

  String Receive ;
  
  if (Serial.available()) {

    String input = Serial.readString();
    input.trim();
    
    if (input.startsWith("PING")) { 
      ping = true; 
      Receive = input.substring(5);  } 
    else if (input.equals("GET_SENSOR_DATA")) { get_sensor_data = true; } 
    else if (input.equals("START_STREAM")) { start_stream = true;} 
    else if (input.equals("STOP_STREAM")) { 
      start_stream = false;
      Serial.println("The data sensor stream has been stopped.");
    }
    else { Serial.println("Unknown command, please try again."); }

    input = "";
  }

    if (ping) {
      Serial.print("TS = ");
      Serial.print(millis());   
      Serial.print(" ms");
      Serial.print(", ");
      Serial.print("REQTIME = ");
      Serial.print(Receive);           
      Serial.print(", ");
      Serial.println("V3.5 READY");

      ping = false;
      
    } else if (get_sensor_data) {
      Serial.print("TS = ");
      Serial.print(millis());
      Serial.print(" ms");
      Serial.print(", ");
      Serial.print("TACHO = ");
      Serial.print(RPM);
      Serial.print(" RPM");
      Serial.print(", ");
      Serial.print("IMU = (");
      Serial.print(x, 4);
      Serial.print(", ");
      Serial.print(y, 4);
      Serial.print(", ");
      Serial.print(z, 4);
      Serial.println(") g");

      get_sensor_data = false;
    
    } else if (start_stream) {
      sendData(20000);
    } 
}

void imuRead(unsigned long intervalUs){
  unsigned long currentUs = micros();
  if(currentUs - previousUsIMU > intervalUs){
    IMU.readAcceleration(x,y,z);
    previousUsIMU = currentUs;
  }
}

void rpmRead(unsigned long intervalUs){ // Calculate rpm each intervalUs microseconds
  unsigned long currentUs = micros();
  if(currentUs - previousUsRPMcompute > intervalUs) {
        
    previousUsRPMcompute = currentUs;   // save the last time you've claculated
    
    if(rev>0){
      RPM = (rev * (adjustUs+60000000.0)) / (detectTime - startTime);
      rev = 0;
      newMeasure = true;
      numberOfTry = 0;
    }else{
      numberOfTry++;
      if(numberOfTry * intervalUs > 100000){  // if 1 second without detection rpm = 0
        RPM = 0;
        numberOfTry = 0;
      }
    } 
  }  
}

void sendData(unsigned long intervalUs){
  unsigned long currentUs = micros();
  if(currentUs - previousUsRPMsent > intervalUs) {
    // save the last time you've sent RPM 
    previousUsRPMsent = currentUs;  
    Serial.print("TS = ");
    Serial.print(millis());
    Serial.print(" ms");
    Serial.print(", ");; 
    Serial.print("TACHO = ");
    Serial.print(RPM);
    Serial.print(" RPM");
    Serial.print(", ");
    Serial.print("IMU = (");
    Serial.print(x, 4);
    Serial.print(", ");
    Serial.print(y, 4);
    Serial.print(", ");
    Serial.print(z, 4);
    Serial.println(") g");
  }
}

void ISR_rev() {
   if(newMeasure){
    startTime = micros();     
    newMeasure = false;
  }else{
    detectTime = micros();
    if(startTime>detectTime){ // when micros overflow after 75mn reset all previous times and the startTime
      //Serial.println("overflow");
      startTime = detectTime;
      previousUsRPMcompute = detectTime;
      previousUsRPMsent = detectTime;
      previousUsIMU = detectTime;
      numberOfTry = 0;
      rev = 0;
    }else{
      ++rev;
    }
  }
}
