# -*- coding: utf-8 -*-
"""
محلل مخرجات ApacheBench
ApacheBench Output Parser
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ABResults:
    """نتائج اختبار ApacheBench"""
    server_software: str = ""
    server_hostname: str = ""
    server_port: int = 80
    document_path: str = ""
    document_length: int = 0
    concurrency_level: int = 1
    time_taken: float = 0.0
    complete_requests: int = 0
    failed_requests: int = 0
    total_transferred: int = 0
    html_transferred: int = 0
    requests_per_second: float = 0.0
    time_per_request: float = 0.0
    time_per_request_concurrent: float = 0.0
    transfer_rate: float = 0.0
    connect_min: float = 0.0
    connect_max: float = 0.0
    connect_mean: float = 0.0
    processing_min: float = 0.0
    processing_max: float = 0.0
    processing_mean: float = 0.0
    waiting_min: float = 0.0
    waiting_max: float = 0.0
    waiting_mean: float = 0.0
    total_min: float = 0.0
    total_max: float = 0.0
    total_mean: float = 0.0

    def get_summary_arabic(self) -> str:
        """الحصول على ملخص النتائج بالعربية"""
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    📊 ملخص نتائج الاختبار                    ║
╠══════════════════════════════════════════════════════════════╣
║  🌐 الخادم: {self.server_software or 'غير محدد':<45} ║
║  🔗 المضيف: {self.server_hostname}:{self.server_port:<38} ║
╠══════════════════════════════════════════════════════════════╣
║                      📈 الأداء العام                         ║
╠══════════════════════════════════════════════════════════════╣
║  ⚡ الطلبات في الثانية:     {self.requests_per_second:>15.2f} req/sec     ║
║  ⏱️  زمن الطلب (متوسط):      {self.time_per_request:>15.2f} ms          ║
║  📦 معدل النقل:             {self.transfer_rate:>15.2f} KB/sec      ║
║  🕐 الزمن الإجمالي:          {self.time_taken:>15.2f} sec         ║
╠══════════════════════════════════════════════════════════════╣
║                      📋 إحصائيات الطلبات                     ║
╠══════════════════════════════════════════════════════════════╣
║  ✅ الطلبات المكتملة:       {self.complete_requests:>20,}              ║
║  ❌ الطلبات الفاشلة:        {self.failed_requests:>20,}              ║
║  🔄 مستوى التزامن:          {self.concurrency_level:>20,}              ║
╠══════════════════════════════════════════════════════════════╣
║                      📊 أزمنة الاستجابة                      ║
╠══════════════════════════════════════════════════════════════╣
║  الاتصال:    أدنى {self.connect_min:>6.0f}ms | متوسط {self.connect_mean:>6.0f}ms | أقصى {self.connect_max:>6.0f}ms ║
║  المعالجة:   أدنى {self.processing_min:>6.0f}ms | متوسط {self.processing_mean:>6.0f}ms | أقصى {self.processing_max:>6.0f}ms ║
║  الانتظار:   أدنى {self.waiting_min:>6.0f}ms | متوسط {self.waiting_mean:>6.0f}ms | أقصى {self.waiting_max:>6.0f}ms ║
║  الإجمالي:   أدنى {self.total_min:>6.0f}ms | متوسط {self.total_mean:>6.0f}ms | أقصى {self.total_max:>6.0f}ms ║
╚══════════════════════════════════════════════════════════════╝
"""
        return summary


class ABParser:
    """محلل مخرجات ApacheBench"""

    def __init__(self):
        self.patterns = {
            'server_software': r'Server Software:\s+(.+)',
            'server_hostname': r'Server Hostname:\s+(.+)',
            'server_port': r'Server Port:\s+(\d+)',
            'document_path': r'Document Path:\s+(.+)',
            'document_length': r'Document Length:\s+(\d+)',
            'concurrency_level': r'Concurrency Level:\s+(\d+)',
            'time_taken': r'Time taken for tests:\s+([\d.]+)',
            'complete_requests': r'Complete requests:\s+(\d+)',
            'failed_requests': r'Failed requests:\s+(\d+)',
            'total_transferred': r'Total transferred:\s+(\d+)',
            'html_transferred': r'HTML transferred:\s+(\d+)',
            'requests_per_second': r'Requests per second:\s+([\d.]+)',
            'time_per_request': r'Time per request:\s+([\d.]+)\s+\[ms\]\s+\(mean\)',
            'time_per_request_concurrent': r'Time per request:\s+([\d.]+)\s+\[ms\]\s+\(mean, across all concurrent requests\)',
            'transfer_rate': r'Transfer rate:\s+([\d.]+)',
        }

    def parse(self, output: str) -> Optional[ABResults]:
        """تحليل مخرجات ApacheBench"""
        if not output:
            return None

        results = ABResults()

        # استخراج القيم الأساسية
        for field, pattern in self.patterns.items():
            match = re.search(pattern, output)
            if match:
                value = match.group(1)
                if field in ['server_port', 'document_length', 'concurrency_level',
                             'complete_requests', 'failed_requests', 'total_transferred',
                             'html_transferred']:
                    setattr(results, field, int(value))
                elif field in ['time_taken', 'requests_per_second', 'time_per_request',
                               'time_per_request_concurrent', 'transfer_rate']:
                    setattr(results, field, float(value))
                else:
                    setattr(results, field, value.strip())

        # استخراج أزمنة الاتصال والمعالجة
        connection_times = self._parse_connection_times(output)
        if connection_times:
            for key, value in connection_times.items():
                setattr(results, key, value)

        return results

    def _parse_connection_times(self, output: str) -> dict:
        """استخراج أزمنة الاتصال"""
        times = {}

        # البحث عن جدول Connection Times
        table_pattern = r'Connection Times \(ms\)\s+min\s+mean.*?Connect:\s+(\d+)\s+(\d+).*?Processing:\s+(\d+)\s+(\d+).*?Waiting:\s+(\d+)\s+(\d+).*?Total:\s+(\d+)\s+(\d+)'
        match = re.search(table_pattern, output, re.DOTALL)

        if match:
            times['connect_min'] = float(match.group(1))
            times['connect_mean'] = float(match.group(2))
            times['processing_min'] = float(match.group(3))
            times['processing_mean'] = float(match.group(4))
            times['waiting_min'] = float(match.group(5))
            times['waiting_mean'] = float(match.group(6))
            times['total_min'] = float(match.group(7))
            times['total_mean'] = float(match.group(8))

        # البحث عن القيم القصوى
        max_pattern = r'(\w+):\s+\d+\s+\d+\s+[\d.]+\s+(\d+)\s+(\d+)'
        for match in re.finditer(max_pattern, output):
            metric = match.group(1).lower()
            if metric in ['connect', 'processing', 'waiting', 'total']:
                times[f'{metric}_max'] = float(match.group(3))

        return times

    def is_error_output(self, output: str) -> tuple[bool, str]:
        """التحقق من وجود أخطاء في المخرجات"""
        error_patterns = [
            (r'apr_socket_connect\(\): Connection refused',
             'تم رفض الاتصال - تأكد من أن الخادم يعمل'),
            (r'apr_socket_connect\(\): Connection timed out',
             'انتهت مهلة الاتصال - تحقق من الشبكة'),
            (r'SSL connect error', 'خطأ في اتصال SSL'),
            (r'Name or service not known', 'اسم المضيف غير معروف'),
            (r'Connection reset by peer', 'تم إعادة تعيين الاتصال من قبل الخادم'),
        ]

        for pattern, message in error_patterns:
            if re.search(pattern, output):
                return True, message

        return False, ""
