import http.server
import socketserver
import urllib.parse
import json
import os

class ClassifierHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Classificador de Descarte</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }
        .upload { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; }
        .result { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        input[type="text"] { width: 300px; padding: 10px; margin: 10px; }
    </style>
</head>
<body>
    <h1>🗂️ Classificador de Descarte</h1>
    <p>Digite o nome do objeto para classificação (demo):</p>
    
    <div class="upload">
        <input type="text" id="objectName" placeholder="Ex: apple, bottle, paper, can, glass">
        <br><br>
        <button onclick="classify()">Classificar</button>
    </div>
    
    <div id="result"></div>

    <script>
        function classify() {
            const objectName = document.getElementById('objectName').value;
            if (!objectName) {
                alert('Digite o nome de um objeto');
                return;
            }
            
            document.getElementById('result').innerHTML = '<p>Processando...</p>';
            
            fetch('/classify?object=' + encodeURIComponent(objectName))
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
            self.wfile.write(html.encode())
        
        elif self.path.startswith('/classify'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            object_name = params.get('object', [''])[0].lower()
            
            # Classificação simples
            result = self.simple_classify(object_name)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        
        else:
            self.send_error(404)
    
    def simple_classify(self, object_name):
        """Classificação simples baseada no nome"""
        if any(word in object_name for word in ['apple', 'banana', 'food', 'fruit', 'orange', 'vegetable']):
            return {
                'categoria': 'ORGÂNICO',
                'objeto': 'Alimento orgânico',
                'descarte': 'Descarte em lixeira orgânica ou compostagem'
            }
        elif any(word in object_name for word in ['bottle', 'plastic', 'cup', 'bag']):
            return {
                'categoria': 'PLÁSTICO',
                'objeto': 'Material plástico',
                'descarte': 'Descarte em lixeira de recicláveis (plástico)'
            }
        elif any(word in object_name for word in ['paper', 'book', 'cardboard', 'newspaper']):
            return {
                'categoria': 'PAPEL',
                'objeto': 'Material de papel',
                'descarte': 'Descarte em lixeira de recicláveis (papel)'
            }
        elif any(word in object_name for word in ['can', 'metal', 'fork', 'knife', 'aluminum']):
            return {
                'categoria': 'METAL',
                'objeto': 'Material metálico',
                'descarte': 'Descarte em lixeira de recicláveis (metal)'
            }
        elif any(word in object_name for word in ['glass', 'mirror', 'wine']):
            return {
                'categoria': 'VIDRO',
                'objeto': 'Material de vidro',
                'descarte': 'Descarte em lixeira de recicláveis (vidro)'
            }
        else:
            return {
                'categoria': 'NÃO IDENTIFICADO',
                'objeto': 'Objeto não reconhecido',
                'descarte': 'Consulte manual de descarte local'
            }

def run_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), ClassifierHandler) as httpd:
        print(f"Aplicacao rodando em: http://localhost:{PORT}")
        print("Pressione Ctrl+C para parar")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nAplicacao encerrada")

if __name__ == "__main__":
    run_server()