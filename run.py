from app import app
from app.Utils.update import update_model
from app.classifier import clf

if __name__ == '__main__':
    clf = update_model(model=clf, batch_size=10000)
    app.run(host='127.0.0.1', port=8080)
