# Fullup Integration for Home Assistant

This integration allows you to monitor your [Fullup](https://fullup.io/) fuel tank sensors in Home Assistant.

## What is Fullup?

[Fullup](https://fullup.io/) is a smart fuel tank monitoring system that helps you track fuel levels in your heating oil, diesel, or other liquid storage tanks. The system consists of a wireless sensor that attaches to your tank and connects to the Fullup cloud service, providing real-time monitoring of your fuel levels.

## What does this integration do?

This integration connects your Fullup sensors to Home Assistant, allowing you to:

- Monitor fuel levels in real-time
- Get alerts when fuel levels are low
- Track fuel consumption patterns
- Monitor tank temperature to prevent freezing
- Keep track of battery levels in your Fullup sensors
- View historical data and consumption trends
- Manage multiple tanks from a single dashboard

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
