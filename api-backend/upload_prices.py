import sys

import pandas as pd
import requests
from pydantic import BaseModel
from requests.auth import HTTPBasicAuth

API = "https://api-backend-olsgyubl4a-ew.a.run.app"
# API = "http://localhost:8000"


class Credentials(BaseModel):
    client_id: str
    client_secret: str


# TODO: implement authentication and upload
def upload_prices(credentials: Credentials, data: pd.DataFrame):
    resp = requests.post(
        f"{API}/import/prices/",
        data.to_json(),
        auth=HTTPBasicAuth(credentials.client_id, credentials.client_secret),
    )
    resp.raise_for_status()


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        creds = Credentials.model_validate_json(f.read())
    upload_prices(creds, pd.read_csv(sys.argv[2]))
