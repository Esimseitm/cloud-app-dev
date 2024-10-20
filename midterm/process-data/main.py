import functions_framework

def process_user_data(request):
    request_json = request.get_json(silent=True)
    if request_json and 'user_data' in request_json:
        user_data = request_json['user_data']
        print(f"Received user data: {user_data}")
        return "User data processed successfully.", 200
    else:
        return "Invalid request. Please provide user data.", 400
