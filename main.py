""""
CASHBACK TELEGRAM BOT
"""
import json
import os.path
from datetime import datetime
from typing import Dict


DATA_FILE = "cashback_data.json"


class CashbackBot:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self) -> Dict:
        """
        Загрузка данных из файла
        :return: словарь с данными о кешбеках
        """
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception as exc:
                return self.get_default_data()
        return self.get_default_data()

    @staticmethod
    def get_default_data() -> Dict:
        """
        Получение данных по умолчанию
        :return: словарь с данными о кешбеках по умолчанию
        """
        current_month = datetime.now().strftime("%Y-%m")
        return {
            "banks": {
                "t-bank": {
                    "categories": {
                        "Рестораны": 5,
                        "АЗС": 3,
                        "Такси": 5
                    }
                },
                "sber": {
                    "categories": {
                        "Аптеки": 3,
                        "Одежда": 2
                    }
                },
                "alfa": {
                    "categories": {
                        "АЗС": 4,
                        "Такси": 5,
                        "Одежда": 1
                    }
                }
            },
            "last_update": current_month
        }

    def save_data(self) -> None:
        """
        Сохранение данных в файл
        :return:
        """
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=2)

    def get_cashback_info(self, bank: str = None, category: str = None) -> str:
        """
        Получение данных о кешбеке
        :return: Форматированный вывод с данными о кешбеках
        """
        result = []

        if bank and bank in self.data.get("banks", dict()):
            # информация по конкретному банку
            all_bank_categories = self.data["banks"][bank].get("categories", dict())
            if category and category in all_bank_categories:
                # информация по конкретной категории
                result.append(f"*{bank}*\n" + "_" * 30)
                result.append(f" - {category}: %{self.data["banks"][bank].get("categories", {}).get(category)}")
            elif not category:
                # информация по всем категориям
                result.append(f"*{bank}*\n" + "_" * 30)
                for category, percent in sorted(all_bank_categories.items()):
                    result.append(f" - {category}: %{percent}")
        elif not bank:
            # информация по всем банкам
            for bank_name, bank_data in self.data.get("banks", dict()).items():
                # информация по конкретному банку
                all_bank_categories = bank_data.get("categories", dict())
                if category and category in all_bank_categories:
                    # информация по конкретной категории
                    result.append(f"*{bank_name}*\n" + "_" * 30)
                    result.append(f" - {category}: %{bank_data.get("categories", {}).get(category)}")
                elif not category:
                    # информация по всем категориям
                    result.append(f"*{bank_name}*\n" + "_" * 30)
                    for category, percent in sorted(all_bank_categories.items()):
                        result.append(f" - {category}: %{percent}")

        if not result:
            return "Данные не найдены"

        result.append(f"\n Обновлено: {self.data.get("last_update")}\n")
        return "\n".join(result)


if __name__ == "__main__":
    bot = CashbackBot()
    print(bot.data)
    bot.save_data()
    print("общая информация")
    print(bot.get_cashback_info())
    print("sber информация")
    print(bot.get_cashback_info("sber"))
    print("vtb информация")
    print(bot.get_cashback_info("vtb"))
    print("sber-Аптеки информация")
    print(bot.get_cashback_info("sber", "Аптеки"))
    print("sber-Сладости информация")
    print(bot.get_cashback_info("sber", "Сладости"))
    print("Аптеки информация")
    print(bot.get_cashback_info(category="Аптеки"))
    print("Сладости информация")
    print(bot.get_cashback_info(category="Сладости"))
