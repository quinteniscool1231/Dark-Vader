import argparse
import json
import asyncio
from main import StressTestMetrics, LoadProfile
import aiohttp
import time
from datetime import datetime
import sys
import signal
import validators
from typing import Optional
import os

class GracefulExit(SystemExit):
    pass

def signal_handler(signum, frame):
    raise GracefulExit()

def validate_url(url: str) -> bool:
    return validators.url(url)

def validate_positive(value: str) -> int:
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} must be positive")
    return ivalue

def validate_method(value: str) -> str:
    valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD']
    if value.upper() not in valid_methods:
        raise argparse.ArgumentTypeError(f"Method must be one of {', '.join(valid_methods)}")
    return value.upper()

class ProgressBar:
    def __init__(self, duration: int):
        self.duration = duration
        self.start_time = time.time()

    def update(self, metrics: StressTestMetrics):
        elapsed = int(time.time() - self.start_time)
        remaining = max(0, self.duration - elapsed)
        bar_len = 40
        filled = int(bar_len * elapsed / self.duration)
        bar = '=' * filled + '-' * (bar_len - filled)
        
        sys.stdout.write('\r')
        sys.stdout.write(f'Progress: [{bar}] {elapsed}/{self.duration}s | ')
        sys.stdout.write(f'Requests: {metrics.success_count + metrics.error_count} | ')
        sys.stdout.write(f'Success Rate: {(metrics.success_count/(metrics.success_count + metrics.error_count)*100 if metrics.success_count + metrics.error_count > 0 else 0):.1f}%')
        sys.stdout.flush()

async def run_stress_test(args) -> Optional[StressTestMetrics]:
    metrics = StressTestMetrics()
    metrics.reset()
    progress = ProgressBar(args.duration)
    
    async def worker(url: str, headers: dict, data: dict):
        try:
            conn = aiohttp.TCPConnector(
                limit=args.pool_size,
                ttl_dns_cache=300,
                force_close=False
            )
            
            timeout = aiohttp.ClientTimeout(total=args.timeout)
            
            async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
                while True:
                    try:
                        if args.delay > 0:
                            await asyncio.sleep(args.delay)
                            
                        start_time = time.time()
                        method = args.method.lower()
                        
                        async with getattr(session, method)(url, json=data, headers=headers) as response:
                            await response.read()
                            response_time = time.time() - start_time
                            
                            metrics.add_response_time(response_time)
                            if response.status < 400:
                                metrics.success_count += 1
                            else:
                                metrics.add_error(f"HTTP {response.status}")
                                
                    except asyncio.CancelledError:
                        return
                    except Exception as e:
                        metrics.add_error(type(e).__name__)
                        
                    if time.time() - metrics.start_time > args.duration:
                        return
                    
                    progress.update(metrics)
        except Exception as e:
            print(f"\nWorker error: {str(e)}")

    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        headers = {'Content-Type': 'application/json'}
        data = {'stress_test': 'x' * args.payload_size}
        
        tasks = [asyncio.create_task(worker(args.url, headers, data)) 
                for _ in range(args.threads)]
        
        await asyncio.gather(*tasks)
        print("\nTest completed successfully")
        return metrics
        
    except GracefulExit:
        print("\nGracefully shutting down...")
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        return metrics
    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        return None

def save_metrics(metrics: StressTestMetrics, output_file: str):
    try:
        data = {
            'response_times': list(metrics.response_times),
            'success_count': metrics.success_count,
            'error_count': metrics.error_count,
            'percentiles': metrics.get_percentiles(),
            'error_types': metrics.error_types,
            'timestamp': datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\nMetrics exported to {output_file}")
    except Exception as e:
        print(f"\nFailed to save metrics: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description='Dark Vader CLI - HTTP Stress Testing Tool',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('url', type=str, help='Target URL')
    parser.add_argument('--threads', type=validate_positive, default=200, help='Number of threads')
    parser.add_argument('--duration', type=validate_positive, default=60, help='Test duration in seconds')
    parser.add_argument('--method', type=validate_method, default='POST', help='HTTP method')
    parser.add_argument('--payload-size', type=validate_positive, default=5000000, help='Payload size in bytes')
    parser.add_argument('--delay', type=float, default=0, help='Delay between requests (seconds)')
    parser.add_argument('--timeout', type=validate_positive, default=30, help='Request timeout (seconds)')
    parser.add_argument('--pool-size', type=validate_positive, default=100, help='Connection pool size')
    parser.add_argument('--output', type=str, help='Output file for metrics (JSON)')
    
    try:
        args = parser.parse_args()
        
        if not validate_url(args.url):
            print("Error: Invalid URL provided")
            sys.exit(1)
            
        print(f"Starting stress test against {args.url}")
        print(f"Configuration: {args.threads} threads, {args.duration}s duration, {args.method} method")
        
        metrics = asyncio.run(run_stress_test(args))
        
        if metrics:
            print(metrics.get_stats())
            if args.output:
                save_metrics(metrics, args.output)
                
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
