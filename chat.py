import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

with open("intents.json", "r") as f:
    intents = json.load(f)

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

exit_commands = ["exit", "quit", "stop", "end", "leave", "terminate"]

bot = "Baymax"
print("My name is Doc Ammy! What would you like to chat about today!")

def make_exit(sentence):
    for exit in exit_commands:
      if exit in sentence:
        print("Thanks for chatting! I hope you feel a little better!\n")
        return True

sentence = "" 
while not make_exit(sentence): 
    sentence = input('You: ')
    
    sentence = tokenize(sentence)
    x = bag_of_words(sentence, all_words)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x).to(device)
    
    output = model(x)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                print(f"{bot}: {random.choice(intent['responses'])}")
    else:
        print(f"{bot}: I apologize but I can't help you with that... if it's an emergency please reach out to emergency services immediately.")
    