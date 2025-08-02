# Classificador de Descarte Q CLI AWS

Aplicação que identifica objetos em fotos e categoriza para descarte adequado usando visão computacional.

## Categorias
- **Orgânico**: Restos de comida, frutas, vegetais
- **Plástico**: Garrafas, copos, embalagens
- **Papel**: Livros, jornais, papelão
- **Metal**: Latas, talheres, utensílios
- **Vidro**: Copos, garrafas, espelhos

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

### Linha de comando:
```bash
python app.py
```

### Interface web:
```bash
python web_app.py
```
Acesse: http://localhost:5000

## Estrutura
- `app.py`: Classificador principal
- `web_app.py`: Interface web Flask
- `templates/index.html`: Interface do usuário
- `requirements.txt`: Dependências
