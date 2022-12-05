from app import app
import models.answers as answers
from flask import request, jsonify, after_this_request
from middlewares.is_admin import is_admin
from dotenv import load_dotenv
from flask_api import status
import pandas as pd
import cohere
from annoy import AnnoyIndex
import warnings
import os

warnings.filterwarnings('ignore')

api_key = os.getenv('COHERE_API')
load_dotenv()


@app.route('/answers', methods=['POST'])
@is_admin()
def add_answer():
  answer = request.json.get('answer')
  category = request.json.get('category')
  if not (answer and category):
    return jsonify({'message':
                    "Insufficient data"}), status.HTTP_400_BAD_REQUEST
  answers.create(
    answer=answer,
    category=category,
  )
  return jsonify({}), status.HTTP_201_CREATED


@app.route('/answers', methods=['GET'])
def get_answers():

  @after_this_request
  def add_header(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

  answersAll = answers.get_all()

  return jsonify(answersAll), status.HTTP_200_OK


@app.route('/evaluate', methods=['POST'])
def evaluate_answer():
  answerQuery = request.json.get('answer')
  categoryQuery = request.json.get('category')

  @after_this_request
  def add_header(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

  answersAll = answers.get_all()

  # testing prediction part
  df = pd.DataFrame(answersAll)
  df.drop('id', axis=1, inplace=True)
  print(df)
  co = cohere.Client(api_key)
  embeds = co.embed(texts=list(df['answer']), model='large',
                    truncate='LEFT').embeddings
  search_index = AnnoyIndex(len(embeds[0]), 'angular')

  # Add all the vectors to the search index
  for i in range(len(embeds)):
    search_index.add_item(i, embeds[i])
  search_index.build(10)  # 10 trees
  search_index.save('test.ann')

  user_input = [answerQuery]
  user_input_embeds = co.embed(texts=user_input,
                               model='large',
                               truncate='LEFT').embeddings

  similar_item_ids = search_index.get_nns_by_vector(user_input_embeds[0],
                                                    10,
                                                    include_distances=True)

  # Format and print the text and distances
  results = pd.DataFrame(
    data={
      'texts': df.iloc[similar_item_ids[0]]['answer'],
      'label': df.iloc[similar_item_ids[0]]['category'],
      'distance': similar_item_ids[1]
    })
  print(f"Question:'{user_input}'\nNearest neighbors:")

  mean_distance = results[results['label'] == int(
    categoryQuery)]['distance'].mean()
  if mean_distance < 1:
    return "The answer is correct " + str(mean_distance), status.HTTP_200_OK
  return "The answer is incorrect"
  # end testing
