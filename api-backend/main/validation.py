from werkzeug.exceptions import HTTPException
from flask import make_response
from flask import jsonify

class NotFoundError(HTTPException):
    def __init__(self,error_message,error_code,status_code):
        message = {"error_code": error_code,"error_message": error_message}
        self.response = make_response(jsonify(message),status_code)

class BusinessValidationError(HTTPException):
    def __init__(self,error_message,error_code,status_code):
        message = {"error_code": error_code, "error_message": error_message}
        self.response = make_response(jsonify(message),status_code)

