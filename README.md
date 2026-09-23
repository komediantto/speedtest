# Internet Speed Test

Простой Python-скрипт для замера скорости скачивания с компьютера.


## Установка

```bash
git clone https://github.com/komediantto/internet-speed-test.git
cd internet-speed-test
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

Можно передать URL достаточно большого файла или изображения(по умолчанию уже есть ссылка на файл):

```bash
python speedtest.py "https://example.com/large-file.jpg"
```

Можно изменить timeout:

```bash
python speedtest.py "https://example.com/large-file.jpg" --timeout 120
```
