from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = Item(name=data['name'])

    try:
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item added successfully!'}), 201
    except:
        return jsonify({'message': 'Error adding item.'}), 500

@app.route('/get_items', methods=['GET'])
def get_items():
    items = Item.query.all()
    item_list = []
    for item in items:
        item_list.append({'name': item.name})
    return jsonify({'items': item_list})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
