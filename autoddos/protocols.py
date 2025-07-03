import asyncio
import aiohttp
import time

async def attack_http(session, url, port, interval):
    base_url = f"http://{url}:{port}"
    count = 0
    try:
        while True:
            start = time.time()
            try:
                async with session.get(base_url) as resp:
                    dt = time.time() - start
                    count += 1
                    print(f"[HTTP {port}] [{count}] {resp.status} за {dt:.3f} сек")
            except Exception as e:
                print(f"[HTTP {port}] Ошибка: {e}")
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        print(f"[HTTP {port}] Остановка нагрузки")

async def attack_https(session, url, port, interval):
    base_url = f"https://{url}:{port}"
    count = 0
    try:
        while True:
            start = time.time()
            try:
                async with session.get(base_url, ssl=True) as resp:
                    dt = time.time() - start
                    count += 1
                    print(f"[HTTPS {port}] [{count}] {resp.status} за {dt:.3f} сек")
            except Exception as e:
                print(f"[HTTPS {port}] Ошибка: {e}")
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        print(f"[HTTPS {port}] Остановка нагрузки")

async def attack_ssh(url, port, interval):
    count = 0
    try:
        while True:
            try:
                reader, writer = await asyncio.open_connection(url, port)
                # Ждём баннер SSH (обычно сразу приходит)
                banner = await asyncio.wait_for(reader.read(100), timeout=2)
                count += 1
                print(f"[SSH {port}] [{count}] Баннер: {banner.decode(errors='ignore').strip()}")
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                print(f"[SSH {port}] Ошибка: {e}")
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        print(f"[SSH {port}] Остановка нагрузки")

async def attack_tcp(url, port, interval):
    count = 0
    try:
        while True:
            start = time.time()
            try:
                reader, writer = await asyncio.open_connection(url, port)
                dt = time.time() - start
                count += 1
                print(f"[TCP {port}] [{count}] Успешное подключение за {dt:.3f} сек")
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                print(f"[TCP {port}] Ошибка: {e}")
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        print(f"[TCP {port}] Остановка нагрузки")
