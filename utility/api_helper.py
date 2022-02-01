from rest_framework.response import Response

STATUSES = (
    ('ACTIVE', 'ACTIVE'),
    ('DELETED', 'DELETED')
)


def api_response(status: int, message: str, data: any = None, login: bool = False):
    resp = {
        "status": status,
        "message": message,
    }

    if data is not None:
        resp['output'] = data

    response = Response(resp, status=status)

    if login:
        response = response.__dict__.pop('data')

    return response
