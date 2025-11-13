#!/usr/bin/env python3
"""
Simple direct IP recovery report (compact, one-line fields, English)

Usage: python3 simple_ip_report.py
"""

import socket
import subprocess
import platform
import sys
import ipaddress
import ssl
import time

# Optional: nicer geo/isp info if 'requests' is available
try:
    import requests
except Exception:
    requests = None

SOCKET_TIMEOUT = 3.0

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except Exception:
        return False

def ping_ok(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    cmd = ['ping', param, '1', ip]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=4)
        return p.returncode == 0
    except Exception:
        return False

def reverse_dns(ip):
    try:
        name, _, _ = socket.gethostbyaddr(ip)
        return name
    except Exception:
        return None

def check_port_open(ip, port, timeout=SOCKET_TIMEOUT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        res = s.connect_ex((ip, port))
        if res == 0:
            # attempt quick banner read (non-blocking short)
            try:
                s.settimeout(1.0)
                banner = s.recv(512).decode(errors='ignore').strip()
            except Exception:
                banner = ""
            s.close()
            return True, banner
        s.close()
    except Exception:
        pass
    return False, None

def try_ssl_cert(ip, ports=(443,465,993,995,8443,587)):
    for p in ports:
        try:
            ctx = ssl.create_default_context()
            # do not require hostname verification, connect by IP
            with ctx.wrap_socket(socket.socket(socket.AF_INET), server_hostname=None) as ss:
                ss.settimeout(4.0)
                ss.connect((ip, p))
                cert = ss.getpeercert()
                # get subject commonName if present
                subj = None
                for tup in cert.get('subject', ()):
                    for k,v in tup:
                        if k.lower() == 'commonname':
                            subj = v
                return True, p, subj or cert
        except Exception as e:
            last_err = e
            continue
    return False, None, str(last_err) if 'last_err' in locals() else "no TLS"

def ipinfo_lookup(ip):
    if not requests:
        return {}
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=4)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {}

def main():
    ip = input("Enter IPv4 address: ").strip()
    if not validate_ip(ip):
        print("Invalid IP. Exiting.")
        sys.exit(1)

    # Minimal, direct report lines (English)
    # 1) IP
    print(f"IP: {ip}")

    # 2) IP Type
    print("IP Type: ipv4" if ':' not in ip else "IP Type: ipv6")

    # 3) Ping
    p = ping_ok(ip)
    print(f"Ping: {'Succeed' if p else 'Failed'}")

    # 4) DNS (reverse)
    rd = reverse_dns(ip)
    print(f"DNS: {rd if rd else 'N/A'}")

    # 5) Port: 25 Status: Open Protocol: SMTP  (try port 25)
    open25, banner25 = check_port_open(ip, 25)
    proto = "SMTP"
    status_str = "Open" if open25 else "Closed"
    # if banner includes SMTP greet, keep a short excerpt
    banner_excerpt = ""
    if banner25:
        banner_excerpt = " | " + banner25.splitlines()[0][:120]
    print(f"Port: 25 Status: {status_str} Protocol: {proto}{banner_excerpt}")

    # 6) Host Country (via ipinfo)
    info = ipinfo_lookup(ip)
    country = info.get("country") or "N/A"
    print(f"Host Country: {country}")

    # 7) Host Name (reverse)
    print(f"Host Name: {rd if rd else 'N/A'}")

    # 8) Host ISP (org) - from ipinfo 'org' if available
    isp = info.get("org") or "N/A"
    print(f"Host ISP: {isp}")

    # 9) SSL Certificate Check (try common TLS ports) -> short result
    ssl_ok, ssl_port, ssl_info = try_ssl_cert(ip)
    if ssl_ok:
        # ssl_info might be subject string or full cert dict
        if isinstance(ssl_info, dict):
            cn = None
            for t in ssl_info.get('subject', ()):
                for k,v in t:
                    if k.lower() == 'commonname':
                        cn = v
            cn = cn or ssl_info.get('issuer')
            print(f"SSL Certificate: OK on port {ssl_port} | Subject: {cn}")
        else:
            print(f"SSL Certificate: OK on port {ssl_port} | {ssl_info}")
    else:
        # match example wording "SSL Certificate Check Failed: timed out"
        err = ssl_info or "timed out"
        print(f"SSL Certificate Check Failed: {err}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
