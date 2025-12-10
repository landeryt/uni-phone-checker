const express = require('express');
const { readFile } = require('fs').promises;

const app = express();

// Serve all static files from current directory
app.use(express.static('./'));

app.get('/', async (request, response) => {
    response.send(await readFile('./index.html', 'utf8'));
});

const port = process.env.PORT || 9000; 

app.listen(port, () => {
    console.log(`Running on http://localhost:${port}`);
});