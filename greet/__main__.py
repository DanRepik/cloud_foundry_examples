# __main__.py

import cloud_foundry

greet_function = cloud_foundry.python_function(
    "test-function", handler="app.handler", sources={"app.py": "./app.py"}
)

greet_api = cloud_foundry.rest_api(
    "greet-api",
    body="./api_spec.yaml",
    integrations=[{"path": "/greet", "method": "get", "function": greet_function}],
)
