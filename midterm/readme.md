curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d '{"task": "Новая задача", "done": false, "user_data": "Информация о пользователе"}'

curl -X POST http://127.0.0.1:5000/send_notification -H "Content-Type: application/json" -d '{"message": "Уведомление отправлено"}'

curl -X POST https://cloud-app-dev-yessimseit2.ew.r.appspot.com/tasks -H "Content-Type: application/json" -d '{"task": "Train 4 ama", "done": false, "user_data": "Check working 1"}'

https://console.cloud.google.com/functions/details/europe-west1/process_user_data?project=cloud-app-dev-yessimseit2&tab=logs

https://console.cloud.google.com/functions/details/europe-west1/send_notification?project=cloud-app-dev-yessimseit2&tab=logs


