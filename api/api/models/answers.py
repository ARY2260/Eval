from app import db
from dataclasses import dataclass


@dataclass
class Answers(db.Model):
  id: int
  answer: str
  category: str

  id = db.Column(db.Integer, primary_key=True)
  answer = db.Column(db.String(255), unique=False, nullable=False)
  category = db.Column(db.Integer)

  def __init__(self, answer, category):
    self.answer = answer
    self.category = category

  def __repr__(self):
    return str(self.id)


def create(answer, category):
  answerMain = Answers(answer=answer, category=category)
  db.session.add(answerMain)
  db.session.commit()


def delete(answer_id):
  answerMain = Answers.query.filter_by(id=answer_id).first()
  if answerMain:
    db.session.delete(answerMain)
    db.session.commit()


def delete_all():
  if Answers.query.first():
    Answers.query.delete()
    Answers.session.commit()


def get(answer_id):
  return Answers.query.filter_by(id=answer_id).first()


def get_all(size=-1):
  return Answers.query.all()
