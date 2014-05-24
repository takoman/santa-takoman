from santa import create_app

if __name__ == '__main__':
    port = 5000
    host = '127.0.0.1'

    app = create_app()
    app.run(host=host, port=port)
