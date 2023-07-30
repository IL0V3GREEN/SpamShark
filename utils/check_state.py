async def check_text(data):
    try:
        text = data['text']
        if text != "":
            return True
        else:
            return False
    except KeyError:
        return False


async def check_media(data):
    try:
        text = data['media']
        if text != "":
            return True
        else:
            return False
    except KeyError:
        return False


async def check_inline(data):
    try:
        text = data['inline']
        if text != "":
            return True
        else:
            return False
    except KeyError:
        return False
