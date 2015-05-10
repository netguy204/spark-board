#include <Arduino.h>
#include <stdint.h>
#include <avr/pgmspace.h>

#define ARRAY_SIZE(x) (sizeof(x) / sizeof(x[0]))
#define EN0 1
#define EN1 2
#define EN2 3

#define SB0 5
#define SB1 6
#define SB2 7
#define SB3 8

#define DATA 9
#define CLOCK 10
#define LATCH 11

const uint8_t matrix_enables[] PROGMEM = {EN0, EN1, EN2};
const uint8_t matrix_data[] PROGMEM = {SB0, SB1, SB2, SB3};
typedef uint8_t MATRIX_RESULT[ARRAY_SIZE(matrix_enables) * ARRAY_SIZE(matrix_data)];
typedef uint8_t LIGHTS[16];

const LIGHTS light_mapping PROGMEM = {
  8, 10, 12, 14,
  9, 11, 13, 15,
  0, 2, 7, 5,
  1, 3, 6, 4
};

const MATRIX_RESULT button_mapping PROGMEM = {
  8, 9, 10, 11,
  4, 5, 6, 7,
  0, 1, 2, 3
};

void scan_matrix(MATRIX_RESULT result) {
  for(uint8_t enii = 0; enii < ARRAY_SIZE(matrix_enables); ++enii) {
    // power up the enable line
    uint8_t en = pgm_read_byte_near(matrix_enables + enii);
    pinMode(en, OUTPUT);
    digitalWrite(en, LOW);

    // scan the data lines
    for(uint8_t dii = 0; dii < ARRAY_SIZE(matrix_data); ++dii) {
      uint8_t d = pgm_read_byte_near(matrix_data + dii);
      pinMode(d, INPUT);
      digitalWrite(d, HIGH); // enable pull up resistor

      // test for logic low
      uint8_t idx = enii * ARRAY_SIZE(matrix_data) + dii;
      uint8_t value = (digitalRead(d) == 0);
      /*
      Serial.print(en);
      Serial.print(" => ");
      Serial.print(d);
      Serial.print(": ");
      Serial.println(value);
      */
      //uint8_t nidx = pgm_read_byte_near(button_mapping + idx);
      result[idx] = value;
    }

    // put the enable line hiz
    pinMode(en, INPUT);
  }
}

void draw_screen(LIGHTS lights) {
  LIGHTS rlights;
  for(uint8_t ii = 0; ii < 16; ++ii) {
    uint8_t nii = pgm_read_byte_near(light_mapping + ii);
    rlights[nii] = lights[ii];
  }

  digitalWrite(LATCH, LOW);
  for(uint8_t ii = 0; ii < 2; ++ii) {
    uint8_t output = 0;
    for(uint8_t jj = 0; jj < 8; ++jj) {
      uint8_t value = (rlights[ii * 8 + jj] > 0);
      output = output << 1;
      output |= value;
      //Serial.print(value);
      //Serial.print(" ");
    }

    //Serial.println(output);

    shiftOut(DATA, CLOCK, MSBFIRST, output);
  }
  digitalWrite(LATCH, HIGH);
}
