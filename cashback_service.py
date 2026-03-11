""""
CASHBACK TELEGRAM BOT
"""
import json
import os.path
from datetime import datetime
from typing import Dict, List


DATA_FILE = "cashback_data.json"


class CashbackService:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self) -> Dict:
        """
        Загрузка данных из файла
        :return: словарь с данными о кешбэках
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
        :return: словарь с данными о кешбэках по умолчанию
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
        :param bank: банк
        :param category: категория кешбэка
        Получение данных о кешбэке
        :return: Форматированный вывод с данными о кешбэках
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

    def get_categories_list(self, bank: str) -> List[str]:
        """
        Получение списка категорий для банка
        :param bank: банк
        :return: Список категорий конкретного банка
        """
        if bank in self.data.get("banks", dict()):
            return list(self.data.get("banks").get(bank, dict()).get("categories").keys())
        return []

    def update_cashback(self, bank: str, category: str, percent: float) -> bool:
        """
        Обновление значения кешбэка
        :param bank: банк
        :param category: категория кешбэка
        :param percent: проценты
        :return: Категория кешбэка обновлена
        """
        if bank in self.data.get("banks", dict()):
            if category in self.data.get("banks", dict()).get(bank, dict()).get("categories", dict()):
                self.data.get("banks").get(bank).get("categories")[category] = percent
                self.data["last_update"] = datetime.now().strftime("%Y-%m")
                self.save_data()
                return True
        return False

    def add_bank(self, bank_name: str) -> bool:
        """
        Добавление нового банка
        :param bank_name: название банка
        :return: банк добавлен
        """
        if bank_name not in self.data.get("banks"):
            self.data.get("banks")[bank_name] = {"categories": {}}
            self.save_data()
            return True
        return False

    def add_category(self, bank: str, category: str, percent: float) -> bool:
        """
        Добавление категории кешбэка
        :param bank: банк
        :param category: категория кешбэка
        :param percent: проценты
        :return: Категория кешбэка добавлена
        """
        if bank in self.data.get("banks", dict()):
            if category not in self.data.get("banks", dict()).get(bank, dict()).get("categories", dict()):
                self.data.get("banks").get(bank).get("categories")[category] = percent
                self.data["last_update"] = datetime.now().strftime("%Y-%m")
                self.save_data()
                return True
        return False

    def delete_bank(self, bank_name: str) -> bool:
        """
        Удаление банка
        :param bank_name: название банка
        :return: банк удален
        """
        if bank_name in self.data.get("banks"):
            del self.data.get("banks")[bank_name]
            self.save_data()
            return True
        return False

    def delete_category(self, bank: str, category: str) -> bool:
        """
        Удаление категории кешбэка
        :param bank: банк
        :param category: категория кешбэка
        :return: Категория кешбэка удалена
        """
        if bank in self.data.get("banks", dict()):
            if category in self.data.get("banks", dict()).get(bank, dict()).get("categories", dict()):
                del self.data.get("banks").get(bank).get("categories")[category]
                self.data["last_update"] = datetime.now().strftime("%Y-%m")
                self.save_data()
                return True
        return False


if __name__ == "__main__":
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    bot = CashbackService()
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
    print("get_categories_list sber")
    print(bot.get_categories_list("sber"))
    print("get_categories_list vtb")
    print(bot.get_categories_list("vtb"))
    print("update_cashback sber Аптеки 10")
    print(bot.update_cashback("sber", "Аптеки", 10))
    print("update_cashback sber Сладости 10")
    print(bot.update_cashback("sber", "Сладости", 10))
    print("add_bank vtb")
    print(bot.add_bank("vtb"))
    print("add_bank sber")
    print(bot.add_bank("sber"))
    print("add_category sber Топливо")
    print(bot.add_category("sber", "Топливо", 5))
    print("add_category sber Аптеки")
    print(bot.add_category("sber", "Аптеки", 5))
    print("delete_bank vtb")
    print(bot.delete_bank("vtb"))
    print("delete_bank psb")
    print(bot.delete_bank("psb"))
    print("delete_category sber Топливо")
    print(bot.delete_category("sber", "Топливо"))
    print("delete_category sber Театр")
    print(bot.delete_category("sber", "Театр"))
