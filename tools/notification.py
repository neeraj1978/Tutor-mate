class NotificationTool:
    def __init__(self):
        pass

    def send_email(self, to_email: str, subject: str, body: str):
        """
        Simulates sending an email.
        """
        print(f"--- EMAIL NOTIFICATION ---")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print(f"--------------------------")
        return True
