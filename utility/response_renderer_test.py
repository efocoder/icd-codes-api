import json


def render_response_and_send_content(response):
    response.render()
    return json.loads(response.content)
