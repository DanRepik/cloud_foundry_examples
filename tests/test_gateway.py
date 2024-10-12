# test_gateway.py

import logging
import requests
import time

from cloud_foundry import logger
from test_fixtures import gateway_endpoint, oauth_endpoint

log = logger(__name__)

def test_get_request_unauthorized(gateway_endpoint):
    # Define the endpoint
    endpoint = gateway_endpoint + "/greet?name=World"
    log.info(f"request: {endpoint}")

    # Send the GET request
    start = time.perf_counter()
    response = requests.get(endpoint)
    log.info(f"response time: {time.perf_counter()-start}")
    log.info(f"response text: {response.text}")

    # Validate the response status code
    assert (
        response.status_code == 401
    ), f"Expected status code 401, got {response.status_code}"

    # Validate the response content
    result = response.json()
    print(f"result: {result['message']}")
    assert result['message'] == "Unauthorized"

def test_oauth_endpoint(oauth_endpoint):
    assert oauth_endpoint.startswith("https://")
    assert "execute-api" in oauth_endpoint

def test_get_request_authorized(gateway_endpoint, oauth_endpoint):
    # Define the endpoint
    start = time.perf_counter()
    body = {
        "client_id": "client1",
        "client_secret": "client1-secret",
        "audience": "test-api",
        "grant_type": "client_credentials"
    }
    response = requests.post(f"{oauth_endpoint}/token", json=body)
    log.info(f"response time: {time.perf_counter()-start}")
    log.info(f"response status: {response.status_code}")
    log.info(f"response text: {response.text}")

    result = response.json()
    log.info(f"token: {result["token"]}")
    log.info(f"gateway: {gateway_endpoint}")

    # Send the GET request
    start = time.perf_counter()
    headers = {"Authorization": f"Bearer {result['token']}"}
    log.info(f"headers: {headers}")
    response = requests.get(f"{gateway_endpoint}/greet?name=World", headers=headers)
    log.info(f"response time: {time.perf_counter()-start}")
    log.info(f"response text: {response.text}")

    assert False
