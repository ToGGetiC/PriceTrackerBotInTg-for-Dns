import setuptools
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import re

def get_dns_prices_stealth(url):
    print("Запускаю невидимый браузер...")
    

    options = uc.ChromeOptions()

    driver = uc.Chrome(options=options)

    try:
        print(f"Перехожу на {url}")
        driver.get(url)
        
        print("Жду загрузки (имитирую чтение)...")
        time.sleep(10) 

        if "Forbidden" in driver.title or "Доступ запрещен" in driver.page_source:
            print("Упс! Нас всё равно узнали. Нужно менять тактику.")
            return []

        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        price_elements = soup.find_all(lambda tag: tag.name in ['div', 'span'] and '₽' in tag.text)
        
        prices = []
        for el in price_elements:
        
            text = el.get_text(strip=True)
        
            digits = "".join(re.findall(r'\d+', text))
            if digits and 3 < len(digits) < 7:
                prices.append(int(digits))
        
        return list(set(prices))

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []
    finally:
        print("Закрываю браузер через 5 секунд...")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    url = "https://www.dns-shop.ru/product/107598551b8183a5/gazovaa-varocnaa-poverhnost-midea-mg693tx/"
    res = get_dns_prices_stealth(url)
    print(f"Итоговый результат: {res}")