from flask import Flask, request, jsonify
import sql

app = Flask(__name__)
@app.route('/api/v1', methods=['GET'])
def handle_get():
    param = request.args.get('email')
    title,text=sql.email_code(param)
    return jsonify({'email': param,'title':title,'text':text})

if __name__ == '__main__':
    app.run(debug=True)

