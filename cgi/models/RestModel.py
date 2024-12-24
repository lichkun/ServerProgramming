class RestModel:
    def __init__(self, status=200, meta=None, data=None):
        self.status = status if isinstance(status, RestStatus) else RestStatus(status)
        self.meta = meta if isinstance(meta, RestMeta) else RestMeta(meta or {})
        self.data = data

    def to_json(self):
        return {
            'status': self.status.to_json(),
            'meta': self.meta.to_json(),
            'data': self.data
        }


class RestStatus:
    def __init__(self, status_code: int, reason_phrase: str = None, is_success: bool | None = None):
        if not isinstance(status_code, int):
            raise ValueError("status_code must be an integer")
        self.statusCode = status_code
        self.reasonPhrase = reason_phrase if reason_phrase is not None else self.phrase_by_code(status_code)
        self.isSuccess = is_success if is_success is not None else status_code < 400

    def to_json(self):
        return {
            'statusCode': self.statusCode,
            'reasonPhrase': self.reasonPhrase,
            'isSuccess': self.isSuccess
        }

    def phrase_by_code(self, status_code: int) -> str:
        match status_code:
            case 200: return "OK"
            case 405: return "Method Not Allowed"
            case 415: return "Unsupported Media Type"
            case _: return "Unknown Status"


class RestMeta:
    def __init__(self, meta):
        if not isinstance(meta, dict):
            raise ValueError("meta must be a dictionary")
        self.meta = meta

    def to_json(self):
        return self.meta

    def add(self, key, value):
        self.meta[key] = value
