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

- GUI built with `customtkinter` for a responsive, modern interface
- Real-time performance metrics and logging panel
- Asynchronous request engine using `asyncio` and `aiohttp`
- Multiple HTTP method support:
  - `GET`, `POST`, `PUT`, `DELETE`
- Configurable load profiles:
  - Constant
  - Ramp Up
  - Pulse
  - Random
- Live log panel with timestamped request feedback
- Retry logic with adjustable:
  - Retry count
  - Retry delay (seconds)
- Adjustable request delay between each thread
- Support for:
  - Custom HTTP headers (JSON input)
  - Cookie injection (JSON input)
- Request body payload generator
  - Customizable payload size in bytes
- Request timeout configuration
- Thread pool executor integration for background management
- Percentile response time tracking:
  - P50, P75, P90, P95, P99
- Success vs. error tracking
  - Error type aggregation and count
- Appearance customization:
  - Light/Dark mode
  - Color theme selection (blue, green, dark-blue)
  - Adjustable font size
  - Window opacity (transparency)

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
2. Select HTTP method.
3. Choose number of threads (1–1000).
4. Set request delay in seconds (e.g., `0.1`).
5. Define payload size in bytes (e.g., `5000000`).
6. Set request timeout in seconds.
7. Select a load profile type.
8. Optionally input custom headers and cookies as JSON.
9. Choose retry count and delay.
10. Tune connection settings:
    - Pool size
    - Keep-alive timeout
11. Configure UI appearance:
    - Theme mode
    - Font size
    - Opacity
12. Click **Start Test** to begin.
13. View live results in **Metrics** and **Log** tabs.
14. Click **Stop Test** to end the run.

## Metrics Dashboard

Displays the following:

- Average response time (ms)
- Requests per second
- Success rate (%)
- Total requests
- Number of successful and failed responses
- Response time percentiles:

```
P50: 123.45 ms
P75: 234.56 ms
P90: 345.67 ms
P95: 456.78 ms
P99: 567.89 ms
```

- Error breakdown by type and count

## Advanced Options

- **Custom Headers**  
  JSON-formatted key-value input for custom headers  
  Example:
  ```
  {
    "Authorization": "Bearer token",
    "User-Agent": "CustomClient/1.0"
  }
  ```

- **Custom Cookies**  
  JSON-formatted cookies to include in each request

- **Connection Pool Settings**
  - Max pool size (default: 100)
  - Keep-alive timeout (default: 300 seconds)

- **Retry Logic**
  - Retry attempts (default: 3)
  - Delay between retries (default: 1.0 second)

- **UI Configuration**
  - Theme (dark/light)
  - Color scheme (blue, green, dark-blue)
  - Font size
  - Window transparency

## Planned Features

- [ ] Export metrics to CSV or JSON
- [ ] Save/load test configurations
- [ ] Authentication header presets
- [ ] CLI interface for headless usage
- [ ] Response body content analysis
- [ ] Graphical visualizations (charts, graphs)

