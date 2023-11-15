#include <SparkFun_Bio_Sensor_Hub_Library.h>
#include <Wire.h>

// No other Address options.
#define DEF_ADDR 0x55

// Takes address, reset pin, and MFIO pin.
SparkFun_Bio_Sensor_Hub bioHub(8, 9);

bioData sample;

void setup() {
  Serial.begin(115200);

  Wire.begin();
  int result = bioHub.begin();
  if (!result)
    Serial.println("Sensor started!");
  else
    Serial.println("Could not communicate with the sensor!");
    
  int error = bioHub.configBpm(MODE_TWO); // Configuring just the BPM settings.
  if (!error) {
    Serial.println("Sensor configured.");
  }
  else {
    Serial.println("Error configuring sensor:" + error);
  }
  
  // Data lags a bit behind the sensor, if you're finger is on the sensor when
  // it's being configured this delay will give some time for the data to catch up.
  delay(4000);
}

void loop() {

  // Information from the readBpm function will be saved to the "sample" variable.
  sample = bioHub.readBpm();
  Serial.println(sample.heartRate);
  Serial.println(sample.confidence);
  Serial.println(sample.oxygen);
  Serial.println(sample.extStatus);
  // 0   Success
  // 1   Not Ready
  // -1  Object Detected
  // -2  Excessive Sensor Device Motion
  // -3  No object detected
  // -4  Pressing too hard
  // -5  Object other than finger detected
  // -6  Excessive finger motion
  delay(500); // Delay in ms
}
