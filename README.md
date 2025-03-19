### [ Автоматическая генерация геоданных и конфигураций маршрутизации ]

## Данный репозиторий содержит:
- Скрипты для генерации файлов геоданных:
  - `geosite.dat` – на основе списка доменов из [domains.lst](https://antifilter.download/list/domains.lst) с тегом `antizapret`.
  - `geoip.dat` – на основе списка IP-сетей из [allyouneed.lst](https://antifilter.download/list/allyouneed.lst) с тегом `antifilter`.
- Скрипт `generate_routing.py` для создания двух вариантов конфигураций routing:
  - `routing_proxy.json` – маршрутизация, где домены и IP, заданные в геоданных, направляются через прокси (`proxy`), остальной трафик идёт напрямую.
  - `routing_adguard.json` – аналогичная маршрутизация, но все DNS-запросы перераспределяются через локальный сервер AdGuard DNS (`adguard-dns`).
- Workflow GitHub Actions для автоматической генерации и коммита обновленных конфигураций по расписанию или вручную.

## Настройка outbound
Убедитесь, что в основном файле V2Ray/V2Fly (например, `config.json`) присутствует outbound с тегом `adguard-dns`, настроенный для работы с локальным AdGuard DNS-сервером:
```json
{
  "tag": "adguard-dns",
  "protocol": "dns",
  "settings": {
    "network": "udp",
    "address": "127.0.0.1",
    "port": 53,
    "queryStrategy": "UseIPv4"
  }
}
```

## Примечания по безопасности
- Если ваша основная ветка защищена, убедитесь, что GitHub Actions имеет соответствующие разрешения для прямых коммитов или настройте автоматическое создание pull-request.
- При необходимости можно использовать персональный токен (PAT) вместо `GITHUB_TOKEN`.

## Запуск
GitHub Actions автоматически запустится по расписанию или можно запустить workflow вручную через вкладку Actions в репозитории.
