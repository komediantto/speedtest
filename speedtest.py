import argparse
import statistics
import time
from dataclasses import dataclass

import requests


REQUESTS_COUNT = 10


@dataclass
class Result:
    elapsed_time: float
    bytes_downloaded: int

    @property
    def mb_per_sec(self) -> float:
        return self.bytes_downloaded / 1024 / 1024 / self.elapsed_time if self.elapsed_time else 0.0


def download_once(url: str, timeout: float) -> Result:
    started = time.perf_counter()
    downloaded = 0

    with requests.get(
        url,
        stream=True,
        timeout=timeout,
        headers={"Accept-Encoding": "identity"},
    ) as response:
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                downloaded += len(chunk)

    return Result(time.perf_counter() - started, downloaded)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Скачивает ресурс 10 раз и замеряет скорость"
    )
    parser.add_argument("url", help="URL файла большого размера для скачивания", default="http://212.183.159.230/512MB.zip", nargs="?")
    parser.add_argument(
        "--timeout",
        type=float,
        default=60,
        help="Таймаут запроса в секундах (default: 60)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results: list[Result] = []

    print(f"URL: {args.url}")
    print(f"Requests: {REQUESTS_COUNT}")
    print()

    for number in range(1, REQUESTS_COUNT + 1):
        try:
            result = download_once(args.url, args.timeout)
        except requests.RequestException as exc:
            print(f"[{number:2}/{REQUESTS_COUNT}] ERROR: {exc}")
            continue

        results.append(result)
        print(
            f"[{number:2}/{REQUESTS_COUNT}] "
            f"{result.bytes_downloaded / 1024 / 1024:.2f} MB, "
            f"{result.elapsed_time:.3f} s, "
            f"{result.mb_per_sec:.2f} MB/s"
        )

    if not results:
        raise SystemExit("All requests failed.")

    total_bytes = sum(result.bytes_downloaded for result in results)
    total_time = sum(result.elapsed_time for result in results)
    average_time = statistics.mean(result.elapsed_time for result in results)
    speed = total_bytes / 1024 / 1024 / total_time if total_time else 0.0

    print("\n--- Итоги ---")
    print(f"Успешных запросов: {len(results)}/{REQUESTS_COUNT}")
    print(f"Среднее время запроса: {average_time:.3f} s")
    print(f"Загружено: {total_bytes / 1024 / 1024:.2f} MB")
    print(f"Средняя скорость загрузки: {speed:.2f} MB/s")


if __name__ == "__main__":
    main()
