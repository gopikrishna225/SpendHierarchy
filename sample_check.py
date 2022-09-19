import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        html.H1("Scrollbars", className="text-center"),
                        className="p-3 gradient",
                    ),
                    width=6,
                    style={"overflow": "scroll", "height": "400px"},
                ),
                dbc.Col(
                    html.Div(
                        html.H1("No scrollbars", className="text-center"),
                        className="p-3 gradient",
                    ),
                    width=6,
                    style={"overflow": "scroll", "height": "400px"},
                    className="no-scrollbars",
                ),
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)