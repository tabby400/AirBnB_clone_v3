#!/usr/bin/python3
"""objects handling all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, request, jsonify


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["GET"])
def amenity(amenity_id=None):
    """showing the amenity and amenity with id"""
    amenity_list = []
    if amenity_id is None:
        all_objs = storage.all(Amenity).values()
        for v in all_objs:
            amenity_list.append(v.to_dict())
        return jsonify(amenity_list)
    else:
        result = storage.get(Amenity, amenity_id)
        if result is None:
            abort(404)
        return jsonify(result.to_dict())  # json fmt


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def amenity_delete(amenity_id):
    """the deleting method"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def create_amenity():
    """creating new post request"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def update_amenity(amenity_id):
    """updating the amenity"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200
