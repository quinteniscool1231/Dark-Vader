import customtkinter as ctk
from tkinter import messagebox, ttk
import threading
import time
from datetime import datetime
from collections import deque
import statistics
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import json
import random
import numpy as np
from typing import Dict, List, Optional

class StressTestMetrics:
    def __init__(self):
        self.response_times = deque(maxlen=1000000)
        self.success_count = 0
        self.error_count = 0
        self.start_time = None
        self.error_types: Dict[str, int] = {}
        self.percentiles = [50, 75, 90, 95, 99]

    def reset(self):
        self.response_times.clear()
        self.success_count = 0
        self.error_count = 0
        self.error_types.clear()
        self.start_time = datetime.now()

    def add_response_time(self, response_time: float):
        self.response_times.append(response_time)

    def add_error(self, error_type: str):
        self.error_types[error_type] = self.error_types.get(error_type, 0) + 1
        self.error_count += 1

    def get_percentiles(self) -> Dict[int, float]:
        if not self.response_times:
            return {p: 0 for p in self.percentiles}
        return {p: float(np.percentile(list(self.response_times), p)) for p in self.percentiles}

    def get_stats(self) -> str:
        if not self.response_times:
            return "No data available"

        avg_response = statistics.mean(self.response_times) if self.response_times else 0
        total_requests = self.success_count + self.error_count
        success_rate = (self.success_count / total_requests * 100) if total_requests > 0 else 0
        duration = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        requests_per_second = total_requests / duration if duration > 0 else 0

        percentiles = self.get_percentiles()
        percentile_stats = "\n".join(f"P{p}: {percentiles[p]*1000:.2f}ms" for p in self.percentiles)

        error_breakdown = "\n".join(f"{error}: {count}" for error, count in self.error_types.items())

        return f"""
Performance Metrics:
==================
Requests/sec: {requests_per_second:.2f}
Avg Response Time: {avg_response*1000:.2f}ms
Success Rate: {success_rate:.1f}%
Total Requests: {total_requests}
Successes: {self.success_count}
Errors: {self.error_count}

Response Time Percentiles:
=======================
{percentile_stats}

Error Breakdown:
==============
{error_breakdown}
"""

class LoadProfile:
    CONSTANT = "Constant"
    RAMP_UP = "Ramp Up"
    PULSE = "Pulse"
    RANDOM = "Random"

    @staticmethod
    def get_thread_count(profile: str, base_threads: int, elapsed_time: float) -> int:
        if profile == LoadProfile.CONSTANT:
            return base_threads
        elif profile == LoadProfile.RAMP_UP:
            return min(base_threads, int(base_threads * (elapsed_time / 60)))
        elif profile == LoadProfile.PULSE:
            return base_threads if int(elapsed_time / 30) % 2 == 0 else base_threads // 2
        elif profile == LoadProfile.RANDOM:
            return random.randint(1, base_threads)
        return base_threads

class StressTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Dark Vader")
        self.root.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.metrics = StressTestMetrics()
        self.setup_variables()
        self.create_ui()
        self.session = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.setup_settings_traces()

        self.custom_headers: Dict[str, str] = {}
        self.cookies: Dict[str, str] = {}
        self.retry_count = 3
        self.retry_delay = 1.0
        self.connection_pool_size = 100
        self.keep_alive_timeout = 300

    def setup_variables(self):
        self.url_var = ctk.StringVar()
        self.num_threads_var = ctk.IntVar(value=200)
        self.config_name_var = ctk.StringVar()
        self.request_delay_var = ctk.StringVar(value="0")
        self.payload_size_var = ctk.IntVar(value=5000000)
        self.request_timeout_var = ctk.IntVar(value=30)
        self.request_method_var = ctk.StringVar(value="POST")
        self.load_profile_var = ctk.StringVar(value=LoadProfile.CONSTANT)

        self.retry_enabled_var = ctk.BooleanVar(value=True)
        self.retry_count_var = ctk.IntVar(value=3)
        self.retry_delay_var = ctk.DoubleVar(value=1.0)
        self.pool_size_var = ctk.IntVar(value=100)
        self.keep_alive_var = ctk.IntVar(value=300)

        self.appearance_mode_var = ctk.StringVar(value="dark")
        self.color_theme_var = ctk.StringVar(value="blue")
        self.font_size_var = ctk.IntVar(value=12)
        self.window_opacity_var = ctk.DoubleVar(value=1.0)

        self.stress_test_running = False

    def create_ui(self):
        self.tabview = ctk.CTkTabview(self.root, width=850, height=600)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.create_control_tab()
        self.create_settings_tab()
        self.create_metrics_tab()
        self.create_advanced_tab()

        self.root.after(100, self.update_metrics_display)

    def create_control_tab(self):
        control_tab = self.tabview.add("Control")

        status_frame = ctk.CTkFrame(control_tab)
        status_frame.pack(fill="x", padx=10, pady=5)

        self.status_label = ctk.CTkLabel(status_frame, text="Status: Ready")
        self.status_label.pack(side="left", padx=10)

        button_frame = ctk.CTkFrame(control_tab)
        button_frame.pack(fill="x", padx=10, pady=5)

        self.start_button = ctk.CTkButton(
            button_frame, 
            text="Start Test", 
            command=self.start_stress_test,
            fg_color="green"
        )
        self.start_button.pack(side="left", padx=5)

        self.stop_button = ctk.CTkButton(
            button_frame, 
            text="Stop Test", 
            command=self.stop_stress_test,
            state="disabled",
            fg_color="red"
        )
        self.stop_button.pack(side="left", padx=5)

        self.clear_button = ctk.CTkButton(
            button_frame,
            text="Clear Logs",
            command=lambda: self.log_textbox.delete("1.0", "end"),
            fg_color="gray"
        )
        self.clear_button.pack(side="left", padx=5)

        self.log_textbox = ctk.CTkTextbox(control_tab, height=400)
        self.log_textbox.pack(fill="both", expand=True, padx=10, pady=5)

    def create_settings_tab(self):
        settings_tab = self.tabview.add("Settings")

        # Configuration management frame
        config_frame = ctk.CTkFrame(settings_tab)
        config_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(config_frame, text="Configuration Name:").pack(side="left", padx=5)
        ctk.CTkEntry(config_frame, textvariable=self.config_name_var).pack(side="left", padx=5)
        ctk.CTkButton(config_frame, text="Save Config", command=self.save_config).pack(side="left", padx=5)
        ctk.CTkButton(config_frame, text="Load Config", command=self.load_config).pack(side="left", padx=5)

        settings_tabview = ctk.CTkTabview(settings_tab)
        settings_tabview.pack(fill="both", expand=True, padx=10, pady=10)

        request_tab = settings_tabview.add("Request")
        request_settings = [
            ("URL:", self.url_var, "Enter target URL", 300, "entry"),
            ("Number of Threads:", self.num_threads_var, "1-1000", 100, "entry"),
            ("Request Delay (s):", self.request_delay_var, "0.001-1.0", 100, "entry"),
            ("Payload Size (bytes):", self.payload_size_var, "1000-10000000", 100, "entry"),
            ("Timeout (seconds):", self.request_timeout_var, "1-60", 100, "entry"),
            ("Request Method:", self.request_method_var, "", 100, "combobox", ["GET", "POST", "PUT", "DELETE"]),
            ("Load Profile:", self.load_profile_var, "", 100, "combobox", 
             [LoadProfile.CONSTANT, LoadProfile.RAMP_UP, LoadProfile.PULSE, LoadProfile.RANDOM])
        ]

        for i, setting in enumerate(request_settings):
            label = ctk.CTkLabel(request_tab, text=setting[0])
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            if setting[4] == "entry":
                widget = ctk.CTkEntry(
                    request_tab,
                    textvariable=setting[1],
                    placeholder_text=setting[2],
                    width=setting[3]
                )
            elif setting[4] == "combobox":
                widget = ctk.CTkComboBox(
                    request_tab,
                    variable=setting[1],
                    values=setting[5],
                    width=setting[3]
                )
            widget.grid(row=i, column=1, padx=10, pady=10, sticky="w")

        appearance_tab = settings_tabview.add("Appearance")
        appearance_settings = [
            ("Theme Mode:", self.appearance_mode_var, "", 150, "combobox", ["dark", "light"]),
            ("Color Theme:", self.color_theme_var, "", 150, "combobox", ["blue", "green", "dark-blue"]),
            ("Font Size:", self.font_size_var, "10-20", 100, "entry"),
            ("Window Opacity:", self.window_opacity_var, "0.5-1.0", 100, "entry")
        ]

        for i, setting in enumerate(appearance_settings):
            label = ctk.CTkLabel(appearance_tab, text=setting[0])
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            if setting[4] == "entry":
                widget = ctk.CTkEntry(
                    appearance_tab,
                    textvariable=setting[1],
                    placeholder_text=setting[2],
                    width=setting[3]
                )
            elif setting[4] == "combobox":
                widget = ctk.CTkComboBox(
                    appearance_tab,
                    variable=setting[1],
                    values=setting[5],
                    width=setting[3]
                )
            widget.grid(row=i, column=1, padx=10, pady=10, sticky="w")

        apply_button = ctk.CTkButton(
            appearance_tab,
            text="Apply Settings",
            command=self.apply_settings,
            fg_color="green"
        )
        apply_button.grid(row=len(appearance_settings), column=0, columnspan=2, pady=20)

    def create_metrics_tab(self):
        metrics_tab = self.tabview.add("Metrics")

        # Top frame for metrics display
        top_frame = ctk.CTkFrame(metrics_tab)
        top_frame.pack(fill="x", padx=10, pady=5)

        self.metrics_display = ctk.CTkTextbox(top_frame, height=300)
        self.metrics_display.pack(fill="both", expand=True, padx=5, pady=5)

        # Bottom frame for export buttons and graph
        bottom_frame = ctk.CTkFrame(metrics_tab)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=5)

        export_frame = ctk.CTkFrame(bottom_frame)
        export_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkButton(export_frame, text="Export CSV", command=lambda: self.export_metrics("csv")).pack(side="left", padx=5)
        ctk.CTkButton(export_frame, text="Export JSON", command=lambda: self.export_metrics("json")).pack(side="left", padx=5)

        self.fig_canvas = None
        self.update_graph()

    def export_metrics(self, format_type):
        import pandas as pd
        import json
        from datetime import datetime

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = {
            'response_times': list(self.metrics.response_times),
            'success_count': self.metrics.success_count,
            'error_count': self.metrics.error_count,
            'percentiles': self.metrics.get_percentiles(),
            'error_types': self.metrics.error_types
        }

        if format_type == "csv":
            df = pd.DataFrame(data['response_times'], columns=['response_time'])
            df.to_csv(f'metrics_{timestamp}.csv', index=False)
        else:
            with open(f'metrics_{timestamp}.json', 'w') as f:
                json.dump(data, f, indent=2)

        self.log_message(f"Metrics exported to metrics_{timestamp}.{format_type}")

    def update_graph(self):
        if not hasattr(self, 'fig_canvas'):
            return

        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        if self.metrics.response_times:
            if self.fig_canvas:
                self.fig_canvas.get_tk_widget().destroy()

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.hist(self.metrics.response_times, bins=50, color='blue', alpha=0.7)
            ax.set_title('Response Time Distribution')
            ax.set_xlabel('Response Time (s)')
            ax.set_ylabel('Frequency')

            self.fig_canvas = FigureCanvasTkAgg(fig, master=self.metrics_tab)
            self.fig_canvas.draw()
            self.fig_canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        self.root.after(1000, self.update_graph)

    def create_advanced_tab(self):
        advanced_tab = self.tabview.add("Advanced")

        headers_frame = ctk.CTkFrame(advanced_tab)
        headers_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(headers_frame, text="Custom Headers").pack()
        self.headers_text = ctk.CTkTextbox(headers_frame, height=100)
        self.headers_text.pack(fill="x", padx=5, pady=5)

        cookies_frame = ctk.CTkFrame(advanced_tab)
        cookies_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(cookies_frame, text="Cookies").pack()
        self.cookies_text = ctk.CTkTextbox(cookies_frame, height=100)
        self.cookies_text.pack(fill="x", padx=5, pady=5)

        conn_frame = ctk.CTkFrame(advanced_tab)
        conn_frame.pack(fill="x", padx=10, pady=5)

        settings = [
            ("Pool Size:", self.pool_size_var, "10-1000"),
            ("Keep-Alive (s):", self.keep_alive_var, "60-600"),
            ("Retry Count:", self.retry_count_var, "0-10"),
            ("Retry Delay (s):", self.retry_delay_var, "0.1-5.0")
        ]

        for i, (label, var, placeholder) in enumerate(settings):
            ctk.CTkLabel(conn_frame, text=label).grid(row=i, column=0, padx=5, pady=5)
            ctk.CTkEntry(conn_frame, textvariable=var, placeholder_text=placeholder).grid(
                row=i, column=1, padx=5, pady=5)

    def update_metrics_display(self):
        if self.stress_test_running:
            self.metrics_display.delete("1.0", "end")
            self.metrics_display.insert("1.0", self.metrics.get_stats())
        self.root.after(100, self.update_metrics_display)

    def log_message(self, message):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.log_textbox.insert("end", f"[{timestamp}] {message}\n")
        self.log_textbox.see("end")

    async def make_request(self, session, url, headers, data):
        retries = self.retry_count_var.get() if self.retry_enabled_var.get() else 0
        retry_delay = self.retry_delay_var.get()

        for attempt in range(retries + 1):
            try:
                start_time = time.time()
                method = self.request_method_var.get().lower()

                request_headers = headers.copy()
                try:
                    custom_headers = json.loads(self.headers_text.get("1.0", "end").strip())
                    request_headers.update(custom_headers)
                except:
                    pass

                try:
                    cookies = json.loads(self.cookies_text.get("1.0", "end").strip())
                except:
                    cookies = {}

                async with getattr(session, method)(
                    url, 
                    json=data, 
                    headers=request_headers,
                    cookies=cookies
                ) as response:
                    await response.read()
                    response_time = time.time() - start_time

                    self.root.after(0, self.log_message, 
                                  f"Request completed in {response_time*1000:.2f}ms")

                    self.metrics.add_response_time(response_time)
                    if response.status < 400:
                        self.metrics.success_count += 1
                    else:
                        error_msg = f"HTTP {response.status}: {response.reason}"
                        self.metrics.add_error(error_msg)
                        self.log_message(error_msg)

            except Exception as e:
                error_type = type(e).__name__
                self.metrics.add_error(error_type)
                self.log_message(f"Request failed: {str(e)}")

                if attempt < retries:
                    await asyncio.sleep(retry_delay)
                    continue
                break

    def save_config(self):
        try:
            if not self.config_name_var.get().strip():
                messagebox.showerror("Error", "Please enter a configuration name")
                return

            config = {
                'url': self.url_var.get(),
                'num_threads': self.num_threads_var.get(),
                'request_delay': self.request_delay_var.get(),
                'payload_size': self.payload_size_var.get(),
                'request_timeout': self.request_timeout_var.get(),
                'request_method': self.request_method_var.get(),
                'load_profile': self.load_profile_var.get(),
                'headers': self.headers_text.get("1.0", "end").strip(),
                'cookies': self.cookies_text.get("1.0", "end").strip(),
                'retry_count': self.retry_count_var.get(),
                'retry_delay': self.retry_delay_var.get(),
                'pool_size': self.pool_size_var.get(),
                'keep_alive': self.keep_alive_var.get()
            }

            filename = f"config_{self.config_name_var.get()}.json"
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2)
            self.log_message(f"Configuration saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")

    def load_config(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            initialdir="."
        )
        if not filename:
            return

        try:
            with open(filename, 'r') as f:
                config = json.load(f)

            self.url_var.set(config.get('url', ''))
            self.num_threads_var.set(config.get('num_threads', 200))
            self.request_delay_var.set(config.get('request_delay', '0'))
            self.payload_size_var.set(config.get('payload_size', 5000000))
            self.request_timeout_var.set(config.get('request_timeout', 30))
            self.request_method_var.set(config.get('request_method', 'POST'))
            self.load_profile_var.set(config.get('load_profile', LoadProfile.CONSTANT))

            self.headers_text.delete("1.0", "end")
            self.headers_text.insert("1.0", config.get('headers', ''))

            self.cookies_text.delete("1.0", "end")
            self.cookies_text.insert("1.0", config.get('cookies', ''))

            self.retry_count_var.set(config.get('retry_count', 3))
            self.retry_delay_var.set(config.get('retry_delay', 1.0))
            self.pool_size_var.set(config.get('pool_size', 100))
            self.keep_alive_var.set(config.get('keep_alive', 300))

            self.log_message(f"Configuration loaded from {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")

    async def worker(self, url):
        conn = aiohttp.TCPConnector(
            limit=self.pool_size_var.get(),
            ttl_dns_cache=300,
            force_close=False,
            enable_cleanup_closed=True
        )

        timeout = aiohttp.ClientTimeout(total=self.request_timeout_var.get())
        headers = {
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'Keep-Alive': f'timeout={self.keep_alive_var.get()}'
        }

        data = {'stress_test': 'x' * self.payload_size_var.get()}

        async with aiohttp.ClientSession(
            connector=conn, 
            timeout=timeout,
            trace_configs=None
        ) as session:
            while self.stress_test_running:
                try:
                    delay = float(self.request_delay_var.get())
                    if delay > 0:
                        await asyncio.sleep(delay)
                    await self.make_request(session, url, headers, data)
                except Exception as e:
                    self.log_message(f"Worker error: {str(e)}")
                    continue

    def run_async_loop(self, url):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        base_threads = self.num_threads_var.get()
        start_time = time.time()

        while self.stress_test_running:
            elapsed_time = time.time() - start_time
            thread_count = LoadProfile.get_thread_count(
                self.load_profile_var.get(),
                base_threads,
                elapsed_time
            )

            tasks = [loop.create_task(self.worker(url)) for _ in range(thread_count)]
            loop.run_until_complete(asyncio.gather(*tasks))

    def validate_inputs(self):
        if not self.url_var.get().strip():
            messagebox.showerror("Error", "Please enter a valid URL")
            return False

        try:
            threads = self.num_threads_var.get()
            if not 1 <= threads <= 1000:
                raise ValueError
        except:
            messagebox.showerror("Error", "Threads must be between 1 and 1000")
            return False

        return True

    def start_stress_test(self):
        if not self.validate_inputs():
            return

        self.stress_test_running = True
        self.metrics.reset()
        self.status_label.configure(text="Status: Running")
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        url = self.url_var.get().strip()
        threading.Thread(target=self.run_async_loop, args=(url,), daemon=True).start()

    def stop_stress_test(self):
        self.stress_test_running = False
        self.status_label.configure(text="Status: Stopping...")
        
        def complete_stop():
            self.status_label.configure(text="Status: Stopped")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.log_message("Stress test stopped")
            
        # Give workers time to clean up
        self.root.after(1000, complete_stop)

    def apply_settings(self, *args):
        try:
            ctk.set_appearance_mode(self.appearance_mode_var.get())
            ctk.set_default_color_theme(self.color_theme_var.get())

            font_size = max(8, min(20, self.font_size_var.get()))
            self.log_textbox.configure(font=("TkDefaultFont", font_size))
            self.metrics_display.configure(font=("TkDefaultFont", font_size))

            opacity = max(0.1, min(1.0, float(self.window_opacity_var.get())))
            self.root.attributes('-alpha', opacity)

            self.log_message("Settings applied successfully!")
        except Exception as e:
            self.log_message(f"Error applying settings: {str(e)}")

    def setup_settings_traces(self):
        def validate_and_apply(*args):
            try:
                font_size = max(8, min(20, self.font_size_var.get()))
                opacity = max(0.1, min(1.0, self.window_opacity_var.get()))
                self.font_size_var.set(font_size)
                self.window_opacity_var.set(opacity)
                self.apply_settings()
            except:
                pass

        self.appearance_mode_var.trace_add("write", validate_and_apply)
        self.color_theme_var.trace_add("write", validate_and_apply)
        self.font_size_var.trace_add("write", validate_and_apply)
        self.window_opacity_var.trace_add("write", validate_and_apply)

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Dark Vader")
    tester = StressTester(app)
    app.mainloop()