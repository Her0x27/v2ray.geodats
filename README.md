# v2ray.geodats
# Автоматическая генерация geosite.dat и geoip.dat

Данный репозиторий использует GitHub Actions для автоматической генерации двух файлов:

- **geosite.dat** – на основе списка доменов из [domains.lst](https://antifilter.download/list/domains.lst). Все домены сохраняются под тегом `antizapret`.
- **geoip.dat** – на основе списка IP-сетей из [allyouneed.lst](https://antifilter.download/list/allyouneed.lst). IP-сети сохраняются под тегом `antifilter`.

## Как это работает

Каждый день (а также при ручном запуске через кнопку "Run workflow") GitHub Actions загружает свежие данные, генерирует файлы и коммитит их в репозиторий.

Файлы генерируются с помощью скрипта [generate_dat.py](generate_dat.py) – он скачивает исходные данные, обрабатывает их и сохраняет в виде JSON.

## Использование

В конфигурации вашего клиента (например, V2Ray или V2Fly) вы можете ссылаться на созданный ресурс через ссылки вида `geosite:antizapret` и `geoip:antifilter`.
