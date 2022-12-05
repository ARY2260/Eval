from app import db
from dataclasses import dataclass


@dataclass
class Answers(db.Model):
  q_category: int
  answer1: str
  answer2: str
  answer3: str
  answer4: str
  answer5: str

  question: str

  q_category = db.Column(db.Integer, primary_key=True)
  answer1 = db.Column(db.String(255), unique=False, nullable=False)
  answer2 = db.Column(db.String(255), unique=False, nullable=False)
  answer3 = db.Column(db.String(255), unique=False, nullable=False)
  answer4 = db.Column(db.String(255), unique=False, nullable=False)
  answer5 = db.Column(db.String(255), unique=False, nullable=False)
  question = db.Column(db.String(255), unique=False, nullable=False)

  def __init__(self, answer1, answer2, answer3, answer4, answer5, question):
    self.answer1 = answer1
    self.answer2 = answer2
    self.answer3 = answer3
    self.answer4 = answer4
    self.answer5 = answer5

    self.question = question

  def __repr__(self):
    return str(self.q_category)


def create(answer1, answer2, answer3, answer4, answer5, question):
  answerMain = Answers(answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4, answer5=answer5, question=question)
  db.session.add(answerMain)
  db.session.commit()


def delete(answer_id):
  answerMain = Answers.query.filter_by(q_category=answer_id).first()
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
