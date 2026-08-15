"""System diagnostics with Jedi flavor."""

import subprocess
import os
from typing import Optional


def get_cpu_usage() -> Optional[str]:
    """Get current CPU usage percentage."""
    try:
        result = subprocess.run(
            ['top', '-bn1'],
            capture_output=True,
            text=True,
            timeout=5
        )
        for line in result.stdout.split('\n'):
            if 'Cpu(s)' in line:
                cpu_pct = line.split(':')[1].split(',')[0].strip()
                return f"{cpu_pct}%"
        return None
    except Exception:
        return None


def get_memory_usage() -> Optional[dict]:
    """Get memory usage information."""
    try:
        result = subprocess.run(
            ['free', '-m'],
            capture_output=True,
            text=True,
            timeout=5
        )
        lines = result.stdout.split('\n')
        if len(lines) >= 2:
            parts = lines[1].split()
            return {
                'total': int(parts[1]),
                'used': int(parts[2]),
                'available': int(parts[6]) if len(parts) > 6 else int(parts[3]),
                'unit': 'MB'
            }
        return None
    except Exception:
        return None


def get_disk_usage() -> Optional[dict]:
    """Get disk usage for root partition."""
    try:
        result = subprocess.run(
            ['df', '-h', '/'],
            capture_output=True,
            text=True,
            timeout=5
        )
        lines = result.stdout.split('\n')
        if len(lines) >= 2:
            parts = lines[1].split()
            return {
                'size': parts[1],
                'used': parts[2],
                'available': parts[3],
                'percent': parts[4],
                'mount': parts[5]
            }
        return None
    except Exception:
        return None


def get_uptime() -> Optional[str]:
    """Get system uptime."""
    try:
        result = subprocess.run(
            ['uptime', '-p'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return None


def get_load_average() -> Optional[dict]:
    """Get system load averages."""
    try:
        load1, load5, load15 = os.getloadavg()
        return {
            '1min': f"{load1:.2f}",
            '5min': f"{load5:.2f}",
            '15min': f"{load15:.2f}"
        }
    except Exception:
        return None


def get_network_interfaces() -> list[dict]:
    """Get network interface information."""
    try:
        result = subprocess.run(
            ['ip', '-j', 'addr', 'show'],
            capture_output=True,
            text=True,
            timeout=5
        )
        import json
        interfaces = json.loads(result.stdout)
        return [
            {
                'name': iface.get('ifname', ''),
                'state': iface.get('operstate', 'UNKNOWN'),
                'address': next(
                    (addr.get('local', '') for addr in iface.get('addr_info', []) 
                     if addr.get('family') == 'inet'),
                    ''
                )
            }
            for iface in interfaces
        ]
    except Exception:
        return []


def get_all_diagnostics() -> dict:
    """Collect all system diagnostics."""
    return {
        'cpu': get_cpu_usage(),
        'memory': get_memory_usage(),
        'disk': get_disk_usage(),
        'uptime': get_uptime(),
        'load': get_load_average(),
        'network': get_network_interfaces()
    }
