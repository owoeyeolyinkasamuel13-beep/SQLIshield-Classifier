from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np

# Load trained CNN
model = load_model("sql_injection_cnn_model.h5", compile=False)

# Load tokenizer
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Load label encoder
labels = ['Error-Based', 'None_Type', 'Time-Based', 'Union-Based',
          'boolean-based', 'meta_based', 'stackqueries_based']

# Load settings
with open("model_settings.pkl", "rb") as f:
    settings = pickle.load(f)

max_len = settings["max_len"]

print("Model files loaded successfully.\n")

sample = ["SELECT * FROM users UNION SELECT username,password FROM admin"]

seq = tokenizer.texts_to_sequences(sample)
padded = pad_sequences(seq, maxlen=max_len, padding='post', truncating='post')

prediction = model.predict(padded)

predicted_index = prediction.argmax(axis=1)[0]
confidence = float(prediction[0][predicted_index])
attack_type = labels[predicted_index]

print("Predicted index:", predicted_index)
print("Attack type:", attack_type)
print("Confidence:", round(confidence, 2))
print("Raw prediction:", prediction)