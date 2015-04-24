#include <Arduino.h>
#include <stdint.h>
#include <avr/pgmspace.h>

#define ARRAY_SIZE(x) (sizeof(x) / sizeof(x[0]))
#define EN0 2
#define EN1 3

#define SB0 5
#define SB1 6
#define SB2 7
#define SB3 8

#define DATA 9
#define CLOCK 10
#define LATCH 11

const uint8_t matrix_enables[] PROGMEM = {EN0, EN1};
const uint8_t matrix_data[] PROGMEM = {SB0, SB1, SB2, SB3};
typedef uint8_t MATRIX_RESULT[ARRAY_SIZE(matrix_enables) * ARRAY_SIZE(matrix_data)];
typedef uint8_t LIGHTS[16];

uint8_t scan_matrix(MATRIX_RESULT result) {
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
      result[idx] = value;
    }
    
    // put the enable line hiz
    pinMode(en, INPUT);
  }
}

void draw_screen(LIGHTS lights) {
  for(uint8_t ii = 0; ii < 2; ++ii) {
    uint8_t output = 0;
    for(uint8_t jj = 0; jj < 8; ++jj) {
      uint8_t value = (lights[ii * 8 + jj] > 0);
      output = output << 1;
      output |= value;
      Serial.print(value);
      Serial.print(" ");
    }
    
    Serial.println(output);
    digitalWrite(LATCH, LOW);
    shiftOut(DATA, CLOCK, MSBFIRST, output);
    digitalWrite(LATCH, HIGH);
  }
}


