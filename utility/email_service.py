import os

from mailjet_rest import Client


class EmailService:
    api_key = os.environ['MAILJET_API_KEY']
    api_secret = os.environ['MAILJET_API_SECRET']

    def __init__(self, receiver: str, subject: str):
        self.receiver = receiver
        self.subject = subject

        self.mailjet = Client(auth=(self.api_key, self.api_secret), version='v3.1')

    def send_upload_success(self, total: int):
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "efocoder@gmail.com",
                        "Name": "efocoder.com"
                    },
                    "To": [
                        {
                            "Email": self.receiver,
                            "Name": self.receiver
                        }
                    ],
                    "Subject": self.subject,
                    "HTMLPart": f"""
                                <h4>{self.receiver}r</h4>
                                <p>Your upload of {total} icd codes was successful</p>
                            """,
                    "CustomID": "MESSAGEFROMCLIENT"
                }
            ]
        }

        result = self.mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
