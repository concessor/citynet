var express = require('express');
var axios = require('axios');


var router = express.Router();

// Why AXIOS
// https://medium.com/@thejasonfile/fetch-vs-axios-js-for-making-http-requests-2b261cdd3af5

module.exports = io => {

	const getApiAndEmit = async socket => {
	  try {
	    const res = await axios.get(
	      "https://api.darksky.net/forecast/326453a7139f863c15599146a608cdef/37.8267,-122.4233"
	    ); // Getting the data from DarkSky
	    console.log('tests');
	    socket.emit('FromAPI', res.data.currently.temperature); // Emitting a new message. It will be consumed by the client
	  } catch (error) {
	    console.error('Error:' + error);
	  }
	};
    
    let interval;

	io.on("connection", socket => {
	  console.log("New client connected");
	  if (interval) {
	    clearInterval(interval);
	  }
	  interval = setInterval(() => getApiAndEmit(socket), 1000);
	  socket.on("disconnect", () => {
	    console.log("Client disconnected");
	  });
	});

    return router;
}


