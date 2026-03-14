import asyncio
from playwright.async_api import async_playwright
import csv

async def run():
    async with async_playwright() as p:
        # 1. Запускаем браузер (в фоновом режиме)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 2. Переходим на сайт (тренировочный магазин)
        print("Захожу на сайт...")
        await page.goto("https://books.toscrape.com")

        # 3. Собираем данные о товарах
        # Мы ищем все карточки товаров на странице
        products = await page.query_selector_all(".product_pod")
        
        results = []
        for product in products:
            # Извлекаем название
            title_element = await product.query_selector("h3 a")
            title = await title_element.get_attribute("title")
            
            # Извлекаем цену
            price_element = await product.query_selector(".price_color")
            price = await price_element.inner_text()
            
            results.append({"Название": title, "Цена": price})
            print(f"Нашел: {title} - {price}")

        # 4. Сохраняем в CSV (Excel его откроет)
        with open("result.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Название", "Цена"])
            writer.writeheader()
            writer.writerows(results)

        print("\nГотово! Данные сохранены в файл result.csv")
        await browser.close()

asyncio.run(run())