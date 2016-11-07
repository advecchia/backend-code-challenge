# API Description
The challenge ask to development of an endpoint that can capture emissions only, I delivered one extra endpoint to get the existing emissions, also one to get emissions for some specific vehicle identifier and another for a specific vehicle type. See below the information about API endpoints access, payload and returned data.

### <a id="toc"></a>Table of Contents 
 * [Go back to home](https://github.com/advecchia/backend-code-challenge/blob/master/README.md)  
 * [Home description](#home-description)  
 * [Post Emission](#post-emission)  
 * [Get Emissions](#get-emissions)  
 * [Get Emissions By Vehicle ID](#get-emissions-by-vehicle-id)  
 * [Get Emissions By Vehicle Type](#get-emissions-by-vehicle-type)  

## Home description <a id="home-description"></a> [^](#toc "To top")
Website Home showing the project README.

| API Endpoint  | HTTP Method   | Content-Type
| ------------- |:-------------: | -------------
| /      | GET | text/html  

## Post Emission <a id="post-emission"></a> [^](#toc "To top")  
Sends an emission body (see below) and returns the same emission. **timestamp** is not an obligatory field, it is added if inexistent.  

| API Endpoint  | HTTP Method   | Content-Type
| ------------- |:-------------: | -------------
| /api/v1/emissions       | POST | application/json 

Body:
``` 
{
  "vehicleId":"UUID",
  "vehicleType":"taxi or bus or tram or train",
  "latitude":<float between -90/+90>,
  "longitude":<float between -180/+180>,
  "heading":<integer between 0/359>,
  "timestamp":<unix timestamp format>
}
```

## Get Emissions <a id="get-emissions"></a> [^](#toc "To top")
Retrieves a list of existing emissions, **offset** and **limit** query parameters can be used for pagination.

| API Endpoint  | HTTP Method   | Content-Type
| ------------- |:-------------: | -------------
| /api/v1/emissions   | GET | application/json  

Response example:
``` 
{
  "data": [
    {
      "heading": 0, 
      "latitude": 52.635484, 
      "longitude": -4.255552, 
      "timestamp": 1478375156.41285, 
      "vehicleId": "001244bc-b4fd-479e-a1a7-88f197c65910", 
      "vehicleType": "bus"
    }, 
    {
      "heading": 180, 
      "latitude": 53.126944, 
      "longitude": -3.441342, 
      "timestamp": 1478375445.022973, 
      "vehicleId": "006ed6ec-e25e-48ea-af2f-064826542d0f", 
      "vehicleType": "bus"
    }, 
    {
      "heading": 0, 
      "latitude": 53.034853, 
      "longitude": -3.59391, 
      "timestamp": 1478375416.713166, 
      "vehicleId": "00842d72-2a39-4212-a591-ad442c8a1bee", 
      "vehicleType": "taxi"
    }, 
    {
      "heading": 106, 
      "latitude": 52.77088, 
      "longitude": -3.534391, 
      "timestamp": 1478158005.821124, 
      "vehicleId": "00945f1c-b045-4d07-bfe9-6d92fe541714", 
      "vehicleType": "taxi"
    }, 
    {
      "heading": 180, 
      "latitude": 52.949376, 
      "longitude": -3.735521, 
      "timestamp": 1478375094.914598, 
      "vehicleId": "00a3bdd4-b82d-4233-bd82-dcc2344219c9", 
      "vehicleType": "taxi"
    }
  ], 
  "limit": 5, 
  "offset": 0, 
  "total": 4201
}
```

## Get Emissions By Vehicle ID <a id="get-emissions-by-vehicle-id"></a> [^](#toc "To top")
Retrieves a list of existing emissions for an existing vehicle by its identifier, **offset** and **limit** query parameters can be used for pagination.  

| API Endpoint  | HTTP Method   | Content-Type
| ------------- |:-------------: | -------------
| /api/v1/emissions/vehicles/<uuid:id> | GET | application/json  

Response example (for /api/v1/emissions/vehicles/001244bc-b4fd-479e-a1a7-88f197c65910):
``` 
{
  "data": [
    {
      "heading": 0, 
      "latitude": 52.635484, 
      "longitude": -4.255552, 
      "timestamp": 1478375156.41285, 
      "vehicleId": "001244bc-b4fd-479e-a1a7-88f197c65910", 
      "vehicleType": "bus"
    }, 
    {
      "heading": 30, 
      "latitude": 52.635584, 
      "longitude": -4.255652, 
      "timestamp": 1478375176.41285, 
      "vehicleId": "001244bc-b4fd-479e-a1a7-88f197c65910", 
      "vehicleType": "bus"
    },
    {
      "heading": 45, 
      "latitude": 52.635684, 
      "longitude": -4.255752, 
      "timestamp": 1478375196.41285, 
      "vehicleId": "001244bc-b4fd-479e-a1a7-88f197c65910", 
      "vehicleType": "bus"
    }
  ], 
  "limit": 3, 
  "offset": 0, 
  "total": 4201
}
```

## Get Emissions By Vehicle Type <a id="get-emissions-by-vehicle-type"></a> [^](#toc "To top")
Retrieves a list of existing emissions for existing vehicles by its type, **offset** and **limit** query parameters can be used for pagination.  

| API Endpoint  | HTTP Method   | Content-Type
| ------------- |:-------------: | -------------
| /api/v1/emissions/vehicles/type/<string:type> | GET | application/json  

Response example (for /api/v1/emissions/vehicles/type/taxi):
``` 
{
  "data": [
    {
      "heading": 0, 
      "latitude": 53.034853, 
      "longitude": -3.59391, 
      "timestamp": 1478375416.713166, 
      "vehicleId": "00842d72-2a39-4212-a591-ad442c8a1bee", 
      "vehicleType": "taxi"
    }, 
    {
      "heading": 106, 
      "latitude": 52.77088, 
      "longitude": -3.534391, 
      "timestamp": 1478158005.821124, 
      "vehicleId": "00945f1c-b045-4d07-bfe9-6d92fe541714", 
      "vehicleType": "taxi"
    }, 
    {
      "heading": 180, 
      "latitude": 52.949376, 
      "longitude": -3.735521, 
      "timestamp": 1478375094.914598, 
      "vehicleId": "00a3bdd4-b82d-4233-bd82-dcc2344219c9", 
      "vehicleType": "taxi"
    }
  ], 
  "limit": 3, 
  "offset": 0, 
  "total": 4201
}
```