from blog import create_app

app = create_app()

def getApp():
      return app

if __name__ == '__main__':
      app.run(debug=False)