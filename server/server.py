import json

from fastapi import FastAPI, Request, Response, APIRouter
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.responses import RedirectResponse


""" CONFIG """

routes = APIRouter()
limiter = Limiter(key_func=get_remote_address)
routes.state.limiter = limiter

async def rate_limit_exceeded_handler(request: Request, exc: Exception) -> Response:
  if isinstance(exc, RateLimitExceeded):
      return _rate_limit_exceeded_handler(request, exc)  
  else:
      raise exc

routes.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


""" URL HashMap """

class UrlHashmap: 
  with open("urls/url_map_app.json", "r") as json_file:
      env_vars = json.load(json_file)
  url_map = dict(env_vars)
  json_file.close()

url_hashmap = UrlHashmap()
 
""" ROUTES """

@routes.get("/")
@limiter.limit("1/second")
async def root(request: Request):
  return {"message": "Hello World"}


@routes.get("/iam-alive")
@limiter.limit("1/second")
async def ping_pong(request: Request):
  return {"I am alive": True}
  

""" Data Collection """

@routes.get("/update-water-status")
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