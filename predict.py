import torch
import os
from openai import OpenAI
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, models
from PIL import Image
from .imagenet1000 import class_mapping
class Network(nn.Module):
  def __init__(self):
    super(Network, self).__init__()
    # Image size = 32x32x3 N/B the 3 is the depth i.e R, G, B color channel
    self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
    self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
    self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
    self.pool = nn.MaxPool2d(2, 2)
    self.fc1 = nn.Linear(64 * 28 * 28, 500)
    self.fc2 = nn.Linear(500, 10)
    self.dropout = nn.Dropout(p=0.25)
  def forward(self, x):                  #if we resize the size of the image to be 224
    x = self.pool(F.relu(self.conv1(x))) #output size = 112x112
    x = self.pool(F.relu(self.conv2(x))) #output size = 56x56
    x = self.pool(F.relu(self.conv3(x))) #output size = 28x28
    # Flatten the result
    x = x.view(-1, 64 * 28 * 28) #input here is (-1, 64 * 28 * 28)
    x = self.dropout(x)
    x = F.relu(self.fc1(x))
    x = self.dropout(x)
    x = self.fc2(x)
    return x

# Load the pretrained model
model_path = '/Users/chidubemonwuchuluba/Desktop/djangostuff/waste_app/app/waste_model.pth' #Change this to your own path
model = Network()
model.load_state_dict(torch.load(model_path))
model.eval()
# The optimized model already trained
model3 = models.resnet101(weights='ResNet101_Weights.DEFAULT')
# The transformation the images would undergo
transform2 = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
# The architecture of the optimized model
class ResNet50(nn.Module):
    def __init__(self, num_classes=10):
        super(ResNet50, self).__init__()
        # Load pre-trained ResNet50 model
        resnet50 = models.resnet50(pretrained=True)  
        # Keep the feature extractor layers
        self.features = nn.Sequential(*list(resnet50.children())[:-1])
        # Modify the classification layer
        self.fc = nn.Linear(resnet50.fc.in_features, num_classes)
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return x

# This is the function to classify the image
def predict_item(image_path):
    dict = {
    'water bottle': 'plastic',
    'running shoe': 'shoes',
    'envelope': 'paper',
    'jersey, T-shirt, tee shirt': 'cloth',
    'plastic bag': 'trash',
    'carton': 'cardboard',
    'screw': 'metal',
    'cup': 'glass',
    }
    model3 = models.resnet101(weights='ResNet101_Weights.DEFAULT')
    image = Image.open(image_path)
    input_tensor = transform2(image)
    input_batch = input_tensor.unsqueeze(0)
    # Now to make predictions
    model3.eval()
    with torch.no_grad():
        predictions = model3(input_batch)
        predicted_class_index = torch.argmax(predictions).item()
        predicted_class_name = class_mapping.get(predicted_class_index, "Unknown")
        if predicted_class_name not in dict:
            item_name = "Item was not trained with the model"
        else:
            item_name = dict[predicted_class_name]
        object = item_name
        api_key = "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"
        client = OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"how can {object} be recycled!"}
          ]
        )
        method_of_recycling = completion.choices[0].message.content
        return item_name, method_of_recycling
        