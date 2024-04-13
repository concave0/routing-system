## Purpose 

Routing-system routes all traffic coming from Ngrok (traffic from Raspberry Pi's), discord, and data processing. It is the central hub for all communication within the IoT irrigation systems controller.  


## Main Application (main.py)
### Overview
The main application sets up and runs a FastAPI application with OpenTelemetry instrumentation for tracing HTTP requests and exporting the traces to a custom JSON file. It also runs a diagnostics app alongside the main app, each on different ports using threading.

### Key Components

JsonSpanExporter: A custom SpanExporter that exports span information to a JSON file. This is used for tracing and diagnostics purposes.

Setup OpenTelemetry (setup_opentelemetry): Configures OpenTelemetry with a custom JSON span exporter and instruments both FastAPI and the requests library for automatic span generation.

Running the Apps (run_app, run_diagnostics_app): Functions to run the primary FastAPI app and the diagnostics FastAPI app using Uvicorn.

### Usage
To start the application and diagnostics server, simply execute:

python3 main.py

This will start both servers on ports 8000 (main app) and 8001 (diagnostics app), respectively.

## Application Server ( app.py )

### Overview
Defines the main application server using FastAPI, incorporating rate limiting and structured around a simple web application framework with routes for health checks and basic operations.

### Key Components
Rate Limiting: Utilizes slowapi to limit the request rate to various endpoints.

URL HashMap (UrlHashmap): A utility to manage URL mappings loaded from a JSON file, enabling dynamic endpoint configurations.

Routes: Defines various endpoints, including a root message, an "I am alive" message, and a water status update handling route that forwards requests to another service based on URL mappings.

### Usage
The app is automatically started when main.py is executed and is accessible on the assigned port (default 8000).

## Diagnostics Server ( diagnostics_server.py )

### Overview

A separate FastAPI application aimed at running diagnostics, including uptime checks for various components of the system. It includes rate limiting and is structured to periodically check the health of specified URLs.

### Key Components

DiagnosticsData: Maintains diagnostic information and history for various components like data processors, water level data collection, and a Discord bot status check.

Collecting Uptime Data (collect_data_uptime): A function to perform health checks on configured URLs and record their status and response metadata.

### Usage
While the diagnostics server's setup is included, starting the scheduling for diagnostics collection is commented out. It can be enabled and customized as needed for periodic diagnostic checks.

