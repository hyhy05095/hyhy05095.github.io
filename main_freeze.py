from main import app
from flask_frozen import Freezer

freezer = Freezer(app)

@freezer.register_generator
def search():
    yield {'keyword': 'python'}

if __name__ == '__main__':
    freezer.freeze()