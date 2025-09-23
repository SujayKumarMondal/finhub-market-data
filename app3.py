import dash
from dash import html, dcc, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import requests
import json
import pyperclip

# ----------------- Initialize app -----------------
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
app.title = "Financial Microservice Explorer"
server = app.server  # for deployment

# ----------------- Fetch OpenAPI dynamically -----------------
API_BASE = "http://127.0.0.1:8012"
OPENAPI_URL = f"{API_BASE}/openapi.json"

try:
    openapi_data = requests.get(OPENAPI_URL).json()
except Exception as e:
    openapi_data = {"paths": {}}
    print("Error fetching OpenAPI:", e)

# Prepare endpoints dict dynamically
endpoints = {}
for path, methods in openapi_data.get("paths", {}).items():
    for method, info in methods.items():
        tag = info.get("tags", ["Other"])[0]
        key = f"{tag} {method.upper()} {path}"
        parameters = info.get("parameters", [])
        endpoints[key] = {
            "url": path,
            "method": method.upper(),
            "params": parameters
        }

GOOGLE_FORM_URL = "https://docs.google.com/forms/d/1SG_zFgd_L8Fae65cOAjFdlbjEr5FED5YeOPx0N5jXhU/edit?usp=forms_home&ouid=109228766598378673168&ths=true"

# ----------------- Layout -----------------
app.layout = dbc.Container([
    # Header with title & feedback
    dbc.Row(
        dbc.Col(
            dbc.Row(
                [
                    dbc.Col(html.H2("📊 Financial Microservice Explorer"), width="auto"),
                    dbc.Col(html.A("Feedback", href=GOOGLE_FORM_URL, target="_blank",
                                   className="btn btn-primary"), width="auto", className="ms-auto")
                ],
                align="center",
                className="w-100"
            )
        ),
        className="my-3"
    ),

    # Dropdown + Try button
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id="endpoint-dropdown",
            options=[{"label": k, "value": k} for k in endpoints.keys()],
            placeholder="Select an endpoint...",
            clearable=True
        ), width=8),
        dbc.Col(dbc.Button("Try it out", id="try-btn", color="success"), width=4)
    ], className="mb-4"),

    # Swagger-like and Response screens
    html.Div(id="swagger-screen"),
    html.Div(id="response-screen", style={"marginTop": "20px"}),

    # Toast for copy notification
    dbc.Toast(
        "Copied!",
        id="copy-toast",
        header="",
        is_open=False,
        duration=2000,
        icon="success",
        style={"position": "fixed", "top": 20, "right": 20, "width": 150}
    )
])

# ----------------- Callbacks -----------------

# Show Swagger-like screen dynamically
@app.callback(
    Output("swagger-screen", "children"),
    Output("swagger-screen", "style"),
    Input("try-btn", "n_clicks"),
    Input({"type": "cancel-btn", "index": ALL}, "n_clicks"),
    State("endpoint-dropdown", "value"),
    prevent_initial_call=True
)
def update_swagger(try_clicks, cancel_clicks, selected_key):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if "cancel-btn" in triggered_id:
        return "", {"display": "none"}

    if "try-btn" in triggered_id:
        if not selected_key:
            return dbc.Alert("⚠️ Please select an endpoint.", color="warning"), {"display": "block"}

        ep = endpoints[selected_key]
        fields = []
        for p in ep["params"]:
            pname = p.get("name")
            ptype = p.get("schema", {}).get("type", "string")
            default = p.get("example") or p.get("schema", {}).get("default") or ""
            fields.append(dbc.Label(f"{pname} ({ptype})"))
            fields.append(dbc.Input(id={"type": "param-input", "index": pname}, value=default, placeholder=str(default)))

        card = dbc.Card([
            dbc.CardHeader(f"Swagger Screen - {selected_key}"),
            dbc.CardBody(fields),
            dbc.CardFooter([
                dbc.Button("Execute", id={"type": "exec-btn", "index": "1"}, color="primary", className="me-2"),
                dbc.Button("Cancel", id={"type": "cancel-btn", "index": "1"}, color="secondary")
            ])
        ], className="mt-3")

        return card, {"display": "block"}

    return dash.no_update, dash.no_update

# Execute API & show response
@app.callback(
    Output("response-screen", "children"),
    Output("response-screen", "style"),
    Input({"type": "exec-btn", "index": ALL}, "n_clicks"),
    Input({"type": "close-btn", "index": ALL}, "n_clicks"),
    State("endpoint-dropdown", "value"),
    State({"type": "param-input", "index": ALL}, "value"),
    State({"type": "param-input", "index": ALL}, "id"),
    prevent_initial_call=True
)
def handle_response(exec_clicks, close_clicks, selected_key, param_values, param_ids):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Close response screen
    if "close-btn" in triggered_id:
        return "", {"display": "none"}

    # Execute API
    if "exec-btn" in triggered_id:
        ep = endpoints[selected_key]
        params = {}
        for val, pid in zip(param_values, param_ids):
            params[pid["index"]] = val

        try:
            if ep["method"] == "GET":
                r = requests.get(f"{API_BASE}{ep['url']}", params=params)
                data = r.json()
            else:
                r = requests.request(ep["method"], f"{API_BASE}{ep['url']}", json=params)
                data = r.json()
        except Exception as e:
            data = {"error": str(e)}

        card = dbc.Card([
            dbc.CardHeader([
                html.Span("Response"),
                dbc.Button("Copy", id={"type": "copy-btn", "index": "1"}, color="info", size="sm",
                           style={"float": "right", "marginLeft": "5px"}),
                dbc.Toast(
                    "Copied!",
                    id="copy-toast",
                    is_open=False,
                    duration=2000,
                    style={
                        "position": "absolute",
                        "top": "0px",
                        "right": "-120px",
                        "zIndex": 9999,
                        "width": "100px",
                        "padding": "2px",
                        "textAlign": "center"
                    }
                ),
                dbc.Button("Close", id={"type": "close-btn", "index": "1"}, color="danger", size="sm",
                           style={"float": "right"})
            ]),
            dbc.CardBody([
                html.Pre(json.dumps(data, indent=2), id="response-text", style={"whiteSpace": "pre-wrap"})
            ])
        ], className="mt-3")
        return card, {"display": "block"}

    return dash.no_update, dash.no_update

# Copy response to clipboard
@app.callback(
    Output("copy-toast", "is_open"),
    Input({"type": "copy-btn", "index": ALL}, "n_clicks"),
    State("response-text", "children"),
    prevent_initial_call=True
)
def copy_response(n_clicks, text):
    n_clicks = [0 if x is None else x for x in n_clicks]
    if sum(n_clicks) > 0 and text:
        pyperclip.copy(text)
        return True
    return False

# ----------------- Run -----------------
if __name__ == "__main__":
    app.run(debug=True, port=8050)
