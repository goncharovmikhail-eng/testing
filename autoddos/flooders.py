import socket
import requests
import time
import paramiko

def send_http_request(host, port):
    url = f"http://{host}:{port}"
    try:
        resp = requests.get(url, timeout=2)
        return f"HTTP {resp.status_code}"
    except Exception as e:
        return f"HTTP ошибка: {e}"

def send_https_request(host, port):
    url = f"https://{host}:{port}"
    try:
        resp = requests.get(url, timeout=2, verify=False)
        return f"HTTPS {resp.status_code}"
    except Exception as e:
        return f"HTTPS ошибка: {e}"

def send_raw_ping(host, port):
    try:
        with socket.create_connection((host, port), timeout=2) as sock:
            sock.sendall(b'ping\r\n')
            response = sock.recv(1024)
            return f"RAW ответ: {response.decode(errors='ignore').strip()}"
    except Exception as e:
        return f"RAW ошибка: {e}"

def ssh_handshake(host, port):
    try:
        transport = paramiko.Transport((host, port))
        transport.start_client(timeout=5)
        banner = transport.get_banner()
        transport.close()
        banner_str = banner.decode(errors='ignore') if banner else "нет"
        return f"SSH handshake успешен. Баннер: {banner_str}"
    except Exception as e:
        return f"SSH ошибка: {e}"

def run_protocol_flood(host, port, protocol, interval, stop_event):
    print(f"Начинаем нагрузку на порт {port} ({protocol})")
    while not stop_event.is_set():
        if protocol == "http":
            msg = send_http_request(host, port)
        elif protocol == "https":
            msg = send_https_request(host, port)
        elif protocol == "ssh":
            msg = ssh_handshake(host, port)
        else:
            msg = send_raw_ping(host, port)
        print(f"[{port}] {msg}")
        time.sleep(interval)
    print(f"Нагрузка на порт {port} остановлена.")
