#include "inputs.h"

uint8_t enables[][3] = {
   {13, 2, 8},
   {4, 1, 9},
   {12, 6, 4},
   {15, 8, 0},
   {10, 7, 15},
   {9, 14, 11},
   {12, 6, 9},
   {8, 15, 2},
   {7, 10, 8},
   {3, 6, 14},
   {3, 11, 9},
   {13, 5, 10}
};

uint8_t disables[] = {
 9,
 7,
 8,
 6,
 4,
 5,
 5,
 3,
 1,
 7,
 10,
 11
};

void setup() {
  //Serial.begin(9600);
  pinMode(DATA, OUTPUT);
  pinMode(CLOCK, OUTPUT);
  pinMode(LATCH, OUTPUT);
}

void loop() {
  MATRIX_RESULT result;
  LIGHTS lights;

  scan_matrix(result);
  for(uint8_t ii = 0; ii < ARRAY_SIZE(lights); ++ii) {
    lights[ii] = 0;
  }


  for(uint8_t ii = 0; ii < ARRAY_SIZE(result); ++ii) {
    for(uint8_t jj = 0; jj < ARRAY_SIZE(enables[ii]); ++jj) {
      if(result[ii] > 0) {
        lights[enables[ii][jj]] = 1;
      }
    }
  }

  for(uint8_t ii = 0; ii < ARRAY_SIZE(result); ++ii) {
    if(result[ii] > 0) {
      lights[disables[ii]] = 0;
    }
  }


  /*
  for(uint8_t ii = 0; ii < ARRAY_SIZE(result); ++ii) {
    if(result[ii] > 0) {
      lights[ii] = 1;
    }
    Serial.print(result[ii]);
    Serial.print(" ");
  }
  Serial.println();
  */

  draw_screen(lights);
  //delay(1000);
}
