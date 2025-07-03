import asyncio
import aiohttp

async def check_port(url, port, timeout=1):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(url, port), timeout)
        writer.close()
        await writer.wait_closed()
        return True
    except:
        return False

async def detect_protocol_http(session, url, port):
    try:
        async with session.get(f"http://{url}:{port}", timeout=2) as resp:
            if resp.status < 400:
                return "http"
    except:
        pass
    return None

async def detect_protocol_https(session, url, port):
    try:
        async with session.get(f"https://{url}:{port}", ssl=True, timeout=2) as resp:
            if resp.status < 400:
                return "https"
    except:
        pass
    return None

async def detect_protocol_ssh(url, port):
    try:
        reader, writer = await asyncio.open_connection(url, port)
        banner = await asyncio.wait_for(reader.read(100), timeout=2)
        writer.close()
        await writer.wait_closed()
        if banner.startswith(b'SSH'):
            return "ssh"
    except:
        pass
    return None

async def scan_ports_and_protocols(url, start_port, end_port):
    open_ports = []
    protocols = {}
    async with aiohttp.ClientSession() as session:
        for port in range(start_port, end_port + 1):
            if await check_port(url, port):
                proto = None
                for check_proto in (detect_protocol_http, detect_protocol_https):
                    proto = await check_proto(session, url, port)
                    if proto:
                        break
                if not proto:
                    proto = await detect_protocol_ssh(url, port)
                if not proto:
                    proto = "tcp"
                open_ports.append(port)
                protocols[port] = proto
    return open_ports, protocols
