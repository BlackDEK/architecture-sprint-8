import io
import keycloak
import os
import flask_cors
import flask

app = flask.Flask(__name__)
flask_cors.CORS(app, origins=[os.getenv('FRONT_URL', 'http://localhost:3000'), 'http://localhost:3000'],
                allow_methods=['GET'],
                allow_headers=['DNT', 'User-Agent', 'X-Requested-With', 'If-Modified-Since',
                               'Cache-Control', 'Content-Type', 'Range', 'Authorization'],
                )

keycloak_openid = keycloak.KeycloakOpenID(
    server_url=os.getenv("KEYCLOAK_URL", "http://localhost:8080"),
    realm_name=os.getenv("KEYCLOAK_REALM", "reports-realm"),
    client_id=os.getenv("CLIENT_ID", "reports-api"),
    client_secret_key=os.getenv(
        "CLIENT_SECRET", "oNwoLQdvJAvRcL89SydqCWCe5ry1jMgq"
    ),
    verify=True,
)


@app.route('/reports', methods=['GET'])
def reports():
    token = flask.request.headers.get("authorization").removeprefix("Bearer ")
    client_data = keycloak_openid.decode_token(token, validate=True)

    if 'prothetic_user' in client_data['realm_access']['roles']:
        user_name = client_data['preferred_username']
        content = f'Reports for user {user_name}'
        data = io.BytesIO(content.encode(encoding="utf-8"))
        return flask.send_file(data, mimetype="text/txt",
                               as_attachment=True, download_name='report.txt')

    return flask.abort(401)


if __name__ == "__main__":
    app.run(port=8000)
