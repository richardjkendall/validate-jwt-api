import logging
from flask_lambda import FlaskLambda
from flask import request, jsonify, make_response, g

import jwt
import json
from jwt.algorithms import RSAAlgorithm
from jwt.exceptions import ExpiredSignatureError

from error_handler import error_handler, BadRequestException, SystemFailureException, SignatureExpiredException

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s')
lambda_handler = FlaskLambda(__name__)
logger = logging.getLogger(__name__)

def success_json_response(payload):
  """Turns payload into a JSON HTTP200 response"""
  response = make_response(jsonify(payload), 200)
  response.headers["Content-type"] = "application/json"
  return response

def validate_jwt(token, key_set, aud):
  # first we have to get the headers
  headers = jwt.get_unverified_header(token)
  public_key = ""
  # then find the key
  for key in key_set:
    if key["kid"] == headers["kid"]:
      public_key = RSAAlgorithm.from_jwk(json.dumps(key))
  # then validate the token against the key
  if public_key:
    try:
      decoded = jwt.decode(
        token,
        public_key,
        algorithms=[headers["alg"]],
        audience=aud
      )
      return decoded
    except ExpiredSignatureError as e:
      raise SignatureExpiredException("Signature not valid")
  else:
    # could not find the key, probably an issue with keycloak
    raise SystemFailureException("Key could not be found in key set")

@lambda_handler.route("/", methods=["POST"])
@error_handler
def root():
  if not request.json:
    raise BadRequestException("Request should be JSON")
  if "keys" not in request.json:
    raise BadRequestException("Expecting 'keys' field, but not found")
  if "token" not in request.json:
    raise BadRequestException("Expecting 'token' field, but not found")
  if "aud" not in request.json:
    raise BadRequestException("Expecting 'aud', but not found")
  logger.info("Validating...")
  d = validate_jwt(
    token=request.json["token"],
    key_set=request.json["keys"],
    aud=request.json["aud"]
  )
  logger.info("Validated")
  return success_json_response(d)

if __name__ == '__main__':
  lambda_handler.run(debug=True, port=5001, host="0.0.0.0", threaded=True)