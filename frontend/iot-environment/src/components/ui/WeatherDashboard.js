import React, { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Droplets, Thermometer, Sun, Cloud, CloudRain, Info, AlertTriangle, Moon, Menu } from 'lucide-react';
import io from 'socket.io-client';

const socket = io('http://10.42.0.1:5000', {
  transports: ['websocket', 'polling'],
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
  timeout: 10000
});

const WeatherDashboard = () => {
  const [weatherData, setWeatherData] = useState({
    temperature: 0,
    humidity: 0,
    temp_class: '',
    humid_class: '',
    env_state: ''
  });
  const [showInfo, setShowInfo] = useState(false);
  const [history, setHistory] = useState([]);
  const [darkMode, setDarkMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    socket.on('weather_update', (data) => {
      setWeatherData(data);
      setHistory(prev => [...prev, { ...data, time: new Date().toLocaleTimeString() }].slice(-20));
    });

    return () => socket.off('weather_update');
  }, []);

  const WeatherIcon = ({ className }) => {
    switch(weatherData.temp_class) {
      case 'chaud': return <Sun className={className} />;
      case 'froid': return <CloudRain className={className} />;
      default: return <Cloud className={className} />;
    }
  };

  const getColorClass = (value, type) => {
    if (type === 'temp') {
      if (value < 10) return darkMode ? 'text-blue-400' : 'text-blue-500';
      if (value > 30) return darkMode ? 'text-red-400' : 'text-red-500';
      return darkMode ? 'text-green-400' : 'text-green-500';
    } else {
      if (value < 30) return darkMode ? 'text-yellow-400' : 'text-yellow-500';
      if (value > 70) return darkMode ? 'text-blue-400' : 'text-blue-500';
      return darkMode ? 'text-green-400' : 'text-green-500';
    }
  };

  const generateEnvironmentState = () => {
    const lastHour = history.slice(-6);
    const avgTemp = lastHour.reduce((sum, data) => sum + data.temperature, 0) / lastHour.length;
    const avgHumidity = lastHour.reduce((sum, data) => sum + data.humidity, 0) / lastHour.length;
    
    let state = "Conditions actuelles : ";
    
    if (avgTemp > 25 && avgHumidity > 60) {
      state += "Chaud et humide. Risque de sensation d'inconfort.";
    } else if (avgTemp < 10 && avgHumidity < 30) {
      state += "Froid et sec. Pensez à vous hydrater et à protéger votre peau.";
    } else if (avgTemp > 30) {
      state += "Très chaud. Restez hydraté et évitez l'exposition prolongée au soleil.";
    } else if (avgHumidity > 80) {
      state += "Très humide. Attention aux moisissures et à la qualité de l'air intérieur.";
    } else {
      state += "Conditions confortables. Profitez-en !";
    }
    
    return state;
  };

  return (
    <div className={`${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-800'} min-h-screen`}>
      {/* Header */}
      <header className={`${darkMode ? 'bg-gray-800' : 'bg-white'} shadow-md p-4 flex justify-between items-center`}>
        <div className="flex items-center">
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="mr-4">
            <Menu size={24} />
          </button>
          <h1 className="text-2xl font-bold">Tableau de Bord Météo</h1>
        </div>
        <button
          onClick={() => setDarkMode(!darkMode)}
          className={`p-2 rounded-full ${darkMode ? 'bg-yellow-400 text-gray-900' : 'bg-gray-800 text-yellow-400'}`}
        >
          {darkMode ? <Sun size={24} /> : <Moon size={24} />}
        </button>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className={`${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} ${darkMode ? 'bg-gray-800' : 'bg-white'} w-64 fixed left-0 h-full shadow-lg transition-transform duration-300 ease-in-out z-20`}>
          <nav className="p-4">
            <ul>
              <li className="mb-2">
                <a href="#" className="block p-2 rounded hover:bg-gray-700">Accueil</a>
              </li>
              <li className="mb-2">
                <a href="#" className="block p-2 rounded hover:bg-gray-700">Historique</a>
              </li>
              <li className="mb-2">
                <a href="#" className="block p-2 rounded hover:bg-gray-700">Paramètres</a>
              </li>
            </ul>
          </nav>
        </aside>

        {/* Main Content */}
        <main className={`flex-1 p-4 ${sidebarOpen ? 'ml-64' : ''} transition-margin duration-300 ease-in-out`}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} shadow-lg rounded-lg p-6 flex items-center justify-between`}>
              <div>
                <h2 className="text-xl font-semibold mb-2">Température</h2>
                <p className={`text-4xl font-bold ${getColorClass(weatherData.temperature, 'temp')}`}>
                  {weatherData.temperature}°C
                </p>
                <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'} mt-1`}>{weatherData.temp_class}</p>
              </div>
              <Thermometer className={`w-16 h-16 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`} />
            </div>
            
            <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} shadow-lg rounded-lg p-6 flex items-center justify-between`}>
              <div>
                <h2 className="text-xl font-semibold mb-2">Humidité</h2>
                <p className={`text-4xl font-bold ${getColorClass(weatherData.humidity, 'humid')}`}>
                  {weatherData.humidity}%
                </p>
                <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'} mt-1`}>{weatherData.humid_class}</p>
              </div>
              <Droplets className={`w-16 h-16 ${darkMode ? 'text-gray-500' : 'text-gray-400'}`} />
            </div>
          </div>

          <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} shadow-lg rounded-lg p-6 mb-8`}>
            <h3 className="text-xl font-semibold mb-4">Historique des données</h3>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={history}>
                <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? '#4a5568' : '#e2e8f0'} />
                <XAxis dataKey="time" stroke={darkMode ? '#a0aec0' : '#4a5568'} />
                <YAxis yAxisId="left" stroke={darkMode ? '#a0aec0' : '#4a5568'} />
                <YAxis yAxisId="right" orientation="right" stroke={darkMode ? '#a0aec0' : '#4a5568'} />
                <Tooltip contentStyle={{ backgroundColor: darkMode ? '#2d3748' : '#ffffff', borderColor: darkMode ? '#4a5568' : '#e2e8f0' }} />
                <Area yAxisId="left" type="monotone" dataKey="temperature" stroke="#8884d8" fill="#8884d8" fillOpacity={0.3} name="Température (°C)" />
                <Area yAxisId="right" type="monotone" dataKey="humidity" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.3} name="Humidité (%)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} shadow-lg rounded-lg p-6`}>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-semibold">État de l'environnement</h3>
              <button 
                onClick={() => setShowInfo(!showInfo)}
                className={`${darkMode ? 'bg-blue-600 hover:bg-blue-700' : 'bg-blue-500 hover:bg-blue-600'} text-white px-4 py-2 rounded-full transition-colors flex items-center`}
              >
                <Info className="w-5 h-5 mr-2" />
                {showInfo ? 'Masquer' : 'Afficher'}
              </button>
            </div>
            {showInfo && (
              <div className={`mt-4 p-4 ${darkMode ? 'bg-gray-700' : 'bg-gray-100'} rounded-lg`}>
                <div className="flex items-start">
                  <AlertTriangle className="w-6 h-6 text-yellow-500 mr-3 flex-shrink-0 mt-1" />
                  <p>{generateEnvironmentState()}</p>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
};

export default WeatherDashboard;