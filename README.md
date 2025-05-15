# Dark Vader

> A powerful GUI and CLI-based HTTP stress testing tool built with Python and `customtkinter`, designed for visibility, customization, and performance diagnostics.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage (GUI)](#usage-gui)
- [CLI Usage](#cli-usage)
- [Main Functions](#main-functions)
- [Metrics Dashboard](#metrics-dashboard)
- [Planned Features](#planned-features)
- [License](#license)

---

## Features

- 🖥️ **GUI** with `customtkinter`
- 🔁 Async request handling (`aiohttp`, `asyncio`)
- ⚙️ Full test config: URL, method, threads, delay, timeout, payload
- 🧠 **Load Profiles**: constant, ramp-up, pulse, random
- 📊 **Real-time metrics**: success rate, req/s, error types, percentiles
- 🧪 Live logs and stats dashboard
- 🎨 Appearance settings (theme, font, opacity)
- 💾 Config save/load + metrics export (JSON/CSV)
- 🧵 CLI mode with graceful exit and progress bar

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/quinteniscool1231/Dark-Vader.git
cd Dark-Vader
```

### 2. Create a Virtual Environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install customtkinter aiohttp numpy pandas matplotlib validators
```

---

## Usage (GUI)

Launch the GUI app:

```bash
python main.py
```

### Setup in GUI

1. Enter target **URL**
2. Choose HTTP **method** (`GET`, `POST`, `PUT`, etc.)
3. Set **threads**, **delay**, **payload**, **timeout**
4. Choose load profile + optional UI theme
5. Click **Start Test**
6. Monitor live logs, charts, and metrics
7. Click **Stop Test** and export results

---

## CLI Usage

Dark Vader includes a fully featured CLI for automated or headless stress testing with validation, progress bar, and metrics export.

### Run the CLI

```bash
python cli.py https://example.com \
  --threads 300 \
  --duration 60 \
  --method POST \
  --payload-size 1000000 \
  --delay 0.1 \
  --timeout 15 \
  --pool-size 200 \
  --output results/output.json
```

> Press `Ctrl+C` to stop gracefully at any time.

### CLI Arguments

| Argument          | Description                                           | Default    |
|-------------------|-------------------------------------------------------|------------|
| `url` (positional)| The target URL to test                               | *required* |
| `--threads`       | Number of concurrent threads/workers (positive int)  | `200`      |
| `--duration`      | Test duration in seconds                             | `60`       |
| `--method`        | HTTP method: `GET`, `POST`, `PUT`, etc.              | `POST`     |
| `--payload-size`  | Payload size in bytes                                | `5000000`  |
| `--delay`         | Delay between requests (seconds)                     | `0`        |
| `--timeout`       | Timeout for each request in seconds                  | `30`       |
| `--pool-size`     | Max number of open connections                       | `100`      |
| `--output`        | Path to JSON output file for metrics                 | *None*     |

### Output Example

```text
Progress: [==========----------------------------] 15/60s | Requests: 1324 | Success Rate: 98.2%
...
Test completed successfully

Performance Metrics:
==================
Requests/sec: 147.12
Avg Response Time: 189.53ms
Success Rate: 98.7%
Total Requests: 8827
Successes: 8711
Errors: 116

Response Time Percentiles:
=======================
P50: 182.34ms
P75: 210.87ms
P90: 258.67ms
P95: 315.33ms
P99: 408.98ms

Error Breakdown:
==============
TimeoutError: 65
HTTP 500: 51
```

> If `--output` is used, results are exported to JSON automatically.

---

## Main Functions

| Function                     | Purpose                                                              |
|-----------------------------|----------------------------------------------------------------------|
| `StressTestMetrics`         | Collects and summarizes performance metrics                         |
| `LoadProfile.get_thread_count()` | Calculates dynamic thread count based on profile type       |
| `make_request()` (GUI)      | Sends requests and logs responses/errors                            |
| `run_stress_test()` (CLI)   | Manages workers, async loop, metrics, and progress bar              |
| `save_config()` / `load_config()` | Stores/loads full test setups as JSON                    |
| `export_metrics()`          | Exports logs and stats to `.csv` or `.json`                         |
| `apply_settings()`          | Applies appearance preferences                                      |

---

## Metrics Dashboard

Both GUI and CLI collect:

- 🔄 **Requests/sec** – Throughput
- 🕒 **Avg Response Time** – Mean duration per request
- ✅ **Success Rate** – Ratio of successful responses
- 🧮 **Total Requests** – Combined successes + errors
- ⚠️ **Error Breakdown** – Grouped by type/status
- 📈 **Response Time Percentiles** – P50, P75, P90, P95, P99

---

## Planned Features

- [ ] Custom request body editing (raw or JSON)
- [ ] CLI config file loading
- [ ] Response validation and logging
- [ ] Real-time response content viewer
- [ ] Headless batch mode (e.g. multiple targets)
- [ ] Dockerized version for deployments

---

## License

GNU License. See [LICENSE](LICENSE) for full terms.
