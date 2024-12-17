import threading

# Run the subscriber in a separate thread
def run_subscriber():
    listen_for_payment_notifications()

if __name__ == '__main__':
    # Start the subscriber thread
    subscriber_thread = threading.Thread(target=run_subscriber)
    subscriber_thread.start()
    
    # Run the Flask app
    app.run(debug=True)
