const fs = require('fs');
const path = require('path');

const CSV_FILE_PATH = path.join(__dirname, '../data.csv');

// Vérifiez si le fichier CSV existe et ajoutez les en-têtes s'il est nouveau
if (!fs.existsSync(CSV_FILE_PATH)) {
  fs.writeFileSync(CSV_FILE_PATH, 'timestamp,temperature,temperature_class,humidity,humidity_class\n');
}

// Fonction pour ajouter une ligne au fichier CSV
function appendToCSV(timestamp, temperature, temperatureClass, humidity,  humidityClass) {
  const line = `${timestamp},${temperature},${temperatureClass},${humidity},${humidityClass}\n`;
  fs.appendFile(CSV_FILE_PATH, line, (err) => {
    if (err) {
      console.error('Erreur lors de l\'écriture dans le fichier CSV:', err);
    }
  });
}

module.exports = { appendToCSV };
