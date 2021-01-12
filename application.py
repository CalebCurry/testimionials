from flask import Flask

app = Flask(__name__)
application = app


@app.route('/')
def index():
    return 'hello'


@app.route('/api/testimonials')
def testimonials():
    return {'testimonial': ['great', 'its ok', ]}
