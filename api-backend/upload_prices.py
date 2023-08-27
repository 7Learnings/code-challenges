import sys
import json

import pandas as pd
import requests
from pydantic import BaseModel
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

# API = "https://api-backend-olsgyubl4a-ew.a.run.app"
API = "http://localhost:5000"


class Credentials(BaseModel):
    client_id: str
    client_secret: str


def authenticate_user(credentials):
    # try:
    #     auth = HTTPBasicAuth(credentials.client_id, credentials.client_secret)
    #     client = BackendApplicationClient(client_id=credentials.client_id)
    #     oauth = OAuth2Session(client=client)    
    #     token = oauth.fetch_token(token_url=f"{API}/oauth2/v2.0/token", auth=auth)
    #     access_token = token["access_token"]
        
    #     return access_token

    # except Exception as e:
    #     print(f"Authentication failed {e}")
    #     raise
    try:
        auth_resp = requests.post(f"{API}/oauth2/v2.0/token", 
              auth=HTTPBasicAuth(credentials.client_id, credentials.client_secret))
        print("User Authenticated Successfully!")
    except Exception as e:
        print(f"Authentication failed {e}")
        raise

    return auth_resp.json()["access_token"]



# TODO: implement authentication and upload
def upload_prices(access_token, data: pd.DataFrame):
    print("Uploading Prices...")
    try:
                
        i = 0
        chunk_size = 1_000

        while len(data[i:]):
            products_list = create_products_list(data[i:i+chunk_size])

            print(f"Uploading Chunk {i}...")
            imported = 0
            while imported < len(products_list):
                resp = requests.post(
                    f"{API}/product-prices",
                    data = json.dumps({"products":products_list[imported:]}),
                    headers={'accept': 'application/json',
                             'Authorization': f'Bearer {access_token}'}
                )
                imported += resp.json()['num_imported']
            resp.raise_for_status()
            i += chunk_size
        
        print("Prices are uploaded sucessfully!")    
    
    except Exception as e:
        print(f"Error Uploading prices {e}")
        raise



def create_products_list(df):
    products_list = []
    for _, row in df.iterrows():
        product_info = {
            "product_id": row["product_id"],
            "prices": [
                {
                    "market": row['market'],
                    "channel": row['channel'],
                    "price": row['price'],
                    "valid_from": row['valid_from'].replace(" ", "T"),
                    "valid_until": row['valid_until'].replace(" ", "T")
                }
            ]
        }
        products_list.append(product_info)
    
    return products_list


def validate_product_prices(access_token):
    print("\nValidating product prices...")
    try:
        resp = requests.get(
                    f"{API}/validate-product-prices",
                    headers={'accept': 'application/json',
                            'Authorization': f'Bearer {access_token}'}
                )
        if resp.json()["correct_checksum"]:
            print("Checksum validation successful!")
        else:
            print("Checksum validation failed!")
    except Exception as e:
        print(f"Error validating prices {e}")
        raise


def main(creds_file, csv_file):
    try:
        with open(creds_file) as f:
            creds = Credentials.model_validate_json(f.read())

        access_token = authenticate_user(creds)

        upload_prices(access_token, pd.read_csv(csv_file))
    
        validate_product_prices(access_token)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

    