from website import create_app
import os

SESSION_TYPE = 'filesystem'

app = create_app()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"./website/keys/networknotetaker-dddcaba2ca84.json"

if __name__ == '__main__':
    app.run(debug=True)