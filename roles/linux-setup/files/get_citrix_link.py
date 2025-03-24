#!/usr/bin/env python3

import os
import platform
import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def get_geckodriver_path():
    # Controleer standaard locaties
    possible_paths = [
        '/usr/bin/geckodriver',
        '/usr/local/bin/geckodriver',
        '/usr/lib/firefox-geckodriver/geckodriver'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def get_citrix_download_url(package_type='deb'):
    try:
        arch_label = platform.machine()
        if arch_label == "x86_64":
            arch_label = "amd64"
        elif arch_label in ["aarch64", "arm64"]:
            arch_label = "arm64"
        else:
            print(f"❌ Onbekende architectuur: {arch_label}", file=sys.stderr)
            sys.exit(1)

        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")

        # Gebruik Firefox met geckodriver
        geckodriver_path = get_geckodriver_path()
        if geckodriver_path:
            print(f"Gebruik geckodriver op: {geckodriver_path}", file=sys.stderr)
            service = Service(executable_path=geckodriver_path)
            driver = webdriver.Firefox(service=service, options=firefox_options)
        else:
            print("Geckodriver niet gevonden, probeer automatische detectie", file=sys.stderr)
            driver = webdriver.Firefox(options=firefox_options)

        url = "https://www.citrix.com/downloads/workspace-app/linux/workspace-app-for-linux-latest.html"
        driver.get(url)

        try:
            # Zoek downloadlinks
            download_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "ctx-dl-link"))
            )

            # Zoek de juiste link voor de systeemarchitectuur
            download_url = None
            for element in download_elements:
                rel_link = element.get_attribute("rel")
                if arch_label in rel_link and f".{package_type}" in rel_link:
                    download_url = "https:" + rel_link
                    break

            if download_url:
                print(download_url)
            else:
                raise Exception(f"Geen .{package_type} package gevonden voor {arch_label}")

        except Exception as e:
            print(f"Er is een fout opgetreden: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            driver.quit()

    except Exception as e:
        print(f"Er is een fout opgetreden: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Bepaal package type op basis van command line argument
    package_type = 'rpm' if len(sys.argv) > 1 and sys.argv[1] == 'rpm' else 'deb'
    get_citrix_download_url(package_type)
