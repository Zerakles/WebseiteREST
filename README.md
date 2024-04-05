# WebsiteRest Project

## Overview
WebsiteRest is a project aimed at monitoring and controlling temperature using Raspberry Pi devices interconnected through a RESTful architecture. The project consists of several components:

1. **Temperature Sender**: A Raspberry Pi equipped with temperature sensors collects temperature data and sends it to another Raspberry Pi through a RESTful API.

2. **Temperature Receiver**: Another Raspberry Pi acts as a receiver, accepting temperature data from the sender. If the received temperature exceeds a predefined threshold (28°C in this case), the receiver triggers a fan to cool down the environment.

3. **Statistics Website**: A web application displays temperature data in graphical form. Additionally, it indicates whether the fan connected to the receiving Pi is currently enabled.

## Features
- Collects temperature data using Raspberry Pi.
- Implements RESTful communication between Raspberry Pi devices.
- Automatically activates a fan if the temperature exceeds a specified threshold.
- Provides a web interface to visualize temperature data and fan status.

## Usage
1. Temperature data will be sent from the sender Pi to the receiver Pi automatically.
2. The receiver Pi monitors the incoming temperature data and activates the fan if the temperature exceeds 28°C.
3. Access the statistics website to view temperature data in graphical form and check the status of the fan.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
Special thanks to the contributors and the open-source community for their valuable contributions and support.
