import shutil

from flask import jsonify
from flask_restplus import Resource

from ..api.screenshot_api import screenshot_namespace


@screenshot_namespace.route('/clear')
class Screenshot(Resource):
    def get(self):
        try:
            shutil.rmtree('/app/screenshots/authentication')
        except Exception as e:
            print("folder doesn't found")

        try:
            shutil.rmtree('/app/screenshots/task')
        except Exception as e:
            print("folder doesn't found")

        return jsonify({'message', 'remove success'})
