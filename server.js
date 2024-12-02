const express = require('express');
const fs = require('fs');
const path = require('path');
const JSONStream = require('JSONStream');

const app = express();
app.use(express.static(path.join(__dirname, 'public')));

app.get('/api/job/:index', (req, res) => {
    const { index } = req.params;
    const targetIndex = parseInt(index); // Convert index to integer
    let currentIndex = 0; // To track the index of streamed objects

    const parser = JSONStream.parse('*');

    fs.createReadStream(path.join(__dirname, 'public', 'features.json'))
        .pipe(parser)
        .on('data', job => {
            if (currentIndex === targetIndex) {
                parser.pause(); // Found the job at the specified index, pause the stream
                res.json(job);
                parser.end();
            }
            currentIndex++; // Increment the current index
        })
        .on('end', () => {
            if (currentIndex <= targetIndex) { // Check if the end was reached before finding the index
                res.status(404).send('Job not found.');
            }
        })
        .on('error', error => {
            console.error('Stream error:', error);
            res.status(500).send('Error processing data file.');
        });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
