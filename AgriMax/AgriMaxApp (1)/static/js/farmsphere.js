// Add event listeners to buttons
document.addEventListener('DOMContentLoaded', function() {
    const getRecommendationsButton = document.getElementById('get-recommendations-button');
    const evaluateSoilHealthButton = document.getElementById('evaluate-soil-health-button');
    const saveChangesButton = document.getElementById('save-changes-button');

    getRecommendationsButton.addEventListener('click', getRecommendations);
    evaluateSoilHealthButton.addEventListener('click', evaluateSoilHealth);
    saveChangesButton.addEventListener('click', saveChanges);
});

// Function to get crop recommendations
function getRecommendations() {
    const potassiumLevel = document.getElementById('potassium-level').value;
    const phosphorusLevel = document.getElementById('phosphorus-level').value;
    const nitrogenLevel = document.getElementById('nitrogen-level').value;
    const pHLevel = document.getElementById('pH-level').value;
    const temperature = document.getElementById('temperature').value;
    const rainfall = document.getElementById('rainfall').value;
    const humidity = document.getElementById('humidity').value;

    // Call API to get recommendations
    fetch('/api/recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            potassiumLevel,
            phosphorusLevel,
            nitrogenLevel,
            pHLevel,
            temperature,
            rainfall,
            humidity
        })
    })
   .then(response => response.json())
   .then(data => {
        const recommendationsResults = document.getElementById('recommendations-results');
        recommendationsResults.innerHTML = '';
        data.recommendations.forEach(recommendation => {
            const recommendationHTML = `
            <p>Crop: ${recommendation.crop}</p>
            <p>Yield: ${recommendation.yield}</p>
            <p>Soil Health: ${recommendation.soilHealth}</p>
            `;
            recommendationsResults.innerHTML += recommendationHTML;
        });
   })
   .catch(error => console.error(error));
}

// Function to evaluate soil health
function evaluateSoilHealth() {
    const desiredCrop = document.getElementById('desired-crop').value;
    const potassiumLevel = document.getElementById('potassium-level').value;
    const phosphorusLevel = document.getElementById('phosphorus-level').value;
    const nitrogenLevel = document.getElementById('nitrogen-level').value;
    const pHLevel = document.getElementById('pH-level').value;

    // Call API to evaluate soil health
    fetch('/api/soil-health', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            desiredCrop,
            potassiumLevel,
            phosphorusLevel,
            nitrogenLevel,
            pHLevel
        })
    })
    .then(response => response.json())
    .then(data => {
        const soilHealthResults = document.getElementById('soil-health-results');
        soilHealthResults.innerHTML = '';
        const soilHealthHTML = `
        <p>Soil Health: ${data.soilHealth}</p>
        <p>Recommendations: ${data.recommendations}</p>
        `;
        soilHealthResults.innerHTML = soilHealthHTML;
    })
    .catch(error => console.error(error));
}

// Function to save changes
function saveChanges() {
    const theme = document.getElementById('theme').value;

    // Call API to save changes
    fetch('/api/save-changes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            theme
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error(error));
}
