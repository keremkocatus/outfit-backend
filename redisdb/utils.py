import json

def is_indexable(value):
    return value not in (None, "null", "")


def sanitize_value(value):
    """
    Redis'e güvenli şekilde yazılabilecek tipe dönüştürür.
    
    - None   -> "null"
    - bool   -> "true"/"false"
    - dict   -> JSON string
    - list   -> JSON string
    - diğer  -> string/int/float
    """
    if value is None:
        return "null"

    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, (dict, list)):
        try:
            return json.dumps(value, ensure_ascii=False)
        except Exception:
            return str(value)

    return value


def restore_value(value):
    """
    Redis'ten okunan string değerlerini tekrar Python tipine çevirir.

    - "null"  -> None
    - "true"  -> True
    - "false" -> False
    - JSON    -> dict/list
    """
    if value == "null":
        return None
    if value == "true":
        return True
    if value == "false":
        return False

    # JSON parse etmeyi dene
    try:
        return json.loads(value)
    except Exception:
        return value


def restore_record(record: dict) -> dict:
    """
    Redis'ten dönen tüm key-value çiftlerini restore eder.
    """
    return {k: restore_value(v) for k, v in record.items()}
