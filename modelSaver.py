import tensorflow as tf
import tensorflow_hub as hub
import os

model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"

save_dir = './saved_model'

def download_and_save_model():
    print("Downloading model...")
    model = hub.load(model_url)
    print("Model downloaded successfully.")
    tf.saved_model.save(model, save_dir)
    print(f"Model saved to {save_dir}")

if __name__ == "__main__":
    download_and_save_model()
