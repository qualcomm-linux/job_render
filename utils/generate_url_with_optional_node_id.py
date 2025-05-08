from urllib.parse import urlunparse, urlparse

base_url = "https://kernelci-api.westus3.cloudapp.azure.com/latest/"
params = {
    "kind": "kbuild",
    "result": "pass",
    "name": "kbuild-gcc-12-arm64",
    "data.kernel_revision.tree": "mainline",
    "limit": 1 # defualt value is 250 in the requested server
}

# Function to build URL with optional id
def build_url(base_url=base_url, params=params, id_value=None, tree=None, offset=None):
    if offset is not None:
        params["offset"] = offset
    if tree is not None:
        params["data.kernel_revision.tree"] = tree
    url_parts = list(urlparse(base_url))
    if id_value:
        # If id is provided, construct the URL with node_id
        url_parts[2] = f"/latest/node/{id_value}"
        url_parts[4] = ''  # Clear query parameters
    else:
        # Otherwise, use the original params and construct the URL for nodes
        url_parts[2] = "/latest/nodes"
        query = "&".join([f"{key}={value}" for key, value in params.items()])
        url_parts[4] = query
    return urlunparse(url_parts)

