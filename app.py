from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.get_json()

    if 'name' not in data:
        return jsonify({'error': 'Missing name parameter'}), 400

    new_item = Item(name=data['name'])
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'Item added successfully'}), 201

@app.route('/get_items', methods=['GET'])
def get_items():
    items = Item.query.all()
    item_list = [{'id': item.id, 'name': item.name} for item in items]
    return jsonify({'items': item_list})

# Use an application context to create the tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
