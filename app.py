from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    # Contoh logika Python
    angka1 = int(data['angka1'])
    angka2 = int(data['angka2'])
    hasil = angka1 + angka2
    
    return jsonify({'result': hasil})

@app.route('/process-text', methods=['POST'])
def process_text():
    data = request.json
    text = data['text']
    
    # Logika Python: hitung jumlah kata
    jumlah_kata = len(text.split())
    text_upper = text.upper()
    
    return jsonify({
        'jumlah_kata': jumlah_kata,
        'text_upper': text_upper
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 