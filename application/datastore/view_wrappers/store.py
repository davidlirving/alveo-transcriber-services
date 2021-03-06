from flask import abort, g, jsonify, request

from application.misc.query_wrapper import QueryWrapper


class StoreWrapper(QueryWrapper):
    def get(self, object_id, version=None):
        if object_id is None:
            abort(400, "store_id not provided or invalid")

        if version != None:
            try:
                version = int(version)
            except:
                abort(400, "Provided version is not a valid integer")

        response = self._processor_get(
            object_id=object_id,
            user_id=g.user.id,
            version=version
        )
        return jsonify(response)

    def post(self):
        data = request.get_json()
        key = None
        value = None
        storage_spec = None
        alias = None

        try:
            key = data['key']
            value = data['value']
            storage_spec = data['storage_spec']
            alias = data['alias']
        except BaseException:
            if key is None:
                abort(400, "key not provided or invalid")

            if value is None:
                abort(400, "value not provided or invalid")

            if storage_spec is None:
                abort(400, "storage_spec not provided")

        response = self._processor_post(
            key=key,
            value=value,
            storage_spec=storage_spec,
            alias=alias
        )
        return jsonify(response)
