import threading

import uvicorn

from server.server import routes
from server.diagnostics_server import diagnostics_app


def run_app():
    uvicorn.run(routes, host="0.0.0.0", port=8000, log_level="info")

def run_diagnostics_app():
    uvicorn.run(diagnostics_app, host="0.0.0.0", port=8001, log_level="info")

if __name__ == '__main__':

    app_thread = threading.Thread(target=run_app)
    diagnostics_thread = threading.Thread(target=run_diagnostics_app)

    app_thread.start()
    diagnostics_thread.start()
    




  







