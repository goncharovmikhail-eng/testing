import argparse
from runner import run

def main():
    parser = argparse.ArgumentParser(description="autoddos — асинхронная нагрузка на сервер с автосканированием")
    parser.add_argument("url", help="URL или IP адрес")
    parser.add_argument("--start-port", type=int, default=20, help="Начальный порт (включительно)")
    parser.add_argument("--end-port", type=int, default=100, help="Конечный порт (включительно)")
    parser.add_argument("--interval", type=float, default=0.1, help="Базовый интервал между запросами (сек)")
    parser.add_argument("--threads", type=int, default=10, help="Максимальное количество параллельных задач")
    args = parser.parse_args()

    run(args.url, args.start_port, args.end_port, args.interval, args.threads)

if __name__ == "__main__":
    main()
