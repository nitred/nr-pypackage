"""RESTful {{ current_table_name }} Blueprint."""
import os
import traceback
from sqlalchemy.orm.exc import NoResultFound

from flask import (Blueprint, Response, jsonify, redirect, render_template,
                   request, url_for)

from flask_restful import Resource
from {{ package_name_safe }}.service.database.{{ current_table_name_lower }} import {{ current_table_name_lower }}_api


class {{ current_table_name }}API(Resource):

    def get(self):
        """Get."""
        params = request.args.to_dict()
        try:
            {{ current_table_name_lower }}_objs = {{ current_table_name_lower }}_api.get_{{ current_table_name_lower }}s(**params)
            {{ current_table_name_lower }}_json = [
                {{ current_table_name_lower }}_obj.to_dict()
                for {{ current_table_name_lower }}_obj in {{ current_table_name_lower }}_objs
            ]
            return jsonify({{ current_table_name_lower }}_json)
        except Exception as ex:
            print(traceback.format_exc())
            return False, 500

    def post(self):
        """Post."""
        data = request.form.to_dict()
        try:
            {{ current_table_name_lower }}_obj = {{ current_table_name_lower }}_api.register_{{ current_table_name_lower }}(**data)

            if {{ current_table_name_lower }}_obj:
                return jsonify({{ current_table_name_lower }}_obj.to_dict())
            else:
                return False, 400
        except Exception as ex:
            print(traceback.format_exc())
            return False, 500

    def patch(self):
        """Patch/Update."""
        data = request.form.to_dict()
        try:
            {{ current_table_name_lower }}_obj = {{ current_table_name_lower }}_api.update_{{ current_table_name_lower }}(**data)

            if {{ current_table_name_lower }}_obj:
                return jsonify({{ current_table_name_lower }}_obj.to_dict())
            else:
                return False, 400
        except Exception as ex:
            print(traceback.format_exc())
            return False, 500

    def delete(self):
        """Delete."""
        params = request.args.to_dict()
        try:
            {{ current_table_name_lower }}_obj = {{ current_table_name_lower }}_api.deregister_{{ current_table_name_lower }}(**params)

            if {{ current_table_name_lower }}_obj:
                return jsonify([{'id': {{ current_table_name_lower }}_obj.id}])
            else:
                raise NoResultFound
        except NoResultFound as ex:
            return "NoResultFound", 404
        except Exception as ex:
            print(traceback.format_exc())
            return "Error", 500
