from secrets import token_hex

from application import app, db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alveo_id = db.Column(db.String(48), nullable=False, unique=True)
    api_key = db.Column(db.String(64), nullable=False, unique=True)

    def __init__(self, alveo_id):
        self.alveo_id = alveo_id 
        self.generate_token()

    def __repr__(self):
        return str(self.alveo_id)

    def __str__(self):
        return str(self.alveo_id)

    def generate_token(self):
        self.api_key = token_hex(app.config['TOKEN_LENGTH'])
        return self.api_key