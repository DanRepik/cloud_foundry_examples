# test_fixtures.py

import os
import pytest
import subprocess
import json
from cloud_foundry import is_localstack_deployment, logger

log = logger(__name__)

api_url: str = None
oauth_url: str = None


@pytest.fixture
def gateway_endpoint():
    global api_url
    if not api_url:
        outputs = get_pulumi_stack_outputs("organization/foundry-examples/dev")
        log.info(f"outputs: {outputs}")
        
        # Retrieve the rest-api-id and rest-api-host using .apply() to extract their values
        api_id = outputs.get("test-api-id", None)
        host = outputs.get("test-api-host", None)
        log.info(f"host: {host}")
        api_url = f"https://{api_id}.{host}"
    return api_url

@pytest.fixture(scope="module")
def oauth_endpoint():
    global oauth_url
    if not oauth_url:
        # Use Pulumi's StackReference to reference the 'simple-oauth-server/dev' stack
        outputs = get_pulumi_stack_outputs("organization/simple-oauth-server/dev")
        log.info(f"outputs: {outputs}")
        
        # Retrieve the rest-api-id and rest-api-host using .apply() to extract their values
        api_id = outputs.get("rest-api-id", None)
        host = outputs.get("rest-api-host", None)
        # Return the OAuth endpoint URL as a string (use .apply() to create the final URL)
        oauth_url = f"https://{api_id}.{host}"
    return oauth_url

def get_pulumi_stack_outputs(stack_name: str):
    # Run the Pulumi CLI command to get stack outputs in JSON format
    try:
        result = subprocess.run(
            ['pulumi', 'stack', 'output', '--stack', stack_name, '--json'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        
        # Parse the JSON output
        outputs = json.loads(result.stdout)
        return outputs
    
    except subprocess.CalledProcessError as e:
        print(f"Error executing Pulumi command: {e.stderr.decode().strip()}")
        return None

