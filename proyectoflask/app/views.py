#app/views.py

from flask import render_template
from app import app, data

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask,jsonify,send_from_directory
from marshmallow import Schema, fields
from datetime import date

spec = APISpec(
    title='Flask-api-swagger-doc',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(),MarshmallowPlugin()]
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/articles')
def articles():
    articles_list = data.Articles()
    return render_template('articles.html', articles=articles_list)

@app.route('/article<article>')
def articleBase(article):
    return render_template('articlesBase.html',article=article)

@app.route('/api/swagger.json')
def create_swagger_spec():
            return jsonify(spec.to_dict())

class ArticleResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    body = fields.Str()
    author = fields.Str()
    create_date = fields.Str()

class ArticleListResponseSchema(Schema):
    article_list = fields.List(fields.Nested(ArticleResponseSchema))

@app.route('/articles2')
def article():
    """Get List of Articles
        ---
        get:
            description: Get List of Articles
            responses:
                200:
                    description: Return an article list
                    content:
                        application/json:
                            schema: ArticleListResponseSchema
    """
    resultado = data.Articles()

    return ArticleListResponseSchema().dump({'article_list':resultado})

with app.test_request_context():
        spec.path(view=article)

@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'swagger.html':
        return render_template('swagger.html',base_url='/docs')
    else:
        return send_from_directory('static',path)
