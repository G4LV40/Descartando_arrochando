from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from app import ObjectClassifier

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

classifier = ObjectClassifier()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify_image():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            result = classifier.classify_image(filepath)
            
            descarte_info = {
                'organico': 'Descarte em lixeira orgânica ou compostagem',
                'plastico': 'Descarte em lixeira de recicláveis (plástico)',
                'papel': 'Descarte em lixeira de recicláveis (papel)',
                'metal': 'Descarte em lixeira de recicláveis (metal)',
                'vidro': 'Descarte em lixeira de recicláveis (vidro)',
                'nao_identificado': 'Consulte manual de descarte local'
            }
            
            result['descarte'] = descarte_info[result['categoria']]
            
            os.remove(filepath)  # Remove arquivo após processamento
            return jsonify(result)
            
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Erro ao processar imagem: {str(e)}'}), 500
    
    return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

if __name__ == '__main__':
    app.run(debug=True)