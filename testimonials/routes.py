from testimonials import app, db
from flask import render_template, abort, jsonify, request
from testimonials.models import Testimonial


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
