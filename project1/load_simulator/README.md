# Load Testing Script for Spring Boot App

This Python script simulates user interactions with the **Spring Boot 3.4.3** application by repeatedly loading the `/gallery` endpoint and scrolling to the bottom of the page. The script will be used for measuring **performance**, **resource consumption**, and **response times**.

## Features
- Sends **multiple requests** to the `/gallery` endpoint.
- Uses **Selenium** to automate a **headless browser**.
- Scrolls to the bottom of the page to simulate user interaction.
- Can be customized for different load testing scenarios.

## Requirements
Before running the script, ensure you have:
- **Python 3.8+** installed  
- **Google Chrome** installed  
- **ChromeDriver** (matching your Chrome version)  
- **Selenium** installed  
- **Docker** installed

## Installation

### Install Dependencies
1. First, install the required Python package:
```sh
pip install -r requirements.txt
```

2. Run the script which will package and deploy the app with Docker:
```sh
python -m SB_Simulator <folder-to-app> <nr-of-iterations>
``` 

The Dockerfiles can be configured with the specific platform (e.g `linux/amd64` for mac)