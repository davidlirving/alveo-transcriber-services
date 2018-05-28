from flask import abort, g, jsonify, request

from application.misc.query_wrapper import QueryWrapper

class StoreWrapper(QueryWrapper):
    def get(self):
        store_id = request.args.get('store_id')
        if store_id is None:
            abort(400, "store_id not provided or invalid")

        response = self._processor_get(
                store_id=store_id,
                user_id=g.user.id
            )
        return jsonify(response)

    def post(self):
        data = request.get_json()
        key = None
        value = None
        revision = None

        try:
            key = data['key']
            value = data['value']
        except:
            if key is None:
                abort(400, "key not provided or invalid")

            if value is None:
                abort(400, "value not provided or invalid")
        try:
            revision = data['revision']
        except:
            pass

        response = self._processor_post(
                key=key,
                value=value,
                revision=revision
            )
        return jsonify(response)
