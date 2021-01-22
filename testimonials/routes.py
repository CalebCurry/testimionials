from testimonials import app, db, bcrypt, jwt
from flask import render_template, abort, jsonify, request
from testimonials.models import Testimonial, User
from flask_jwt_extended import jwt_required, create_access_token


@app.route('/api/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = bcrypt.generate_password_hash(
        data.get('password')).decode('utf-8')

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.id)


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user:
        return {'error': 'username or password incorrect'}, 400

    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={'username': username})
        return {'access_token': access_token}

    else:
        return {'error': 'username or password incorrect'}, 400


@app.route('/api/testimonials')
def get_testimonials():
    testimonials = Testimonial.query.all()
    return jsonify({'testimonials': testimonials})


@app.route('/api/testimonials/<id>')
def get_testimonial(id):
    testimonial = Testimonial.query.get(id)

    if testimonial:
        return jsonify(testimonial)

    return {}


@app.route('/api/testimonials', methods=['POST'])
def add_testimonial():
    data = request.get_json()
    testimonial = Testimonial(name=data.get(
        'name'), testimonial=data.get('testimonial'))
    db.session.add(testimonial)
    db.session.commit()
    return jsonify(testimonial.id)


@app.route('/api/testimonials/<id>', methods=['PUT', 'POST'])
@jwt_required
def update_testimonial(id):
    testimonial = Testimonial.query.get(id)

    if not testimonial:
        return {'error': 'testimonial does not exist'}, 400
    data = request.get_json()
    testimonial.name = data.get('name')
    testimonial.testimonial = data.get('testimonial')
    db.session.commit()
    return jsonify(testimonial)


@app.route('/api/testimonials/<id>', methods=['DELETE'])
@jwt_required
def delete_testimonial(id):
    testimonial = Testimonial.query.get(id)

    if not testimonial:
        return {'error': 'testimonial does not exist'}, 400

    db.session.delete(testimonial)
    db.session.commit()

    return {}


testimonials = [
    {
        'id': 10,
        'name': 'Connor',
        'message': 'Your courses helped me land a job at mcDonalds!'
    },
    {
        'id': 35,
        'name': 'Sarah',
        'message': 'Never have I understood OOP until now'
    },
    {
        'id': 43,
        'name': 'John',
        'message': 'I watched all 200 hours straight!'
    }
]


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="404 NOT FOUND"), 404


@app.route('/')
@app.route('/testimonials')
def show_testimonials():
    return render_template('index.html', testimonials=testimonials)


@app.route('/testimonials/<id>')
def show_testimonial(id):

    for testimonial in testimonials:
        if testimonial.get('id') == int(id):
            return render_template('testimonial.html', testimonial=testimonial)
    abort(404)
