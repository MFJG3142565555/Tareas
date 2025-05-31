import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torchvision import transforms
import pickle

def guardar_modelo(model, le, ruta='modelo_emociones'):
    # Guardar modelo PyTorch
    torch.save(model.state_dict(), f'{ruta}.pth')
    # Guardar LabelEncoder
    with open(f'{ruta}_le.pkl', 'wb') as f:
        pickle.dump(le, f)

def cargar_modelo(ruta='modelo_emociones'):
    # Cargar modelo
    model = EmotionCNN(7)  # 7 emociones (ajusta según tu caso)
    model.load_state_dict(torch.load(f'{ruta}.pth'))
    model.to(DEVICE)
    # Cargar LabelEncoder
    with open(f'{ruta}_le.pkl', 'rb') as f:
        le = pickle.load(f)
    return model, le

# Configuración
DATASET_PATH = r"C:\Users\mateo\OneDrive\Desktop\Tec\zuripaps\unidad 4\dataset\DatasetPreProcesado"
IMG_SIZE = (48, 48)
BATCH_SIZE = 32
EPOCHS = 20
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Clase del modelo CNN
class EmotionCNN(nn.Module):
    def __init__(self, num_classes):
        super(EmotionCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(128 * 6 * 6, 512)
        self.fc2 = nn.Linear(512, num_classes)
        self.dropout = nn.Dropout(0.5)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = x.view(-1, 128 * 6 * 6)
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

# Carga de datos
def load_dataset():
    emotions = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    x = []
    y = []
    
    for emotion in emotions:
        emotion_path = os.path.join(DATASET_PATH, "train", emotion)
        for img_name in os.listdir(emotion_path):
            img_path = os.path.join(emotion_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, IMG_SIZE)
            x.append(img)
            y.append(emotion)
    
    x = np.array(x)
    y = np.array(y)
    
    le = LabelEncoder()
    y = le.fit_transform(y)
    
    # Convertir a tensores PyTorch
    x = torch.FloatTensor(x).unsqueeze(1) / 255.0
    y = torch.LongTensor(y)
    
    return x, y, le

# Entrenamiento
def train_model(model, train_loader, criterion, optimizer, epochs):
    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
        
        print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader):.4f}")

# Detección en tiempo real
def detect_emotions(model, le):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    model.eval()
    
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(IMG_SIZE),
        transforms.ToTensor()
    ])
    
    with torch.no_grad():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]
                img_tensor = transform(face_roi).unsqueeze(0).to(DEVICE)
                
                output = model(img_tensor)
                _, predicted = torch.max(output, 1)
                emotion = le.inverse_transform(predicted.cpu().numpy())[0]
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            
            cv2.imshow('Emotion Detection', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Verificar si existe modelo guardado
    if os.path.exists('modelo_emociones.pth'):
        print("Cargando modelo pre-entrenado...")
        model, le = cargar_modelo()
    else:
        print("Entrenando nuevo modelo...")
        print("Cargando dataset...")
        x, y, le = load_dataset()
        
        # Crear DataLoader
        dataset = TensorDataset(x, y)
        train_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
        
        print("Creando modelo...")
        model = EmotionCNN(len(le.classes_)).to(DEVICE)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters())
        
        print("Entrenando modelo...")
        train_model(model, train_loader, criterion, optimizer, EPOCHS)
        
        # Guardar modelo después de entrenar
        guardar_modelo(model, le)
    
    print("Iniciando detección...")
    detect_emotions(model, le)