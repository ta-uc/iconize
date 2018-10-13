from flask_sslify import SSLify
import iconize

app = iconize.create_app()
sslify = SSLify(app)

if __name__=="__main__":
    app.run(debug=True)