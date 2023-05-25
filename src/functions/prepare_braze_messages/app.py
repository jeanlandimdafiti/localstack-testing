def lambda_handler(event, context):
    map_countries = {
        "BR": "BRAZIL",
        "AR": "ARGENTINA",
        "CO": "COLOMBIA",
        "CH": "CHILE",
    }

    messages = []
    recipients = []

    for user in event["audience"]:
        recipient = {
                    "user_alias": {
                        "alias_label": f"{event['store']} {map_countries[event['country']]}"
                        if event["store"] == "DAFITI" else event["store"],
                        "alias_name": user
                    }
                }

        recipients.append(recipient)

    def divide_recipients(recipients_list, n):
        for i in range(0, len(recipients_list), n):
            yield recipients_list[i:i + n]

    # Separate the list with the recipients into chunks according to the objects_limit
    recipients_chunks = list(divide_recipients(recipients, event["braze"]["objects_limit"]))

    for recipients in recipients_chunks:
        message = {
            "MessageAttributes": {
                "Action": "canvas_trigger_send"
            },
            "MessageBody": {
                "canvas_id": event["braze"]["canvas_id"],
                "recipients": recipients
            }
        }

        messages.append(message)

    return messages
