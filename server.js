const express = require('express');
const path = require('path');

const app = express();
const port = 443;

// Serve static files (index.html, script.js, styles.css)
app.use(express.static(path.join(__dirname)));

// Route to serve the index.html file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
