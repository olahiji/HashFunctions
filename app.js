const express = require('express');
const getLocations = require('restaurant-location-search-api');
const app = express();
const fs = require('fs');
const PORT = 3000;

// Endpoint to get the nearest McDonald's location
app.get('/nearest-mcdonalds', async (req, res) => {
    const { latitude, longitude } = req.query;

    // Validate latitude and longitude
    if (!latitude || !longitude) {
        return res.status(400).json({ error: 'Latitude and longitude are required' });
    }

    const lat = parseFloat(latitude);
    const long = parseFloat(longitude);

    if (isNaN(lat) || isNaN(long)) {
        return res.status(400).json({ error: 'Latitude and longitude must be valid numbers' });
    }

    if (lat < -90 || lat > 90 || long < -180 || long > 180) {
        return res.status(400).json({ error: 'Latitude must be between -90 and 90, and longitude must be between -180 and 180' });
    }

    try {
        const location = await getLocations('mcdonalds', { lat, long }, 100, 1, true);
        console.log('Fetched location data:', JSON.stringify(location, null, 2));
        const nearbyStores = location.features.map(feature => ({
            storeNumber: feature.properties.identifierValue, // Store Identifier
            storeStatus: feature.properties.openstatus,
            phoneNumber: feature.properties.telephone,
            addressLine1: feature.properties.addressLine1,
            addressLine3: feature.properties.addressLine3,
            subDivision: feature.properties.subDivision,
            postCode: feature.properties.postcode,
            geoPoint: {
                latitude: feature.geometry.coordinates[1], // Latitude is the second coordinate
                longitude: feature.geometry.coordinates[0] // Longitude is the first coordinate
            },
            formattedDistance: "N/A", // You can set this if available
        }));

        res.json({ nearByStores: nearbyStores });
    } catch (error) {
        console.error(error); // Log the error for debugging
        res.status(500).json({ error: 'Failed to fetch nearest McDonald\'s location' });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});