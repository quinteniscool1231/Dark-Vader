# Dark Vader Pro

> A powerful GUI-based HTTP stress testing tool built with Python and `customtkinter`.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Metrics Dashboard](#metrics-dashboard)
- [Advanced Options](#advanced-options)
- [Planned Features](#planned-features)

## Features

- GUI built with `customtkinter`
- Real-time performance monitoring
- Supports `GET`, `POST`, `PUT`, `DELETE`
- Load profiles: Constant, Ramp Up, Pulse, Random
- Custom headers and cookies support
- Retry logic with delay
- Connection pool and keep-alive settings
- Configurable UI: theme, font, opacity

## Installation

### 1. Clone the repository

```
git clone https://github.com/yourusername/dark-vader-pro.git
cd dark-vader-pro
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

Using `requirements.txt`:

```
pip install -r requirements.txt
```

Or manually:

```
pip install customtkinter aiohttp numpy
```

## Usage

To run the app:

```
python main.py
```

### Steps:

1. Enter the URL to test.
2. Select request method (GET, POST, etc.).
3. Configure thread count, delay, payload, timeout, etc.
4. Add optional headers or cookies in JSON format.
5. Select a load profile.
6. Click "Start Test".
7. View real-time metrics in the Metrics tab.

## Metrics Dashboard

Displays the following:

- Average response time (ms)
- Requests per second
- Success rate (%)
- Total requests and errors
- Response time percentiles:

```
P50: 123.45 ms
P75: 234.56 ms
P90: 345.67 ms
P95: 456.78 ms
P99: 567.89 ms
```

- Error breakdown by type

## Advanced Options

- Custom headers and cookies (JSON format)
- Connection pool size
- Keep-alive timeout
- Retry count and delay
- Appearance:
  - Theme: dark or light
  - Font size
  - Window opacity

## Planned Features

- [ ] Export metrics to CSV or JSON
- [ ] Save/load configurations
- [ ] Authentication header presets
- [ ] CLI support

