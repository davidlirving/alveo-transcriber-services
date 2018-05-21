from flask import g

from application import app, events

MODULE_PATHS = {
    'AUTH': 'auth',
    'SEGMENTATION': 'segmenter',
    'DATASTORE': {
        'EXPORT': {
            'SELF': 'datastore:export',
            'USER': 'datastore:export_by_user',
            'KEY': 'datastore:export_by_key',
            'USER+KEY': 'datastore:export_by_user_key',
        },
        'LIST': {
            'SELF': 'datastore:list',
            'USER': 'datastore:list_by_user',
            'KEY': 'datastore:list_by_key',
            'USER+KEY': 'datastore:list_by_user_key',
        },
        'GET': 'datastore:get',
        'POST': 'datastore:post'
    }
}

class handle_api_event(object):
    def __init__(self, module_id, event_name):
        self.register(module_id, event_name);

    def register(self, module_id, event_name):
        if not module_id in events:
            events.update({module_id: {}})

        events[module_id][event_name] = self

    def __call__(self, function):
        self.handle = function

def get_domain_handler(domain):
    for handler in app.config['DOMAIN_HANDLERS']:
        try:
            if domain in handler['domains']:
                return handler['module']
        except:
            pass

def get_module_metadata(module):
    try:
        return next((handler for handler in app.config['DOMAIN_HANDLERS'] if handler["module"] == module), None)
    except:
        return None

def get_handler_for(domain, event):
    module = get_domain_handler(domain)
    if module is None:
        return None

    handler_ref = None
    try:
        handler_ref = events[module][event]
    except:
        pass

    return handler_ref
