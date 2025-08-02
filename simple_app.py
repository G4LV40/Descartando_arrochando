from flask import Flask, request, jsonify, render_template_string
import os
import json

app = Flask(__name__)

# Template HTML simples
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Classificador de Descarte</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        .upload { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; }
        .result { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🗂️ Classificador de Descarte</h1>
    <p>Aplicação para identificar objetos e categorizar para descarte adequado.</p>
    
    <div class="upload">
        <input type="file" id="file" accept="image/*">
        <button onclick="classify()">Classificar</button>
    </div>
    
    <div id="result"></div>

    <script>
        function classify() {
            const file = document.getElementById('file').files[0];
            if (!file) {
                alert('Selecione uma imagem');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            document.getElementById('result').innerHTML = '<p>Processando...</p>';
            
            fetch('/classify', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').innerHTML = `
                    <div class="result">
                        <h3>Resultado:</h3>
                        <p><strong>Categoria:</strong> ${data.categoria}</p>
                        <p><strong>Objeto:</strong> ${data.objeto}</p>
                        <p><strong>Descarte:</strong> ${data.descarte}</p>
                    </div>
                `;
            })
            .catch(error => {
                document.getElementById('result').innerHTML = '<p style="color:red;">Erro: ' + error + '</p>';
            });
        }
    </script>
</body>
</html>
'''

# Simulador simples de classificação
def simple_classify(filename):
    """Classificação simples baseada no nome do arquivo"""
    filename_lower = filename.lower()
    
    if any(word in filename_lower for word in ['apple', 'banana', 'food', 'fruit']):
        return {'categoria': 'organico', 'objeto': 'Fruta', 'descarte': 'Lixeira orgânica'}
    elif any(word in filename_lower for word in ['bottle', 'plastic', 'cup']):
        return {'categoria': 'plastico', 'objeto': 'Garrafa plástica', 'descarte': 'Lixeira de recicláveis (plástico)'}
    elif any(word in filename_lower for word in ['paper', 'book', 'cardboard']):
        return {'categoria': 'papel', 'objeto': 'Papel', 'descarte': 'Lixeira de recicláveis (papel)'}
    elif any(word in filename_lower for word in ['can', 'metal', 'fork']):
        return {'categoria': 'metal', 'objeto': 'Metal', 'descarte': 'Lixeira de recicláveis (metal)'}
    elif any(word in filename_lower for word in ['glass', 'bottle']):
        return {'categoria': 'vidro', 'objeto': 'Vidro', 'descarte': 'Lixeira de recicláveis (vidro)'}
    else:
        return {'categoria': 'nao_identificado', 'objeto': 'Objeto não identificado', 'descarte': 'Consulte manual local'}

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/classify', methods=['POST'])
def classify():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    # Simulação de classificação
    result = simple_classify(file.filename)
    return jsonify(result)

if __name__ == '__main__':
    print("Iniciando aplicação...")
    print("Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)