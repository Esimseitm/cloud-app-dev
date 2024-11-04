gcloud ai models upload \
--region=us-central1 \
--display-name=saved_model \
--artifact-uri=gs://cloud-app-dev-bucket/models/saved_model.pb \
--container-image-uri=us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-8:latest

gcloud ai models versions create v1 \
--model=model0id \
--region=us-central1 \
--runtime-version=2.8 \
--python-version=3.8 \
--origin=gs://your-bucket-name/model/ \
--machine-type=n1-standard-4
