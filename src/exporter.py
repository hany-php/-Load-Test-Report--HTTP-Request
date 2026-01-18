"""
Export Module
Handles exporting test results to JSON and TXT formats.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from parser import ABMetrics, format_summary
from ab_runner import ABTestConfig


def export_to_json(
    metrics: ABMetrics,
    config: ABTestConfig,
    filepath: str | Path,
    include_raw: bool = True
) -> None:
    """
    Export test results to a JSON file.

    Args:
        metrics: Parsed AB metrics
        config: Test configuration used
        filepath: Path to save the JSON file
        include_raw: Whether to include raw output in export
    """
    export_data = {
        "export_info": {
            "timestamp": datetime.now().isoformat(),
            "format_version": "1.0",
        },
        "test_config": {
            "url": config.url,
            "requests": config.requests,
            "concurrency": config.concurrency,
            "keep_alive": config.keep_alive,
        },
        "metrics": metrics.to_dict(),
    }

    if include_raw:
        export_data["raw_output"] = metrics.raw_output

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)


def export_to_txt(
    metrics: ABMetrics,
    config: ABTestConfig,
    filepath: str | Path,
    include_raw: bool = True
) -> None:
    """
    Export test results to a TXT file.

    Args:
        metrics: Parsed AB metrics
        config: Test configuration used
        filepath: Path to save the TXT file
        include_raw: Whether to include raw output in export
    """
    lines = [
        "=" * 70,
        "              APACHE BENCH LOAD TEST REPORT",
        "=" * 70,
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "TEST CONFIGURATION",
        "-" * 50,
        f"  URL:          {config.url}",
        f"  Requests:     {config.requests:,}",
        f"  Concurrency:  {config.concurrency}",
        f"  Keep-Alive:   {'Yes' if config.keep_alive else 'No'}",
        "",
    ]

    # Add formatted summary
    lines.append(format_summary(metrics))

    # Optionally add raw output
    if include_raw:
        lines.extend([
            "",
            "",
            "RAW OUTPUT",
            "=" * 70,
            metrics.raw_output,
        ])

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def export_to_pdf(
    metrics: ABMetrics,
    config: ABTestConfig,
    filepath: str | Path
) -> None:
    """
    Export test results to a PDF file.

    Args:
        metrics: Parsed AB metrics
        config: Test configuration used
        filepath: Path to save the PDF file
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        raise ImportError(
            "مكتبة reportlab غير مثبتة. قم بتثبيتها باستخدام:\n"
            "pip install reportlab"
        )

    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Create PDF document
    doc = SimpleDocTemplate(
        str(filepath),
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontSize=20,
        spaceAfter=30,
        alignment=1  # Center
    )
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=20,
        textColor=colors.HexColor('#2563eb')
    )
    normal_style = styles['Normal']

    # Build content
    content = []

    # Title
    content.append(Paragraph("Load Test Report", title_style))
    content.append(Paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        normal_style
    ))
    content.append(Spacer(1, 20))

    # Test Configuration
    content.append(Paragraph("Test Configuration", heading_style))
    config_data = [
        ["URL", config.url],
        ["Total Requests", f"{config.requests:,}"],
        ["Concurrency", str(config.concurrency)],
        ["Keep-Alive", "Yes" if config.keep_alive else "No"],
    ]
    config_table = Table(config_data, colWidths=[4*cm, 10*cm])
    config_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
    ]))
    content.append(config_table)
    content.append(Spacer(1, 20))

    # Server Information
    content.append(Paragraph("Server Information", heading_style))
    server_data = [
        ["Server Software", metrics.server_software or "N/A"],
        ["Server Hostname", metrics.server_hostname or "N/A"],
        ["Server Port", str(metrics.server_port)],
        ["Document Path", metrics.document_path or "N/A"],
    ]
    server_table = Table(server_data, colWidths=[4*cm, 10*cm])
    server_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
    ]))
    content.append(server_table)
    content.append(Spacer(1, 20))

    # Performance Results
    content.append(Paragraph("Performance Results", heading_style))
    perf_data = [
        ["Requests/second", f"{metrics.requests_per_second:.2f} req/sec"],
        ["Time per request", f"{metrics.time_per_request:.3f} ms (mean)"],
        ["Transfer rate", f"{metrics.transfer_rate:.2f} KB/sec"],
        ["Total time", f"{metrics.time_taken:.3f} seconds"],
    ]
    perf_table = Table(perf_data, colWidths=[4*cm, 10*cm])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#dcfce7')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bbf7d0')),
    ]))
    content.append(perf_table)
    content.append(Spacer(1, 20))

    # Request Statistics
    content.append(Paragraph("Request Statistics", heading_style))
    stats_data = [
        ["Complete requests", f"{metrics.complete_requests:,}"],
        ["Failed requests", f"{metrics.failed_requests:,}"],
        ["Concurrency level", str(metrics.concurrency_level)],
        ["Total transferred", f"{metrics.total_transferred:,} bytes"],
        ["HTML transferred", f"{metrics.html_transferred:,} bytes"],
    ]
    stats_table = Table(stats_data, colWidths=[4*cm, 10*cm])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
    ]))
    content.append(stats_table)
    content.append(Spacer(1, 20))

    # Connection Times
    content.append(Paragraph("Connection Times (ms)", heading_style))
    times_data = [
        ["", "Min", "Mean", "Median", "Max"],
        ["Connect", f"{metrics.connect_min:.0f}", f"{metrics.connect_mean:.0f}",
         f"{metrics.connect_median:.1f}", f"{metrics.connect_max:.0f}"],
        ["Processing", f"{metrics.processing_min:.0f}", f"{metrics.processing_mean:.0f}",
         f"{metrics.processing_median:.1f}", f"{metrics.processing_max:.0f}"],
        ["Waiting", f"{metrics.waiting_min:.0f}", f"{metrics.waiting_mean:.0f}",
         f"{metrics.waiting_median:.1f}", f"{metrics.waiting_max:.0f}"],
        ["Total", f"{metrics.total_min:.0f}", f"{metrics.total_mean:.0f}",
         f"{metrics.total_median:.1f}", f"{metrics.total_max:.0f}"],
    ]
    times_table = Table(times_data, colWidths=[
                        3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    times_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f1f5f9')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ]))
    content.append(times_table)

    # Build PDF
    doc.build(content)


def get_default_filename(config: ABTestConfig, extension: str) -> str:
    """
    Generate a default filename for exports.

    Args:
        config: Test configuration
        extension: File extension (json or txt)

    Returns:
        str: Generated filename
    """
    # Extract hostname from URL
    from urllib.parse import urlparse
    parsed = urlparse(config.url)
    hostname = parsed.hostname or "unknown"

    # Create timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Clean hostname for filename
    clean_hostname = hostname.replace('.', '_')

    return f"ab_test_{clean_hostname}_{timestamp}.{extension}"


if __name__ == "__main__":
    # Test export functionality
    from parser import ABOutputParser

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
"""

    parser = ABOutputParser()
    metrics = parser.parse(sample_output)

    config = ABTestConfig(
        url="https://example.com/",
        requests=1000,
        concurrency=10,
        keep_alive=True
    )

    # Test exports
    export_to_json(metrics, config, "test_export.json")
    export_to_txt(metrics, config, "test_export.txt")

    print("Exports created successfully!")
