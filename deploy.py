import zipfile
import os

def create_deployment_package():
    """Cria pacote ZIP para deploy no Elastic Beanstalk"""
    
    files_to_include = [
        'application.py',
        'app.py', 
        'requirements.txt',
        'templates/index.html',
        '.ebextensions/python.config'
    ]
    
    with zipfile.ZipFile('classificador-descarte.zip', 'w') as zipf:
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file)
                print(f"Adicionado: {file}")
    
    print("\nPacote criado: classificador-descarte.zip")
    print("\nPróximos passos:")
    print("1. Acesse AWS Console > Elastic Beanstalk")
    print("2. Clique em 'Create Application'")
    print("3. Nome: classificador-descarte")
    print("4. Platform: Python 3.9")
    print("5. Upload classificador-descarte.zip")
    print("6. Clique em 'Create application'")

if __name__ == "__main__":
    create_deployment_package()