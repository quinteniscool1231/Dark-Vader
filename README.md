# Dark Vader

> A simple and effective GUI-based HTTP stress testing tool built with Python and `customtkinter`.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Metrics Dashboard](#metrics-dashboard)
- [Planned Features](#planned-features)

## Features

- GUI interface built with `customtkinter`
- Live logging of HTTP requests and errors
- Asynchronous stress testing using `aiohttp` and `asyncio`
- Customizable:
  - Target URL
  - HTTP method (`GET`, `POST`, `PUT`, `DELETE`)
  - Number of threads (1–1000)
  - Delay between requests
  - Request timeout (in seconds)
  - Payload size (in bytes)
- Live performance metrics display:
  - Requests per second
  - Average response time
  - Success rate
  - Error count
- Appearance customization:
  - Theme (light/dark)
  - Color theme (blue, green, dark-blue)
  - Font size
  - Window opacity

## Installation

### 1. Clone the repository

```
git clone https://github.com/quinteniscool1231/Dark-Vader.git
cd Dark-Vader
```

### 2. Create a virtual environment (optional)

```
python -m venv venv
source venv/bin/activate
```

On Windows:

```
venv\Scripts\activate
```

### 3. Install dependencies

```
pip install customtkinter aiohttp
```

## Usage

To start the GUI:

```
python main.py
```

### Configuration Steps

1. Enter the target **URL**
2. Choose request method (`GET`, `POST`, etc.)
3. Set the number of threads
4. Enter delay between requests (e.g. `0.1`)
5. Choose payload size (e.g. `5000000`)
6. Set timeout (in seconds)
7. Optionally, configure:
   - Theme and color
   - Font size
   - Opacity
8. Click **Start Test**
9. Monitor real-time logs and metrics
10. Click **Stop Test** to finish

## Metrics Dashboard

Displays the following real-time metrics:

- `Requests/sec` – Throughput of the test
- `Avg Response Time` – In milliseconds
- `Success Rate` – Percentage of successful requests
- `Total Requests` – Overall request count
- `Successes` and `Errors` – Breakdown

Example output:

```
Requests/sec: 142.85
Avg Response Time: 198.77ms
Success Rate: 98.1%
Total Requests: 1500
Successes: 1472
Errors: 28
```

## Planned Features

- [ ] Export metrics to file
- [ ] Header and cookie customization
- [ ] CLI mode support
- [ ] Save/load test profiles
- [ ] Add graphs and charts to metrics tab
