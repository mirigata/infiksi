from flask import Flask, request, jsonify

import infiksi


app = Flask(__name__)


@app.route("/")
def get_metadata():
    url = request.args.get('q', None)

    try:
        metadata = infiksi.get_metadata(url)
        return jsonify(metadata.__dict__)
    except infiksi.UnreachableError as e:
        return jsonify(error=str(e)), 404
    except infiksi.TemporaryError as e:
        return jsonify(error=str(e)), 502
    except infiksi.TimeoutError as e:
        return jsonify(error=str(e)), 504


@app.route("/status/ping")
def ping():
    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
