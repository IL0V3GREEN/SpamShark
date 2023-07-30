
def check_bank(number: str):
    if number[12:] == "9146":
        return "Tinkoff"
    elif number[12:] == "1093":
        return "Tinkoff"
    elif number[12:] == "6075":
        return "Sberbank"
    elif number[12:] == "1223":
        return "QIWI Bank"
    elif number[12:] == "6615":
        return "Raiffeisen"
