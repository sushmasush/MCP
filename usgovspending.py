from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import json
import logging
import time
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("USA Spending")

# Constants
NWS_API_BASE = "https://api.usaspending.gov"
OUTPUT_DIRECTORY="./output/"


def getRunLogFile(pyFname):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    logger.info("timestamp "+timestr)
    fileTSName="run-"+timestr+pyFname+".log"
    filepath=OUTPUT_DIRECTORY+fileTSName
    logger.info(filepath)
    return filepath


async def make_all_awards_request(url: str) -> dict[str, Any] | None:
    """Make a request to the USA Spending API with proper error handling."""
    headers = {
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            logger.info(response)
            return response.json()
        except Exception:
            return None


@mcp.tool()
async def get_top_awards_data() -> str:
    """Get US Spending data.
    """
    url = f"{NWS_API_BASE}/api/v2/agency/awards/count/"
    print(url)
    data = await make_all_awards_request(url)
    print(data)
    result = ""
    if not data :
        return "Unable to fetch adata"
    return data

@mcp.tool()
async def get_top_agency_details(code: str) -> str:
    """Get US Spending data for the current Fiscal year.
    Args:
        code: Code of the toptier awarding agency
    """

    url = f"{NWS_API_BASE}/api/v2/agency/{code}/budget_function/"
    print(url)
    data = await make_all_awards_request(url)
    print(data)
    result = ""
    
    if not data :
        return "Unable to fetch adata"

    return data

@mcp.tool()
async def get_state_budget_details(fipscode:str)-> str:
    """Get US Spending data for state based on FIPS code.
    Args:
        FIPS Code: The FIPS code is based on the state
    """
    url = f"{NWS_API_BASE}/api/v2/recipient/state/{fipscode}/"
    logger.info(url)
    data = await make_all_awards_request(url)   
    if not data:
        return "unable to fetch data"
    else: 
        return data
    return data   

@mcp.tool()
async def get_spending_all_state()->str:
    """Get US Spending data for state based on FIPS code.
    """
    url = f"{NWS_API_BASE}/api/v2/recipient/state/"
    print(url)
    data = await make_all_awards_request(url)
    print(data)
    result = "Invalid argument"
    
    if not data :
        return "Unable to fetch adata"
    return data

@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"
