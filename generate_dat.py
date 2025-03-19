#!/usr/bin/env python3
import requests
import json

DOMAINS_URL = "https://antifilter.download/list/domains.lst"
ALLYOUNEED_URL = "https://antifilter.download/list/allyouneed.lst"

GEOSITE_OUTPUT_FILE = "geosite.dat"
GEOIP_OUTPUT_FILE = "geoip.dat"

def download_lines(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text.splitlines()

def process_domains(lines):
    domains = []
    for line in lines:
        line = line.strip()
        # Пропускаем пустые строки и комментарии
        if not line or line.startswith("#"):
            continue
        domains.append(line)
    return sorted(domains)

def process_ip_ranges(lines):
    ip_ranges = []
    for line in lines:
        line = line.strip()
        # Пропускаем пустые строки и комментарии
        if not line or line.startswith("#"):
            continue
        ip_ranges.append(line)
    return sorted(ip_ranges)

def generate_geosite(domains, tag="antizapret"):
    # Формат geosite.dat (версия 1)
    data = {
        "version": "1",
        "entries": [
            {
                "tag": tag,
                "domains": domains,
                "attributes": {}
            }
        ]
    }
    return data

def generate_geoip(ip_ranges, tag="antifilter"):
    # Для geoip.dat определяем простую JSON-структуру с IP-сетями
    data = {
        "version": "1",
        "entries": [
            {
                "tag": tag,
                "ips": ip_ranges
            }
        ]
    }
    return data

def main():
    try:
        # Генерация geosite.dat
        print("Скачивание списка доменов из domains.lst...")
        domain_lines = download_lines(DOMAINS_URL)
        domains = process_domains(domain_lines)
        print(f"Найдено доменов: {len(domains)}")
        geosite_data = generate_geosite(domains)

        with open(GEOSITE_OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(geosite_data, f, indent=2, ensure_ascii=False)
        print(f"{GEOSITE_OUTPUT_FILE} успешно сгенерирован!")

        # Генерация geoip.dat
        print("Скачивание списка IP-сетей из allyouneed.lst...")
        ip_lines = download_lines(ALLYOUNEED_URL)
        ip_ranges = process_ip_ranges(ip_lines)
        print(f"Найдено IP-сетей: {len(ip_ranges)}")
        geoip_data = generate_geoip(ip_ranges)

        with open(GEOIP_OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(geoip_data, f, indent=2, ensure_ascii=False)
        print(f"{GEOIP_OUTPUT_FILE} успешно сгенерирован!")

    except Exception as e:
        print("Ошибка при генерации:", e)

if __name__ == "__main__":
    main()
    
