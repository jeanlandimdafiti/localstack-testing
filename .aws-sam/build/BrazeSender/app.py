import requests

ENDPOINTS = {
    "canvas_trigger_send": "/canvas/trigger/send",
    "track_users": "/users/track",
    "new_user_alias": "/users/alias/new"
}


def _get_headers(bearer_key: str) -> dict:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_key}",
    }

def _send_to_braze(token: str, endpoint_uri: str, json_data: dict) -> "Response":
    headers = _get_headers(token) 

    return requests.post(f"https://{URL}{endpoint_uri}",
                          headers=headers, json=json_data)

def _get_rate_limit(request_type: str, response: "Response") -> dict:
    return {
        "request_type": request_type,
        "request_limit": response.headers["X-RateLimit-Limit"],
        "request_remaining": response.headers["X-RateLimit-Remaining"],
        "request_reset": response.headers["X-RateLimit-Reset"] 
    }    

def lambda_handler(event, context):
    endpoint_uri = ENDPOINTS[event["endpoint_name"]]
    json_data = event["message_body"] 

    response = _send_to_braze(token,
               endpoint_uri, json_data)
    request_type = event["endpoint_name"]

    return _get_rate_limit(request_type, response)