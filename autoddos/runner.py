import asyncio
import aiohttp
from protocols import attack_http, attack_https, attack_ssh, attack_tcp
from scanner import scan_ports_and_protocols

import signal

class GracefulKiller:
    def __init__(self):
        self.kill_now = False
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, self.exit)

    def exit(self):
        print("\nПолучен сигнал остановки. Завершаю задачи...")
        self.kill_now = True

async def run_load(url, ports, protocols, interval_base, concurrency=10):
    killer = GracefulKiller()
    sem = asyncio.Semaphore(concurrency)
    tasks = []

    async def limited_attack(coro_func, *args):
        async with sem:
            await coro_func(*args)

    async with aiohttp.ClientSession() as session:
        for port in ports:
            interval = interval_base * len(ports) / 10
            proto = protocols.get(port, "tcp")

            if proto == "http":
                coro = limited_attack(attack_http, session, url, port, interval)
            elif proto == "https":
                coro = limited_attack(attack_https, session, url, port, interval)
            elif proto == "ssh":
                coro = limited_attack(attack_ssh, url, port, interval)
            else:
                coro = limited_attack(attack_tcp, url, port, interval)

            task = asyncio.create_task(coro)
            tasks.append(task)

        while not killer.kill_now:
            await asyncio.sleep(0.1)

        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        print("Все задачи остановлены.")

async def main(url, start_port, end_port, interval, concurrency):
    print(f"Сканируем порты {start_port}-{end_port} на {url}...")
    ports, protocols = await scan_ports_and_protocols(url, start_port, end_port)
    if not ports:
        print("Открытых портов не найдено.")
        return

    print(f"Найдены открытые порты: {', '.join(map(str, ports))}")
    print(f"Протоколы: {protocols}")
    print(f"Запускаем нагрузку с {concurrency} потоками и интервалом {interval} сек.")
    await run_load(url, ports, protocols, interval, concurrency)

def run(url, start_port, end_port, interval, concurrency):
    asyncio.run(main(url, start_port, end_port, interval, concurrency))
