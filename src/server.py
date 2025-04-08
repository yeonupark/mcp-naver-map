import os
import time
import hmac
import hashlib
import base64
from typing import Optional
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

mcp = FastMCP("server")

load_dotenv()

GEO_API_ENDPOINT = "https://geolocation.apigw.ntruss.com/geolocation/v2"
MAP_API_ENDPOINT = "https://maps.apigw.ntruss.com/map-direction-15/v1/"

NAVER_ACCESS_KEY_ID = os.environ.get("NAVER_ACCESS_KEY_ID")
NAVER_SECRET_KEY = os.environ.get("NAVER_SECRET_KEY")

MAP_CLIENT_ID = os.environ.get("MAP_CLIENT_ID")
MAP_CLIENT_SECRET = os.environ.get("MAP_CLIENT_SECRET")

def make_signature(method, basestring, timestamp, access_key, secret_key):
    message = method + " " + basestring + "\n" + timestamp + "\n" + access_key
    message = message.encode('utf-8')         
    secret_key = secret_key.encode('utf-8')    

    signing_key = hmac.new(secret_key, message, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(signing_key).decode('utf-8') 

    return signature


def build_geo_api_headers(ip: Optional[str] = None):
    timestamp = str(int(time.time() * 1000))
    
    query = f"?ip={ip if ip else ''}&ext=t&responseFormatType=json" 
    basestring = "/geolocation/v2/geoLocation" + query  

    signature = make_signature(
        "GET",
        basestring, 
        timestamp,
        NAVER_ACCESS_KEY_ID,
        NAVER_SECRET_KEY,
    )

    headers = {
        "X-NCP-APIGW-TIMESTAMP": timestamp,
        "X-NCP-IAM-ACCESS-KEY": NAVER_ACCESS_KEY_ID,
        "X-NCP-APIGW-SIGNATURE-V2": signature,
    }
    return headers, query

@mcp.tool(
    name="get_current_location",
    description="Get current approximate location using Naver Geolocation API (IP 기반 위치 조회)",
)
async def get_current_location(ip: Optional[str] = None):
    """
    Get current approximate location using Naver Geolocation API.

    Args:
        ip (str, optional): IP address to lookup. If None, server detects automatically.
    """

    params = {
        "ip": ip if ip else "",
        "ext": "t",
    }

    async with httpx.AsyncClient() as client:
        headers, query = build_geo_api_headers(ip)
        response = await client.get(
            f"{GEO_API_ENDPOINT}/geoLocation{query}",
            headers=headers,
        )

        response.raise_for_status()

        data = response.json()
        latitude = data['geoLocation']['lat']
        longitude = data['geoLocation']['long']

        return {
            "latitude": latitude,
            "longitude": longitude
        }

@mcp.tool(
    name="get_directions",
    description="Get driving directions between two points using Naver Maps Directions15 API",
)
async def get_directions(
    start_lat: float,
    start_lng: float,
    goal_lat: float,
    goal_lng: float,
    option: str = "traoptimal",
):
    """
    Get driving directions between two points using Naver Maps Directions15 API.

    Args:
        start_lat (float): Starting point latitude.
        start_lng (float): Starting point longitude.
        goal_lat (float): Goal point latitude.
        goal_lng (float): Goal point longitude.
        option (str, optional): Route search option. Defaults to "traoptimal".
    """

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{MAP_API_ENDPOINT}driving",
            params={
                "start": f"{start_lng},{start_lat}",
                "goal": f"{goal_lng},{goal_lat}",
                "option": option,
            },
            headers={
                "X-NCP-APIGW-API-KEY-ID": MAP_CLIENT_ID,
                "X-NCP-APIGW-API-KEY": MAP_CLIENT_SECRET,
            },
        )

        response.raise_for_status() 

        return response.text

if __name__ == "__main__":
    mcp.run()