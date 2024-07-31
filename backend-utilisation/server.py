from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
# Configurer CORS pour toutes les routes
CORS(app, 
     resources={r"/*": {"origins": "http://localhost:3000"}},
     supports_credentials=True
     )


# Configurer SocketIO
socketio = SocketIO(app,
                    cors_allowed_origins="http://localhost:3000",
                    async_mode='threading'
                    )

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on_error()
def error_handler(e):
        print('An error has occured: ' +str(e) )


@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    temp_class = data.get('temp_class')
    humid_class = data.get('humid_class')

    print(f"Reçu - Température: {temperature}°C, Humidité: {humidity}%")
    print(f"Classe Température: {temp_class}, Classe Humidité: {humid_class}")

    # Envoyer les données aux clients connectés via WebSocket
    socketio.emit('weather_update', data)

    return jsonify({'status': 'success', 'message': 'Données reçues avec succès'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
