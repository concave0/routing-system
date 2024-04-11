import os
import datetime 
import json 

import requests 
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.blocking import BlockingScheduler
from fastapi import FastAPI, Request, Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send


""" CONFIG """
app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

async def rate_limit_exceeded_handler(request: Request, exc: Exception) -> Response:
  if isinstance(exc, RateLimitExceeded):
      return _rate_limit_exceeded_handler(request, exc)  # Corrected line
  else:
      raise exc


# Use the wrapper function as the exception handler for RateLimitExceeded
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


""" URL HashMap """
class UrlHashmap: 
  # Read the JSON file
  with open("urls/url_map_app.json", "r") as json_file:
      env_vars = json.load(json_file)
  url_map = dict(env_vars)
  json_file.close()

url_hashmap = UrlHashmap()
 
""" ROUTES """
@app.get("/")
@limiter.limit("1/second")
async def root(request: Request):
  return {"message": "Hello World"}


@app.get("/iam-alive")
@limiter.limit("1/second")
async def ping_pong(request: Request):
  return {"I am alive": True}
  

""" Data Collection """
@app.get("/update-water-status")
@limiter.limit("1/second")
async def unstructed_data_collection(request: Request):
  unstructed_data_collection_url = url_hashmap.url_map.get("Water_Level_Data_Collection")

  if unstructed_data_collection_url is None:
      raise ValueError("Water Level Data Collection URL is not defined in URL map.")

  # Get 'moisture_level' from request headers or default to an empty string if not found
  moisture_level = request.headers.get('moisture_level', '')
  headers_to_forward = {'moisture_level': moisture_level}
  redirect = RedirectResponse(url=unstructed_data_collection_url, headers=headers_to_forward)
  return redirect
  

""" Ngrok Routes """
# TODO add ngrok routes here that calls your systems and make that you put the URL's in the secerts file.