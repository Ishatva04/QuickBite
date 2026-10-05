import requests
from django.conf import settings






def send_whatsapp_invoice(
    phone_number,
    document_url,
    customer_name,
    order_id
):
    url = (
        f"https://graph.facebook.com/v23.0/"
        f"{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    )

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": "quickbite_invoice",
            "language": {
                "code": "en"
            },
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "document",
                            "document": {
                                "link": document_url
                            }
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "parameter_name": "customer_name",
                            "text": customer_name
                        },
                        {
                            "type": "text",
                            "parameter_name": "order_id",
                            "text": str(order_id)
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    return response