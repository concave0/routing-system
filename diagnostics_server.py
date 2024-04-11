import datetime 
import json 

import requests 
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.blocking import BlockingScheduler
from fastapi import FastAPI, Request, Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


""" CONFIG """
diagnostics_app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
diagnostics_app.state.limiter = limiter

async def rate_limit_exceeded_handler(request: Request, exc: Exception) -> Response:
  if isinstance(exc, RateLimitExceeded):
      return _rate_limit_exceeded_handler(request, exc)  # Corrected line
  else:
      raise exc


# Use the wrapper function as the exception handler for RateLimitExceeded
diagnostics_app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


""" URL HashMap """
class UrlHashmap: 
  # Read the JSON file
  with open("urls/url_map_diagnostics.json", "r") as json_file:
      env_vars = json.load(json_file)
  url_map = dict(env_vars)
  json_file.close()


""" Diagnostics """
class DiagnosticsData: 

  # Data Proccesser Diagnostic
  diagnostics_data_proccessor = {}
  history_data_proccessor = {} 

  # Water Level Data Collection Diagnostic
  diagnostics_water_level_data_collection = {}
  history_water_level_data_collection = {}

  # Discord Bot Iam Alive Diagnostic
  diagnostics_discord_bot_iam_alive = {}
  history_discord_bot_iam_alive = {}


""" Objects """
url_hashmap = UrlHashmap()
scheduler = BlockingScheduler()
diagnostics = DiagnosticsData()

""" Jobs """
def collect_data_uptime():

  now = datetime.datetime.now()

  # Data Proccesser Diagnostic
  data_proccessor_url = url_hashmap.url_map.get("Ping_Data_Proccesser")
  if not data_proccessor_url:
    raise ValueError("Data Processor URL is missing or invalid.")
  data_proccessor_response = requests.get(data_proccessor_url) 

  history_data_proccessor_url = {
    "json": data_proccessor_response.json, 
    "status_code": data_proccessor_response.status_code, 
    "url": data_proccessor_response.url,
    "headers": data_proccessor_response.headers,
    "encoding": data_proccessor_response.encoding,
  }

  diagnostics.diagnostics_data_proccessor["Data_Proccessor_Status"] = data_proccessor_response.status_code
  diagnostics.history_data_proccessor[f"Data_Proccessor_History {now}"] = history_data_proccessor_url

  # Water Level Data Collection Diagnostic
  data_water_lvl_data = url_hashmap.url_map.get("Water_Level_Data_Collection")
  if not data_water_lvl_data:
    raise ValueError("Water Level Data Collection URL is missing or invalid.")
  response_data_water_lvl_data = requests.get(data_water_lvl_data) 

  history_data_water_lvl_data = {
    "json": response_data_water_lvl_data.json, 
    "status_code": response_data_water_lvl_data.status_code, 
    "url": response_data_water_lvl_data.url,
    "headers": response_data_water_lvl_data.headers,
    "encoding": response_data_water_lvl_data.encoding,
  }

  diagnostics.diagnostics_water_level_data_collection["Water_Level_Status"] = response_data_water_lvl_data.status_code
  diagnostics.history_water_level_data_collection[f"History_Water_Level_Status {now}"] = history_data_water_lvl_data

  # Discord Bot Iam Alive Diagnostic
  discord_bot_url_alive = url_hashmap.url_map.get("Discord_Bot_Url_Iam_Alive")
  if not discord_bot_url_alive:
    raise ValueError("Discord Bot URL is missing or invalid.") 
  response_discord_bot_response_alive = requests.get(discord_bot_url_alive)

  history_discord_bot_response_alive = {
    "json": response_discord_bot_response_alive.json, 
    "status_code": response_discord_bot_response_alive.status_code, 
    "url": response_discord_bot_response_alive.url,
    "headers": response_discord_bot_response_alive.headers,
    "encoding": response_discord_bot_response_alive.encoding,
  }

  diagnostics.diagnostics_discord_bot_iam_alive["Discord_Bot_Iam_Alive_Status"] = response_discord_bot_response_alive.status_code
  diagnostics.history_discord_bot_iam_alive[f"History_Discord_Bot_Iam_Alive {now}"] = history_discord_bot_response_alive



""" Scheduling Route Start """
# @diagnostics_app.get("start-scheduling-diagnostics")
# async def start_scheduling_diagnostics():
#   trigger = IntervalTrigger(hours=1)
#   scheduler.add_job(collect_data_uptime, trigger) 
#   scheduler.start()

