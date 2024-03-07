from flask import Flask, request, jsonify
import torch
import json
from model import NeuralNet
from nltk_utils import tokenize, bag_of_words
import random

app = Flask(__name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load intents
with open("app.json", "r") as json_data:
    intents = json.load(json_data)

# Load trained model data
data = torch.load("data.pth")
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    sentence = request.json['sentence']
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])
                return jsonify({"response": response})
    return jsonify({"response": "I apologize but I can't help you with that... if it's an emergency please reach out to emergency services immediately."})

if __name__ == '__main__':
    app.run(debug=True)
