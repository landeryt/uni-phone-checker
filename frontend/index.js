const express = require('express');
const { readFile } = require('fs').promises;

const app = express();

app.get('/', async (request, response) => {
    // readFile('./index.html', 'utf8', (err, html) => {
    //     if (err) {
    //         response.status(500).send('Error loading index.html');
    //         return;
    //     }

        
    // });
    response.send(await readFile('./index.html', 'utf8'));
});

const port = process.env.PORT || 3000; 

app.listen(port, () => {
    console.log(`Running on port http://localhost:${port}`);
});