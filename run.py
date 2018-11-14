import os
from app import create_app

config_name = os.environ.get('environ')
app = create_app(config_name) #development

if __name__ == '__main__':
    app.run()
