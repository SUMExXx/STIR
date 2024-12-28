document.getElementById('runScriptButton').addEventListener('click', async function(event) {
    event.preventDefault();

    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = 'Running script... Please wait.';

    try {
        // Simulate an API call to fetch the data
        const response = await fetch('http://172.31.18.56:8000/run', {
                method: 'POST',  // Specify POST method
                headers: {
                'Content-Type': 'application/json',  // Specify that we're sending JSON data
                },
                body: JSON.stringify({}),  // Send an empty JSON object
        }); // Replace with your backend endpoint
        if (!response.ok) {
            throw new Error('Failed to fetch data.');
        }
        const data = await response.json();

        // Build the output
        const dateTime = data.dateTime;
        const ipAddress = data.ipAddress;
        const trend1 = data.trend1;
        const trend2 = data.trend2;
        const trend3 = data.trend3;
        const trend4 = data.trend4;
        const trends = [trend1, trend2, trend3, trend4];
        const recordJson = JSON.stringify(data);

        const trendsHtml = trends.map((trend, index) => `<li>${trend}</li>`).join('');

        outputDiv.innerHTML = `
            <p>These are the most happening topics as on ${dateTime}</p>
            <ul>${trendsHtml}</ul>
            <p>The IP address used for this query was ${ipAddress}.</p>
            <p>Here’s a JSON extract of this record from the MongoDB:</p>
            <p>${recordJson}</p>
            <a href="#" class="button" id="runAgainButton">Click here to run the query again</a>
        `;

        // Reattach event listener for the "Run Again" button
        document.getElementById('runAgainButton').addEventListener('click', async function(event) {
            document.getElementById('runScriptButton').click();
        });
    } catch (error) {
        outputDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});