from flask import Flask, request, render_template, send_file
from PIL import Image, ImageDraw, ImageFont
import io
from jinja2.exceptions import TemplateNotFound
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test/<test_id>')
def test(test_id):
    template_name = f'test{test_id}.html'
    try:
        return render_template(template_name)
    except TemplateNotFound:
        return "Шаблон не найден", 404


@app.route('/result', methods=['POST'])
def result():
    answers = request.form
    print(answers) # Для отладки
    test_id = answers.get('test_id')
    factor_scores = {key: int(value) for key, value in answers.items() if key.startswith('factor')}
    
    if not factor_scores:
        return "Нет данных для отображения", 400
    question_titles = {key: "Вопрос " + key[-1] for key in factor_scores.keys()} 

    factors = sorted(factor_scores.keys())
    scores = [factor_scores[factor] for factor in factors]

    fig, ax = plt.subplots(figsize = (10, 8))
    ax.plot(scores, marker='o')

    for i, factor in enumerate(factors):
        title = question_titles[factor] 
        score = factor_scores[factor]  
        ax.annotate(f'{title}: {score}', (i, scores[i]), textcoords="offset points", xytext=(0,15), ha='center')

    
    ax.set_title('Профиль личности')
    ax.set_ylim(0, max(scores) + 1) 
    ax.set_xticks(range(len(factors)))
    ax.set_xticklabels(factors, rotation = 45)
    ax.set_ylabel('Баллы')
    ax.grid(True)

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png', bbox_inches='tight')
    img_io.seek(0)
    plt.close()
    
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

