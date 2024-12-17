#include "DHT.h"

const int pino_dht = 9;
float temperatura;
float umidade;
DHT dht(pino_dht, DHT11);
const int ledPinG = 7;
const int ledPinR = 6;
const int ledPinY = 5;

void setup() {
  Serial.begin(9600);
  pinMode(ledPinG, OUTPUT);
  pinMode(ledPinR, OUTPUT);
  pinMode(ledPinY, OUTPUT);
  dht.begin();
}

void loop() {
  temperatura = dht.readTemperature();
  umidade = dht.readHumidity();

  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    if (comando == "leitura_tempUmid") {
      float temperatura = dht.readTemperature();
      float umidade = dht.readHumidity();
      
      if (isnan(temperatura) || isnan(umidade)) {
        Serial.println("Erro ao ler o sensor");
      } else {
        Serial.println(temperatura, 2);
        Serial.println(umidade, 2);
      }
      delay(200);
    }

    if (comando == "led_verde_ligando") {
      digitalWrite(ledPinG, HIGH);
    } else if (comando == "led_verde_desligando") {
      digitalWrite(ledPinG, LOW);
    }
    if (comando == "led_vermelho_ligando") {
      digitalWrite(ledPinR, HIGH);
    } else if (comando == "led_vermelho_desligando") {
      digitalWrite(ledPinR, LOW);
    }
    if (comando == "led_amarelo_ligando") {
      digitalWrite(ledPinY, HIGH);
    } else if (comando == "led_amarelo_desligando") {
      digitalWrite(ledPinY, LOW);
    }
  }
}