#!/usr/bin/env python3
import json

def generate_routing_proxy():
    """
    Вариант 1.
    Трафик, соответствующий доменам из geosite (например, geosite:antizapret)
    и IP-сетям из geoip (например, geoip:antifilter) направляется через прокси ("proxy").
    Остальной трафик (TCP, UDP, DNS) идет напрямую ("direct").
    """
    config = {
        "routing": {
            "domainStrategy": "IPIfNonMatch",
            "rules": [
                # Если домен попадает в geosite:antizapret – через прокси.
                {
                    "type": "field",
                    "domain": [
                        "geosite:antizapret"
                    ],
                    "outboundTag": "proxy"
                },
                # Если IP входит в диапазоны из geoip:antifilter – через прокси.
                {
                    "type": "field",
                    "ip": [
                        "geoip:antifilter"
                    ],
                    "outboundTag": "proxy"
                },
                # Если протокол является DNS (например, при использовании sniffing), и ни одно из вышеуказанных правил не сработало,
                # направляем DNS-запросы напрямую.
                {
                    "type": "field",
                    "protocol": [
                        "dns"
                    ],
                    "outboundTag": "direct"
                },
                # Остальной трафик направляем напрямую.
                {
                    "type": "field",
                    "ip": [
                        "0.0.0.0/0",
                        "::/0"
                    ],
                    "outboundTag": "direct"
                }
            ]
        }
    }
    return config

def generate_routing_adguard():
    """
    Вариант 2.
    Сначала все DNS-запросы перенаправляются через outbound "adguard-dns".
    При этом для доменов (geosite:antizapret) и IP из geoip:antifilter установлена отправка через "proxy",
    а остальной трафик (кроме DNS) проходит напрямую ("direct").

    В данном варианте ключевое правило:
      {
          "type": "field",
          "protocol": [ "dns" ],
          "outboundTag": "adguard-dns"
      }
    Оно гарантирует, что любой DNS-трафик сразу будет направлен в outbound с тегом "adguard-dns".
    При этом предполагается, что outbound "adguard-dns" настроен на localhost (где работает hiddify).
    """
    config = {
        "routing": {
            "domainStrategy": "IPIfNonMatch",
            "rules": [
                # Все DNS-запросы сразу перенаправляем через AdGuard DNS (работает на localhost).
                {
                    "type": "field",
                    "protocol": [
                        "dns"
                    ],
                    "outboundTag": "adguard-dns"
                },
                # Если домен попадает в geosite:antizapret – через прокси.
                {
                    "type": "field",
                    "domain": [
                        "geosite:antizapret"
                    ],
                    "outboundTag": "proxy"
                },
                # Если IP входит в диапазоны из geoip:antifilter – через прокси.
                {
                    "type": "field",
                    "ip": [
                        "geoip:antifilter"
                    ],
                    "outboundTag": "proxy"
                },
                # Остальной трафик направляем напрямую.
                {
                    "type": "field",
                    "ip": [
                        "0.0.0.0/0",
                        "::/0"
                    ],
                    "outboundTag": "direct"
                }
            ]
        }
    }
    return config

def save_config(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Файл {filename} успешно сгенерирован!")

def main():
    # Генерируем вариант маршрутизации без перенаправления DNS через AdGuard.
    routing_proxy = generate_routing_proxy()
    save_config(routing_proxy, "routing_proxy.json")

    # Генерируем вариант маршрутизации с перенаправлением всех DNS через AdGuard DNS.
    routing_adguard = generate_routing_adguard()
    save_config(routing_adguard, "routing_adguard.json")

if __name__ == "__main__":
    main()
