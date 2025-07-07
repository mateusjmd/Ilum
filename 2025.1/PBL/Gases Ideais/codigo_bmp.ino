#include <Adafruit_BMP280.h>

Adafruit_BMP280 sensor_bmp;

void setup() {
 Serial.begin(9600);
 sensor_bmp.begin();

// Configuração do sensor. Apenas altere se souber o que está fazendo
 sensor_bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
 Adafruit_BMP280::SAMPLING_X2,
 Adafruit_BMP280::SAMPLING_X16,
 Adafruit_BMP280::FILTER_X16,
 Adafruit_BMP280::STANDBY_MS_500);
 }


void loop() {
 float temperatura = sensor_bmp.readTemperature();
 float pressao = sensor_bmp.readPressure();

 for(int i = 0; i < 5; i++) {
        Serial.print(temperatura);
        Serial.print(",");
        Serial.println(pressao);
        delay(10);  // Espera 10ms entre as medidas
    }

 delay(5000);
}
