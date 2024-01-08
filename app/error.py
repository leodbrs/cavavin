from flask import jsonify, render_template, request

from app import app


@app.errorhandler(400)
def bad_request(error):
    app.logger.error(f"Bad request: {error}")
    if request.path.startswith("/api/"):
        return jsonify(error=str(error.description)), 400
    else:
        return error, 400


@app.errorhandler(403)
def forbidden(error):
    app.logger.error(f"Bad request: {error}")
    if request.path.startswith("/api/"):
        return jsonify(error=str(error.description)), 403
    else:
        return error, 403


@app.errorhandler(404)
def not_found(error):
    app.logger.error(f"Bad request: {error}")
    if request.path.startswith("/api/"):
        return jsonify(error=str(error.description)), 404
    else:
        return render_template("404.html"), 404


@app.errorhandler(405)
def method_not_allowed(error):
    app.logger.error(f"Bad request: {error}")
    if request.path.startswith("/api/"):
        return jsonify(error=str(error.description)), 405
    else:
        return error, 405
