from testimonials import db
from dataclasses import dataclass


@dataclass
class Testimonial(db.Model):
    id: int
    name: str
    testimonial: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    testimonial = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'{self.name} says {self.testimonial}'
