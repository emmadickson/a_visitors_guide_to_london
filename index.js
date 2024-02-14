// Importing required modules
const express = require('express');
const path = require('path');

// Creating an Express application
const app = express();
var port = process.env.PORT || 3000;

// Set the static folder for serving static files like index.html
app.use(express.static(path.join(__dirname, 'public')));

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
