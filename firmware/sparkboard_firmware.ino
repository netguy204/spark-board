#include "inputs.h"

void setup() {
  Serial.begin(9600);
  pinMode(DATA, OUTPUT);
  pinMode(CLOCK, OUTPUT);
  pinMode(LATCH, OUTPUT);
}

void loop() {
  MATRIX_RESULT result;
  LIGHTS lights;
  
  scan_matrix(result);
  for(uint8_t ii = 0; ii < ARRAY_SIZE(result); ++ii) {
    lights[ii % ARRAY_SIZE(lights)] = result[ii];
    Serial.print(result[ii]);
    Serial.print(" ");
  }
  Serial.println();
  draw_screen(lights);
  delay(1000);
}
