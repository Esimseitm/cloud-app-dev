import functions_framework

def send_notification(request):
    request_json = request.get_json(silent=True)
    if request_json and 'message' in request_json:
        message = request_json['message']
        print(f"Notification sent: {message}")
        return "Notification sent successfully.", 200
    else:
        return "Invalid request. Please provide a message.", 400
