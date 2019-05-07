# Rides 4 Life

## Overview

This site allows a woman to text a service and a trained driver will come to take her to the hospital. Also, this site allows drivers to sign up to take women to hospitals.

## Tech Stack

```text
1. Python/Django
2. PostgreSQL
3. React
4. RapidSMS
```

## API Endpoints

### Authentication

| Method | Endpoint       | Description                                                                                                                                                                        |
| ------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| POST   | api-token-auth | Generates an auth token. The `body` should be `username` and `password` Returns an object `{"token": "hex"}` To access protected routes, use header `"Authorization", "Token hex"` |

### Drivers

| Method | Endpoint     | Description                                                                                                                                                                                                             |
| ------ | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| POST   | /api/drivers | Creates a `driver` user using the information sent inside the `body` of the request. The body should include `name` (str), `phone` (str), `homebase` (str), `latitude` (float), `longitude` (float), `available` (bool) |
| GET    | /api/drivers | Shows all drivers. Returns an array [{"id":"...", "name":"...", "phone":"...", "latitude":"...", "longitude":"...", "available":"bool"}, {...}]                                                                         |

### Mothers

| Method | Endpoint     | Description                                                                                                                                                                                        |
| ------ | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| POST   | /api/mothers | Creates a `mother` user using the information sent inside the `body` of the request. The body should include `name` (str), `phone` (str), `village` (str), `latitude` (float), `longitude` (float) |
| GET    | /api/mothers | Shows all mothers. Returns an array [{"id":"...", "name":"...", "phone":"...", "village":"...", "latitude":"...", "longitude":"..."}, {...}]                                                       |

### Villages

| Method | Endpoint        | Description                                                                                                 |
| ------ | --------------- | ----------------------------------------------------------------------------------------------------------- |
| GET    | /api/villages   | Shows all villages. Returns an array [{"id":".","name":"...","latitude":"...","longitude":"..."}, {...}]    |
| GET    | /api/village/id | Returns the village specified by id as a JSON object {"name": "...", "latitude": "...", "longitude": "..."} |