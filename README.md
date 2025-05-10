# Dark Vader

> A powerful GUI-based HTTP stress testing tool with real-time metrics and customization options, built in Python with `customtkinter`.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Main Functions](#main-functions)
- [Metrics Dashboard](#metrics-dashboard)
- [Planned Features](#planned-features)
- [License](#license)

## Features

- 🖥️ Graphical user interface (GUI) using `customtkinter`
- 🔁 Asynchronous request handling via `aiohttp` and `asyncio`
- ⚙️ Configurable test parameters:
  - URL, method (`GET`, `POST`, `PUT`, `DELETE`)
  - Threads (1–1000), delay, timeout
  - Payload size (up to 10MB)
- 📊 Real-time metrics: requests/sec, avg response time, success rate, error types
- 🎯 Load profiles: constant, ramp-up, pulse, random
- 🎨 Customizable UI: theme mode, color theme, font size, opacity
- 📁 Save/load configurations and export metrics as CSV/JSON
- 📈 Built-in histogram graph of response times

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/quinteniscool1231/Dark-Vader.git
cd Dark-Vader
```

### 2. Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> Or manually:

```bash
pip install customtkinter aiohttp numpy pandas matplotlib
```

## Usage

To launch the GUI:

```bash
python main.py
```

### Configuration Steps

1. Input **target URL**
2. Choose **HTTP method**
3. Adjust **threads**, **delay**, **timeout**, and **payload**
4. Optionally customize:
   - Load profile (e.g., ramp-up)
   - Theme, font, opacity
   - Headers, cookies, retry policy
5. Click **Start Test**
6. Monitor logs and metrics live
7. Export metrics or save configuration

## Main Functions

| Function | Description |
|---------|-------------|
| `StressTestMetrics` | Stores and calculates performance statistics including percentiles and error breakdown |
| `StressTester` | Main class that initializes UI, handles configuration, and manages request threads |
| `make_request()` | Async function that performs HTTP requests with retry and error handling |
| `worker()` | Background coroutine that repeatedly sends requests based on delay and load profile |
| `run_async_loop()` | Controls the async event loop and worker thread count |
| `export_metrics()` | Exports metrics data to `.csv` or `.json` |
| `save_config()` / `load_config()` | Saves or loads test settings from local JSON file |
| `apply_settings()` | Applies theme, font size, and opacity to GUI |
| `update_graph()` | Draws a histogram of response times using matplotlib |
| `update_metrics_display()` | Refreshes the live metrics tab continuously |

## Metrics Dashboard

Metrics panel updates every second and includes:

- **Requests/sec** – Request throughput
- **Avg Response Time** – Average time in ms
- **Success Rate** – %
- **Total Requests** – Number sent
- **Errors & Error Types** – Counted and grouped
- **Percentiles** – P50, P75, P90, P95, P99 response times

Example Output:

```
Performance Metrics:
==================
Requests/sec: 164.75
Avg Response Time: 148.21ms
Success Rate: 96.3%
Total Requests: 2457
Successes: 2366
Errors: 91

Response Time Percentiles:
=======================
P50: 141.31ms
P75: 176.90ms
P90: 224.88ms
P95: 268.34ms
P99: 390.20ms

Error Breakdown:
==============
TimeoutError: 55
ClientOSError: 24
HTTP 500: 12
```

## Planned Features

- [ ] Full CLI (command-line interface) support
- [ ] Save/load test run history
- [ ] Customizable request bodies (not just JSON)
- [ ] More advanced error visualization
- [ ] Distributed stress testing support

## License

MIT License. See the [LICENSE](LICENSE) file for full terms.
