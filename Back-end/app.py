from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from urllib.parse import quote

app = Flask(__name__)
CORS(app)  # Enable CORS

# Encode the password
password = quote('Riya@nit<3')

# Configure SQLAlchemy with PostgreSQL connection details
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://postgres:{password}@localhost:5423/Todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.ARRAY(db.String(1000)), default=list)

with app.app_context():
    db.create_all()

def check_user_reminders(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return []

    reminders = []
    current_time = datetime.now().time()

    for note in user.notes:
        try:
            item, note_time_str = note.split('#')
            note_time = datetime.strptime(note_time_str, '%H:%M').time()

            # Calculate time difference in seconds
            time_diff = (datetime.combine(datetime.today(), note_time) - datetime.combine(datetime.today(), current_time)).total_seconds()

            # Check if note time is within 1 hour from current time
            if 0 < time_diff <= 3600:
                reminders.append({'item': item, 'time': note_time_str})
        except ValueError:
            continue

    return reminders

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/myacc/signup', methods=['POST'])
def signup():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'id': new_user.id}), 201

@app.route('/myacc/get', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'password': user.password, 'notes': user.notes} for user in users]
    return jsonify(user_list), 200

@app.route('/myacc', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({'message': 'Login successful', 'id': user.id}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 200

from sqlalchemy import text
from flask import jsonify

@app.route('/myacc/<int:user_id>/addnote', methods=['POST'])
def add_note_to_user(user_id):
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Content is required'}), 400


    query = text("UPDATE users SET notes = array_append(notes, :content) WHERE id = :user_id")
    db.session.execute(query, {'content': content, 'user_id': user_id})
    db.session.commit()

    return jsonify({'message': 'Note added successfully'}), 200

@app.route('/myacc/<int:user_id>/fetch', methods=['GET'])
def fetch_notes(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'notes': user.notes}), 200



@app.route('/myacc/<int:user_id>/deletenote/<int:note_index>', methods=['DELETE'])
def delete_note_from_user(user_id, note_index):
    try:
        user = User.query.filter_by(id=user_id).one()
    except NoResultFound:
        return jsonify({'error': 'User not found'}), 404

    if note_index < 0 or note_index >= len(user.notes):
        return jsonify({'error': 'Invalid note index'}), 400

    # Remove the note at note_index
    deleted_note = user.notes.pop(note_index)

    try:
        sql = text("UPDATE users SET notes = :updated_notes WHERE id = :user_id")
        db.session.execute(sql, {'updated_notes': user.notes, 'user_id': user_id})
        db.session.commit()
        db.session.commit()

        return jsonify({'message': f'Note "{deleted_note}" deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/myacc/<int:user_id>/reminders', methods=['GET'])
def get_user_reminders(user_id):
    reminders = check_user_reminders(user_id)
    return jsonify({'reminders': reminders}), 200 if reminders else 204

if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=5000)
