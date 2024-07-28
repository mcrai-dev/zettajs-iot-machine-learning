  // server.js
  const zetta = require('zetta');
  const express = require('express');
  const bodyParser = require('body-parser');
  const ESP32Controller = require('./Controller/ESP32Controller');
  const { appendToCSV } = require('./components/data_insertion');
  
  const app = express();
  app.use(bodyParser.json());
  
  const IP_ADDRESS = '10.42.0.1';
  const PORT = 3000;
  
  // Endpoint pour recevoir les données du capteur
  app.post('/data', (req, res) => {
    const { timestamp, temperature, humidity , temperature_class, humidity_class } = req.body;

    if (timestamp && temperature !== undefined && humidity !== undefined ) {
      appendToCSV(timestamp, temperature, temperature_class , humidity, humidity_class);
      console.log('Données reçues :', req.body);
      res.status(200).send('Données reçues avec succès');

    } else {
      res.status(400).send('Données non valides');
      
    }
  });
  
  function startServers() {
    // Démarrer le serveur Express.js
    app.listen(PORT, IP_ADDRESS, () => {
      console.log(`Express server is running on http://${IP_ADDRESS}:${PORT}`);
    });
  
    // Démarrer le serveur Zetta.js
    zetta()
      .name('Humidity | Temperature Server')
      .use(ESP32Controller)
      .listen(0, () => {
        console.log('Zetta is running.');
      });
  }
  
  startServers();
  
