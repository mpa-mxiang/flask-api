from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kl;\'@localhost/flask-project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.get_json()

    new_data = Data(name=data['name'])

    db.session.add(new_data)
    db.session.commit()

    return jsonify({'message': 'Data added successfully'}), 201

@app.route('/get_data', methods=['GET'])
def get_data():
    data = Data.query.all()
    data_list = [{'id': item.id, 'name': item.name} for item in data]

    return jsonify({'data': data_list})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
