#include "inputs.h"

void setup() {
  Serial.begin(9600);
}

void loop() {
  MATRIX_RESULT result;
  scan_matrix(result);
  for(uint8_t ii = 0; ii < ARRAY_SIZE(result); ++ii) {
    Serial.print(result[ii]);
    Serial.print(" ");
  }
  Serial.println();
  delay(1000);
}
