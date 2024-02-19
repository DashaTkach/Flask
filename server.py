import pydantic
from flask import Flask, jsonify, request
from flask.views import MethodView
from requests import Session

from models import Announcement

app = Flask("ann")


def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)

    except pydantic.ValidationError as er:
        error = er.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


def get_ann_by_id(ann_id: int):
    ann = request.session.get(Announcement, ann_id)
    if ann is None:
        raise HttpError(404, "your announcement not found")
    return ann


class UserView(MethodView):
    def get(self, ann_id):
        ann = get_ann_by_id(ann_id)
        return jsonify(ann.dict)

    def post(self):  #нужна проверка прав
        ann = Announcement(**request.json)
        request.session.add(ann)
        request.session.commit()
        return jsonify(ann.dict)

    def patch(self, ann_id): #нужна проверка прав
        ann = request.session.get(Announcement, ann_id)
        for key, value in request.json.items():  # почему здесь проверка?
            setattr(ann, key, value)
        request.session.commit()
        return jsonify(ann.dict)

    def delete(self, ann_id): #нужна проверка прав
        ann = get_ann_by_id(ann_id)
        request.session.delete(ann)
        request.session.commit()
        return jsonify({
            "status": "deleted"
        })


announcement_view = UserView.as_view("announcement")

app.add_url_rule("/ann/", view_func=announcement_view, methods=["POST"])
app.add_url_rule(
    "/ann/<int:ann_id>", view_func=announcement_view, methods=["GET", "PATCH", "DELETE"]
)

app.run()
