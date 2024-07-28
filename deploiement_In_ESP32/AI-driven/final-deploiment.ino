#include <TensorFlowLite_ESP32.h>
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "DHT.h"

#include "model_temp.h"
#include "model_humid.h"

#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

namespace {
  tflite::ErrorReporter* error_reporter = nullptr;
  const tflite::Model* model_temp = nullptr;
  const tflite::Model* model_humid = nullptr;
  tflite::MicroInterpreter* interpreter_temp = nullptr;
  tflite::MicroInterpreter* interpreter_humid = nullptr;
  TfLiteTensor* input_temp = nullptr;
  TfLiteTensor* input_humid = nullptr;

  constexpr int kTensorArenaSize = 2 * 1024;
  uint8_t tensor_arena[kTensorArenaSize];
}

const float mean_temp = 22.0;
const float std_temp = 2.0;
const float mean_humid = 65.0;
const float std_humid = 10.0;

const char* temp_labels[] = {"froid", "ambiant", "chaud"};
const char* humid_labels[] = {"sec", "confortable", "humide"};

unsigned long lastReadTime = 0;
const unsigned long readInterval = 2000; // Intervalle minimal entre les lectures (2 secondes)

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  static tflite::MicroErrorReporter micro_error_reporter;
  error_reporter = &micro_error_reporter;

  model_temp = tflite::GetModel(model_temp);
  model_humid = tflite::GetModel(model_humid);

  static tflite::AllOpsResolver resolver;

  static tflite::MicroInterpreter static_interpreter_temp(
      model_temp, resolver, tensor_arena, kTensorArenaSize, error_reporter);
  interpreter_temp = &static_interpreter_temp;

  static tflite::MicroInterpreter static_interpreter_humid(
      model_humid, resolver, tensor_arena, kTensorArenaSize, error_reporter);
  interpreter_humid = &static_interpreter_humid;

  TfLiteStatus allocate_status_temp = interpreter_temp->AllocateTensors();
  TfLiteStatus allocate_status_humid = interpreter_humid->AllocateTensors();

  if (allocate_status_temp != kTfLiteOk || allocate_status_humid != kTfLiteOk) {
    Serial.println("AllocateTensors() failed");
    return;
  }

  input_temp = interpreter_temp->input(0);
  input_humid = interpreter_humid->input(0);

  Serial.println("Setup completed. Starting real-time predictions...");
}

void makePrediction(float temperature, float humidity) {
  float temp_normalized = (temperature - mean_temp) / std_temp;
  float humid_normalized = (humidity - mean_humid) / std_humid;

  input_temp->data.f[0] = temp_normalized;
  input_temp->data.f[1] = humid_normalized;
  input_humid->data.f[0] = temp_normalized;
  input_humid->data.f[1] = humid_normalized;

  TfLiteStatus invoke_status_temp = interpreter_temp->Invoke();
  TfLiteStatus invoke_status_humid = interpreter_humid->Invoke();

  if (invoke_status_temp != kTfLiteOk || invoke_status_humid != kTfLiteOk) {
    Serial.println("Invoke failed");
    return;
  }

  TfLiteTensor* output_temp = interpreter_temp->output(0);
  TfLiteTensor* output_humid = interpreter_humid->output(0);

  int temp_class = std::distance(output_temp->data.f, std::max_element(output_temp->data.f, output_temp->data.f + 3));
  int humid_class = std::distance(output_humid->data.f, std::max_element(output_humid->data.f, output_humid->data.f + 3));

  Serial.print("Température: ");
  Serial.print(temperature);
  Serial.print("°C, Classe: ");
  Serial.println(temp_labels[temp_class]);

  Serial.print("Humidité: ");
  Serial.print(humidity);
  Serial.print("%, Classe: ");
  Serial.println(humid_labels[humid_class]);

  Serial.println("--------------------");
}

void loop() {
  unsigned long currentTime = millis();
  
  // Vérifier si suffisamment de temps s'est écoulé depuis la dernière lecture
  if (currentTime - lastReadTime >= readInterval) {
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    if (!isnan(humidity) && !isnan(temperature)) {
      makePrediction(temperature, humidity);
      lastReadTime = currentTime;
    } else {
      Serial.println("Échec de lecture du capteur DHT22!");
    }
  }

  // Ici, vous pouvez ajouter d'autres tâches non bloquantes si nécessaire
}
