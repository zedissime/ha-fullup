# Fullup Integration for Home Assistant

This integration allows you to monitor your Fullup fuel tank sensors in Home Assistant.

## Features

- Monitor fuel level in your tanks
- Track temperature
- Battery level monitoring
- Historical data tracking
- Multiple tanks support

## Installation

### HACS Installation

1. Open HACS
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add the URL of your repository
6. Select "Integration" as the category
7. Click "Add"

### Manual Installation

1. Copy the `fullup` folder to your `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings -> Devices & Services
2. Click "Add Integration"
3. Search for "Fullup"
4. Enter your Fullup credentials

## Available Sensors

- Current Volume (L)
- Fill Level (%)
- Temperature (°C)
- Battery Level (V)
- Days Left
- Last Measure Date
- Last Connection Date
- Total Volume (L)

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/zedissime/fullup/issues).
