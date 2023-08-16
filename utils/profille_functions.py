from mongo import Database


db = Database()


def get_rate_status(x: int) -> str:
    if x < 100:
        return "Новичок"
    elif 100 <= x < 500:
        return "Спамер"
    elif 500 <= x < 1000:
        return "Мейкер"
    elif x >= 1000:
        return "Легенда"


def get_ref_percent(x: int) -> int:
    if x < 100:
        return 5

    elif 100 <= x < 500:
        return 10

    elif 500 <= x < 1000:
        return 15

    elif x >= 1000:
        return 20


def get_price(x: int) -> float:
    if x < 100:
        return 1.5

    elif 100 <= x < 500:
        return 1.5

    elif 500 <= x < 1000:
        return 1.25

    elif x >= 1000:
        return 1


def get_reqs(user_id):
    try:
        requisites = db.user_info(user_id)['requisites']
        return requisites
    except KeyError:
        requisites = "Не указан"
        return requisites
