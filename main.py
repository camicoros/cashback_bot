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
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception as exc:
                return self.get_default_data()
        return self.get_default_data()

    @staticmethod
    def get_default_data() -> Dict:
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


if __name__ == "__main__":
    bot = CashbackBot()
    print(bot.data)
