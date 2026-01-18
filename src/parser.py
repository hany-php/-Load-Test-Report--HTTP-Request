"""
AB Output Parser Module
Parses ApacheBench output using regex to extract key metrics.
"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ABMetrics:
    """Parsed metrics from ApacheBench output."""

    # Server info
    server_software: str = ""
    server_hostname: str = ""
    server_port: int = 0

    # Test parameters
    document_path: str = ""
    document_length: int = 0
    concurrency_level: int = 0

    # Time metrics
    time_taken: float = 0.0  # seconds

    # Request metrics
    complete_requests: int = 0
    failed_requests: int = 0
    non_2xx_responses: int = 0

    # Data transfer
    total_transferred: int = 0  # bytes
    html_transferred: int = 0  # bytes

    # Performance metrics
    requests_per_second: float = 0.0
    time_per_request: float = 0.0  # ms (mean)
    # ms (mean, across all concurrent requests)
    time_per_request_concurrent: float = 0.0
    transfer_rate: float = 0.0  # KB/sec

    # Connection times (ms)
    connect_min: float = 0.0
    connect_mean: float = 0.0
    connect_median: float = 0.0
    connect_max: float = 0.0

    processing_min: float = 0.0
    processing_mean: float = 0.0
    processing_median: float = 0.0
    processing_max: float = 0.0

    waiting_min: float = 0.0
    waiting_mean: float = 0.0
    waiting_median: float = 0.0
    waiting_max: float = 0.0

    total_min: float = 0.0
    total_mean: float = 0.0
    total_median: float = 0.0
    total_max: float = 0.0

    # Percentile data
    percentiles: dict = field(default_factory=dict)

    # Raw output
    raw_output: str = ""

    def to_dict(self) -> dict:
        """Convert metrics to dictionary for JSON export."""
        return {
            "server": {
                "software": self.server_software,
                "hostname": self.server_hostname,
                "port": self.server_port,
            },
            "test_parameters": {
                "document_path": self.document_path,
                "document_length": self.document_length,
                "concurrency_level": self.concurrency_level,
            },
            "results": {
                "time_taken_seconds": self.time_taken,
                "complete_requests": self.complete_requests,
                "failed_requests": self.failed_requests,
                "non_2xx_responses": self.non_2xx_responses,
                "total_transferred_bytes": self.total_transferred,
                "html_transferred_bytes": self.html_transferred,
            },
            "performance": {
                "requests_per_second": self.requests_per_second,
                "time_per_request_ms": self.time_per_request,
                "time_per_request_concurrent_ms": self.time_per_request_concurrent,
                "transfer_rate_kbps": self.transfer_rate,
            },
            "connection_times_ms": {
                "connect": {
                    "min": self.connect_min,
                    "mean": self.connect_mean,
                    "median": self.connect_median,
                    "max": self.connect_max,
                },
                "processing": {
                    "min": self.processing_min,
                    "mean": self.processing_mean,
                    "median": self.processing_median,
                    "max": self.processing_max,
                },
                "waiting": {
                    "min": self.waiting_min,
                    "mean": self.waiting_mean,
                    "median": self.waiting_median,
                    "max": self.waiting_max,
                },
                "total": {
                    "min": self.total_min,
                    "mean": self.total_mean,
                    "median": self.total_median,
                    "max": self.total_max,
                },
            },
            "percentiles": self.percentiles,
        }


class ABOutputParser:
    """Parser for ApacheBench command output."""

    # Regex patterns for parsing ab output
    PATTERNS = {
        'server_software': r'Server Software:\s+(.+)',
        'server_hostname': r'Server Hostname:\s+(.+)',
        'server_port': r'Server Port:\s+(\d+)',
        'document_path': r'Document Path:\s+(.+)',
        'document_length': r'Document Length:\s+(\d+)',
        'concurrency_level': r'Concurrency Level:\s+(\d+)',
        'time_taken': r'Time taken for tests:\s+([\d.]+)\s+seconds',
        'complete_requests': r'Complete requests:\s+(\d+)',
        'failed_requests': r'Failed requests:\s+(\d+)',
        'non_2xx': r'Non-2xx responses:\s+(\d+)',
        'total_transferred': r'Total transferred:\s+(\d+)',
        'html_transferred': r'HTML transferred:\s+(\d+)',
        'requests_per_second': r'Requests per second:\s+([\d.]+)',
        'time_per_request': r'Time per request:\s+([\d.]+)\s+\[ms\]\s+\(mean\)',
        'time_per_request_concurrent': r'Time per request:\s+([\d.]+)\s+\[ms\]\s+\(mean, across all concurrent requests\)',
        'transfer_rate': r'Transfer rate:\s+([\d.]+)',
    }

    # Pattern for connection times table
    CONNECTION_TIMES_PATTERN = r'(Connect|Processing|Waiting|Total)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)'

    # Pattern for percentile data
    PERCENTILE_PATTERN = r'(\d+)%\s+(\d+)'

    def parse(self, output: str) -> ABMetrics:
        """
        Parse ApacheBench output and extract metrics.

        Args:
            output: Raw output from ab command

        Returns:
            ABMetrics: Parsed metrics
        """
        metrics = ABMetrics(raw_output=output)

        # Parse simple patterns
        for key, pattern in self.PATTERNS.items():
            match = re.search(pattern, output)
            if match:
                value = match.group(1).strip()

                # Convert to appropriate type
                if key in ['server_port', 'document_length', 'concurrency_level',
                           'complete_requests', 'failed_requests', 'non_2xx',
                           'total_transferred', 'html_transferred']:
                    value = int(value)
                elif key in ['time_taken', 'requests_per_second', 'time_per_request',
                             'time_per_request_concurrent', 'transfer_rate']:
                    value = float(value)

                # Map to metrics attribute
                attr_map = {
                    'non_2xx': 'non_2xx_responses',
                    'time_per_request': 'time_per_request',
                    'time_per_request_concurrent': 'time_per_request_concurrent',
                }
                attr_name = attr_map.get(key, key)
                setattr(metrics, attr_name, value)

        # Parse connection times
        self._parse_connection_times(output, metrics)

        # Parse percentiles
        self._parse_percentiles(output, metrics)

        return metrics

    def _parse_connection_times(self, output: str, metrics: ABMetrics):
        """Parse the connection times table."""
        matches = re.findall(self.CONNECTION_TIMES_PATTERN, output)

        for match in matches:
            category = match[0].lower()
            min_val = float(match[1])
            mean_val = float(match[2])
            median_val = float(match[3])
            max_val = float(match[4])

            if category == 'connect':
                metrics.connect_min = min_val
                metrics.connect_mean = mean_val
                metrics.connect_median = median_val
                metrics.connect_max = max_val
            elif category == 'processing':
                metrics.processing_min = min_val
                metrics.processing_mean = mean_val
                metrics.processing_median = median_val
                metrics.processing_max = max_val
            elif category == 'waiting':
                metrics.waiting_min = min_val
                metrics.waiting_mean = mean_val
                metrics.waiting_median = median_val
                metrics.waiting_max = max_val
            elif category == 'total':
                metrics.total_min = min_val
                metrics.total_mean = mean_val
                metrics.total_median = median_val
                metrics.total_max = max_val

    def _parse_percentiles(self, output: str, metrics: ABMetrics):
        """Parse the percentile distribution."""
        # Find the percentile section
        percentile_section = re.search(
            r'Percentage of the requests served within a certain time.*?(?=\n\n|\Z)',
            output,
            re.DOTALL
        )

        if percentile_section:
            section_text = percentile_section.group(0)
            matches = re.findall(self.PERCENTILE_PATTERN, section_text)

            for match in matches:
                percentile = int(match[0])
                time_ms = int(match[1])
                metrics.percentiles[f"p{percentile}"] = time_ms


def format_summary(metrics: ABMetrics) -> str:
    """
    Format metrics as a human-readable summary.

    Args:
        metrics: Parsed AB metrics

    Returns:
        str: Formatted summary text
    """
    lines = [
        "=" * 60,
        "                    TEST SUMMARY",
        "=" * 60,
        "",
        "SERVER INFORMATION",
        "-" * 40,
        f"  Software:        {metrics.server_software}",
        f"  Hostname:        {metrics.server_hostname}",
        f"  Port:            {metrics.server_port}",
        "",
        "TEST CONFIGURATION",
        "-" * 40,
        f"  Document Path:   {metrics.document_path}",
        f"  Concurrency:     {metrics.concurrency_level}",
        "",
        "RESULTS",
        "-" * 40,
        f"  Time Taken:      {metrics.time_taken:.3f} seconds",
        f"  Complete:        {metrics.complete_requests:,}",
        f"  Failed:          {metrics.failed_requests:,}",
    ]

    if metrics.non_2xx_responses > 0:
        lines.append(f"  Non-2xx:         {metrics.non_2xx_responses:,}")

    lines.extend([
        "",
        "PERFORMANCE",
        "-" * 40,
        f"  Requests/sec:    {metrics.requests_per_second:.2f}",
        f"  Time/request:    {metrics.time_per_request:.3f} ms (mean)",
        f"  Transfer rate:   {metrics.transfer_rate:.2f} KB/sec",
        "",
        "CONNECTION TIMES (ms)",
        "-" * 40,
        "              Min    Mean   Median    Max",
        f"  Connect:   {metrics.connect_min:>5.0f}   {metrics.connect_mean:>5.0f}   {metrics.connect_median:>6.1f}  {metrics.connect_max:>5.0f}",
        f"  Process:   {metrics.processing_min:>5.0f}   {metrics.processing_mean:>5.0f}   {metrics.processing_median:>6.1f}  {metrics.processing_max:>5.0f}",
        f"  Waiting:   {metrics.waiting_min:>5.0f}   {metrics.waiting_mean:>5.0f}   {metrics.waiting_median:>6.1f}  {metrics.waiting_max:>5.0f}",
        f"  Total:     {metrics.total_min:>5.0f}   {metrics.total_mean:>5.0f}   {metrics.total_median:>6.1f}  {metrics.total_max:>5.0f}",
    ])

    if metrics.percentiles:
        lines.extend([
            "",
            "PERCENTILE DISTRIBUTION (ms)",
            "-" * 40,
        ])
        for key in sorted(metrics.percentiles.keys(), key=lambda x: int(x[1:])):
            lines.append(f"  {key}:  {metrics.percentiles[key]} ms")

    lines.extend([
        "",
        "=" * 60,
    ])

    return "\n".join(lines)


def format_summary_arabic(metrics: ABMetrics) -> str:
    """
    تنسيق المقاييس كملخص مقروء بالعربية.

    Args:
        metrics: مقاييس AB المحللة

    Returns:
        str: نص الملخص المنسق بالعربية
    """
    lines = [
        "╔" + "═" * 60 + "╗",
        "║" + "ملخص نتائج الاختبار".center(60) + "║",
        "╚" + "═" * 60 + "╝",
        "",
        "📊 معلومات الخادم",
        "─" * 45,
        f"  🖥️  البرنامج:        {metrics.server_software or 'غير متاح'}",
        f"  🌐 المضيف:         {metrics.server_hostname or 'غير متاح'}",
        f"  🔌 المنفذ:          {metrics.server_port}",
        "",
        "⚙️  إعدادات الاختبار",
        "─" * 45,
        f"  📁 مسار المستند:    {metrics.document_path or 'غير متاح'}",
        f"  📏 طول المستند:     {metrics.document_length:,} بايت",
        f"  🔄 مستوى التزامن:   {metrics.concurrency_level}",
        "",
        "📈 النتائج",
        "─" * 45,
        f"  ⏱️  الزمن الإجمالي:   {metrics.time_taken:.3f} ثانية",
        f"  ✅ طلبات مكتملة:    {metrics.complete_requests:,}",
        f"  ❌ طلبات فاشلة:     {metrics.failed_requests:,}",
    ]

    if metrics.non_2xx_responses > 0:
        lines.append(f"  ⚠️  استجابات غير 2xx: {metrics.non_2xx_responses:,}")

    lines.extend([
        "",
        "⚡ الأداء",
        "─" * 45,
        f"  🚀 الطلبات/ثانية:   {metrics.requests_per_second:.2f} طلب/ث",
        f"  ⏳ زمن/طلب:        {metrics.time_per_request:.3f} م.ث (متوسط)",
        f"  📦 معدل النقل:      {metrics.transfer_rate:.2f} ك.ب/ث",
        "",
        "📊 نقل البيانات",
        "─" * 45,
        f"  📤 إجمالي المنقول:  {metrics.total_transferred:,} بايت ({metrics.total_transferred / 1024:.2f} ك.ب)",
        f"  📄 HTML المنقول:    {metrics.html_transferred:,} بايت ({metrics.html_transferred / 1024:.2f} ك.ب)",
        "",
        "⏱️  أزمنة الاتصال (مللي ثانية)",
        "─" * 45,
        "                   أدنى    متوسط   الوسيط    أقصى",
        f"  الاتصال:        {metrics.connect_min:>5.0f}    {metrics.connect_mean:>5.0f}    {metrics.connect_median:>6.1f}   {metrics.connect_max:>5.0f}",
        f"  المعالجة:       {metrics.processing_min:>5.0f}    {metrics.processing_mean:>5.0f}    {metrics.processing_median:>6.1f}   {metrics.processing_max:>5.0f}",
        f"  الانتظار:       {metrics.waiting_min:>5.0f}    {metrics.waiting_mean:>5.0f}    {metrics.waiting_median:>6.1f}   {metrics.waiting_max:>5.0f}",
        f"  الإجمالي:       {metrics.total_min:>5.0f}    {metrics.total_mean:>5.0f}    {metrics.total_median:>6.1f}   {metrics.total_max:>5.0f}",
    ])

    if metrics.percentiles:
        lines.extend([
            "",
            "📊 توزيع النسب المئوية (مللي ثانية)",
            "─" * 45,
        ])
        for key in sorted(metrics.percentiles.keys(), key=lambda x: int(x[1:])):
            percent = key[1:]
            lines.append(
                f"  {percent}% من الطلبات اكتملت في: {metrics.percentiles[key]} م.ث")

    lines.extend([
        "",
        "╔" + "═" * 60 + "╗",
        "║" + "تم إنشاء التقرير بواسطة أداة اختبار الحمل".center(60) + "║",
        "╚" + "═" * 60 + "╝",
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    # Test with sample output
    sample_output = """
Server Software:        nginx/1.18.0
Server Hostname:        example.com
Server Port:            443

Document Path:          /
Document Length:        1234 bytes

Concurrency Level:      10
Time taken for tests:   5.123 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      1500000 bytes
HTML transferred:       1234000 bytes

Requests per second:    195.20 [#/sec] (mean)
Time per request:       51.230 [ms] (mean)
Time per request:       5.123 [ms] (mean, across all concurrent requests)
Transfer rate:          286.00 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        1    5   2.0      4      20
Processing:    10   45  15.0     42     150
Waiting:        8   40  12.0     38     140
Total:         12   50  16.0     46     160

Percentage of the requests served within a certain time (ms)
  50%     46
  66%     52
  75%     58
  80%     62
  90%     75
  95%     90
  98%    110
  99%    130
 100%    160 (longest request)
"""

    parser = ABOutputParser()
    metrics = parser.parse(sample_output)
    print(format_summary(metrics))
