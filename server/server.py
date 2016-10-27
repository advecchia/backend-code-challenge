import os
from markdown import markdown
from flask import request, Response
from flask_api import FlaskAPI
app = FlaskAPI(__name__)

PATH_ROOT = '/'
PATH_COLLECT = PATH_ROOT + 'collect/'
CURRENT_STATIC_PATH = os.path.dirname(os.path.abspath(__file__))
README_STATIC_PATH = CURRENT_STATIC_PATH + '/../README.md' 

@app.route(PATH_ROOT, methods=['GET'])
def app_root():
    try:
        with open(README_STATIC_PATH, 'r') as f:
            return Response(markdown(f.read()), mimetype='text/html')
    except:
        return Response('Hello World!', mimetype='text/html')

@app.route(PATH_COLLECT, methods=['POST'])
def collect_emissions():
    return {'content': request.data}

@app.route(PATH_COLLECT, methods=['GET'])
def show_emissions_summary():
    return {'summary': '[]'}
    #return Response('summary', mimetype='text/html')
if __name__ == '__main__':
    app.run(debug=True)
