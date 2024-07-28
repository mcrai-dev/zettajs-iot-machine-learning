const zetta = require('zetta');

/**
+ * Creates a new instance of the ESP32Device class.
+ *
+ * @constructor
+ */

function DHT22Module() {
  zetta.Device.call(this); 
  this.temperature = 0;
  this.humidity = 0;
}

/**
+ * Inherits from the zetta.Device class.
+ */
DHT22Module.prototype = Object.create(zetta.Device.prototype);
DHT22Module.prototype.constructor = DHT22Module;

/**
+ * Initializes the ESP32Device with the given configuration.
+ *
+ * @param {Object} config - The configuration object for the device.
+ * @return {void} This function does not return anything.
+ */

DHT22Module.prototype.init = function(config) {
  config
    .name('Digital Humidity and Temperature Sensor')
    .type('DHT22')
    .state('ready')
    .monitor('temperature')
    .monitor('humidity');

  this.on('updateSensorData', this.onUpdateSensorData.bind(this));
};

/**
+ * Updates the temperature and humidity properties of the ESP32MCUDevice object with the values from the given data object.
+ *
+ * @param {Object} data - The data object containing the new temperature and humidity values.
+ * @return {void} This function does not return anything.
+ */
DHT22Module.prototype.onUpdateSensorData = function(data) {
  this.temperature = data.temperature;
  this.humidity = data.humidity;
  console.log('Updated sensor data:', data);
};

module.exports = DHT22Module;
