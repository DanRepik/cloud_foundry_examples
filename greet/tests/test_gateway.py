# test_gateway.py

import logging
import requests
import time

from cloud_foundry import logger
from test_fixtures import gateway_endpoint

log = logger(__name__)

def test_get_request(gateway_endpoint):
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
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}"

    # Validate the response content
    result = response.json()
    print(f"result: {result['message']}")
    assert result['message'] == "Unauthorized"

