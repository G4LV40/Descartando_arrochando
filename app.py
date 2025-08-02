import cv2
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import json

class ObjectClassifier:
    def __init__(self):
        self.model = MobileNetV2(weights='imagenet')
        self.categories = {
            'organico': ['banana', 'apple', 'orange', 'broccoli', 'carrot', 'pizza', 'sandwich'],
            'plastico': ['bottle', 'cup', 'container', 'bag'],
            'papel': ['book', 'newspaper', 'cardboard', 'envelope'],
            'metal': ['can', 'fork', 'knife', 'spoon', 'scissors'],
            'vidro': ['wine_glass', 'beer_glass', 'vase', 'mirror']
        }
    
    def preprocess_image(self, img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        return preprocess_input(img_array)
    
    def predict_object(self, img_path):
        processed_img = self.preprocess_image(img_path)
        predictions = self.model.predict(processed_img)
        decoded = decode_predictions(predictions, top=3)[0]
        return decoded
    
    def categorize_object(self, predictions):
        for pred in predictions:
            object_name = pred[1].lower()
            for category, items in self.categories.items():
                if any(item in object_name for item in items):
                    return {
                        'categoria': category,
                        'objeto': pred[1],
                        'confianca': float(pred[2])
                    }
        return {
            'categoria': 'nao_identificado',
            'objeto': predictions[0][1],
            'confianca': float(predictions[0][2])
        }
    
    def classify_image(self, img_path):
        predictions = self.predict_object(img_path)
        result = self.categorize_object(predictions)
        return result

def main():
    classifier = ObjectClassifier()
    
    # Exemplo de uso
    img_path = input("Digite o caminho da imagem: ")
    try:
        result = classifier.classify_image(img_path)
        print(f"\nResultado:")
        print(f"Categoria: {result['categoria']}")
        print(f"Objeto: {result['objeto']}")
        print(f"Confiança: {result['confianca']:.2%}")
        
        # Sugestões de descarte
        descarte_info = {
            'organico': 'Descarte em lixeira orgânica ou compostagem',
            'plastico': 'Descarte em lixeira de recicláveis (plástico)',
            'papel': 'Descarte em lixeira de recicláveis (papel)',
            'metal': 'Descarte em lixeira de recicláveis (metal)',
            'vidro': 'Descarte em lixeira de recicláveis (vidro)',
            'nao_identificado': 'Consulte manual de descarte local'
        }
        
        print(f"Descarte: {descarte_info[result['categoria']]}")
        
    except Exception as e:
        print(f"Erro ao processar imagem: {e}")

if __name__ == "__main__":
    main()