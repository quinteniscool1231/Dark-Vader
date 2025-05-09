# Dark Vader

> A simple and powerful GUI-based HTTP stress testing tool built with Python and `customtkinter`.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Metrics Dashboard](#metrics-dashboard)
- [Planned Features](#planned-features)

## Features

- User-friendly GUI built with `customtkinter`
- Live logging of HTTP request results with timestamps
- Asynchronous request handling using `aiohttp` and `asyncio`
- Highly customizable test parameters:
  - Target URL
  - HTTP method: `GET`, `POST`, `PUT`, `DELETE`
  - Number of threads (1–1000)
  - Delay between requests
  - Request timeout (in seconds)
  - Payload size (in bytes)
- Live performance dashboard:
  - Requests per second
  - Average response time
  - Success rate
  - Error count
- Appearance configuration:
  - Theme mode (light / dark)
  - Color theme (blue, green, dark-blue)
  - Adjustable font size
  - Adjustable window opacity

## Installation

### 1. Clone the repository

```
git clone https://github.com/quinteniscool1231/Dark-Vader.git
cd Dark-Vader
```

### 2. Install dependencies

```
pip install customtkinter aiohttp
```

## Usage

To launch the GUI:

```
python main.py
```

### Configuration Steps

1. Enter the **target URL**
2. Select the **HTTP method** (`GET`, `POST`, `PUT`, `DELETE`)
3. Set the **number of threads**
4. Define **request delay** (e.g., `0.1`)
5. Set **payload size** (e.g., `5000000`)
6. Specify **timeout** duration (in seconds)
7. Optionally configure:
   - UI theme and color
   - Font size
   - Window opacity
8. Click **Start Test** to begin
9. Monitor logs and metrics in real time
10. Click **Stop Test** to end

## Metrics Dashboard

Real-time display includes:

- **Requests/sec** – How many requests are processed per second
- **Average Response Time** – In milliseconds
- **Success Rate** – Percentage of successful responses
- **Total Requests** – Combined success and failure count
- **Successes / Errors** – Raw numbers of each

Example:

```
Requests/sec: 142.85
Avg Response Time: 198.77ms
Success Rate: 98.1%
Total Requests: 1500
Successes: 1472
Errors: 28
```

## Planned Features

- [ ] Export metrics to file (CSV or JSON)
- [ ] Header and cookie customization
- [ ] CLI (command-line interface) support
- [ ] Save/load test configurations
- [ ] Add graphs and charts to the metrics tab
