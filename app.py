# %%
import dash
from dash import dcc, html, Input, Output, State
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go 
import dash_bootstrap_components as dbc

df = pd.read_csv('global_house_purchase_dataset.csv')

# %%
# List of numeric/categorical columns for factor analysis in Tab 2
FACTOR_ANALYSIS_COLS = sorted([
    'price', 'property_size_sqft', 'constructed_year', 'previous_owners',
    'rooms', 'bathrooms', 'has_storage_room', 'customer_salary',
    'loan_amount', 'loan_tenure_years', 'monthly_expenses', 'down_payment',
    'emi_to_income_ratio', 'satisfaction_score', 'neighbourhood_rating',
    'connectivity_score', 'crime_cases_reported', 'legal_cases_on_property'
])

# Column Descriptions
column_descriptions = dcc.Markdown("""
    ### Property Features
    - **price**: The final price of the property.
    - **property_size_sqft**: The total area of the property in square feet.
    - **constructed_year**: The year the property was originally built.
    - **previous_owners**: The number of previous owners.
    - **rooms**: The total number of rooms in the property.
    - **bathrooms**: The total number of bathrooms.
    - **has_storage_room**: Whether the property includes a storage room (1 for Yes, 0 for No).
    
    ---
    
    ### Buyer Financials
    - **customer_salary**: The annual salary of the buyer.
    - **loan_amount**: The total amount of the loan taken for the property.
    - **loan_tenure_years**: The duration of the loan in years.
    - **monthly_expenses**: The buyer's average monthly expenses.
    - **down_payment**: The initial payment made by the buyer.
    - **emi_to_income_ratio**: The ratio of the monthly loan payment to the buyer's monthly income. A lower value indicates less financial burden.
    
    ---
    
    ### Ratings & External Factors
    - **satisfaction_score**: A satisfaction rating (1-10) from previous owners.
    - **neighbourhood_rating**: A rating (1-10) for the quality of the neighbourhood.
    - **connectivity_score**: A score (1-10) for how well the property is connected to transport and amenities.
    - **crime_cases_reported**: Number of crime cases reported in the area in the last year.
    - **legal_cases_on_property**: Number of legal cases associated with the property.
    
    ---
    
    ### Outcome
    - **decision**: A outcome (1 for Purchase/Loan Approved, 0 for No).
""")


# Initialize the Dash App
app = dash.Dash(__name__)
server = app.server

# Define the App Layout
app.layout = html.Div(style={'display': 'flex', 'fontFamily': 'Arial, sans-serif'}, children=[
    # Sidebar
    html.Div(style={'width': '25%', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'height': '100vh', 'overflowY': 'auto'}, children=[
        html.H3("Global Property Filters", style={'textAlign': 'center'}),
        html.Hr(),
        html.P("Filter the data to discover insights.", style={'textAlign': 'center', 'fontSize': '14px'}),
        html.Br(),

        html.Label("Country"),
        dcc.Dropdown(id='country-dropdown', options=[{'label': c, 'value': c} for c in sorted(df['country'].unique())], placeholder="Select a Country..."),
        html.Br(),

        html.Label("City"),
        dcc.Dropdown(id='city-dropdown', placeholder="Select a Country first..."),
        html.Br(),

        html.Label("Property Type"),
        dcc.Dropdown(id='property-type-dropdown', placeholder="Select a City first..."),
        html.Br(),

        html.Label("Furnishing Status"),
        dcc.Dropdown(id='furnishing-status-dropdown', placeholder="Select a Property Type first..."),
        html.Br(),
        html.Hr(),
        
        html.Button("View Data Definition", id="btn-open-modal", style={'width': '100%', 'padding': '10px', 'marginBottom': '10px'}),
        html.Button("Download Filtered Data (CSV)", id="btn-download-csv", style={'width': '100%', 'padding': '10px', 'cursor': 'pointer'}),
        dcc.Download(id="download-dataframe-csv")
    ]),

    # Main Content Area
    html.Div(id='main-content', style={'width': '75%', 'padding': '20px', 'height': '100vh', 'overflowY': 'auto'}, children=[
        dcc.Tabs(id="tabs-container", children=[
            # Tab 1: Market Overview
            dcc.Tab(label='Market Overview', children=[
                html.Div(style={'padding': '20px'}, children=[
                    # KPI Section
                    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'textAlign': 'center', 'marginBottom': '20px'}, children=[
                        html.Div(id='kpi-properties', style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'width': '30%', 'backgroundColor': 'white'}),
                        html.Div(id='kpi-avg-price', style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'width': '30%', 'backgroundColor': 'white'}),
                        html.Div(id='kpi-avg-size', style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'width': '30%', 'backgroundColor': 'white'}),
                    ]),
                    html.Hr(),
                    html.H5("Key Metrics Distribution", style={'textAlign': 'center', 'marginBottom': '20px'}),
                    html.Div(style={'display': 'flex', 'flexWrap': 'wrap'}, children=[
                        dcc.Graph(id='violin-price', style={'width': '50%'}),
                        dcc.Graph(id='violin-size', style={'width': '50%'}),
                        dcc.Graph(id='hist-year', style={'width': '50%'}),
                        dcc.Graph(id='hist-rooms', style={'width': '50%'}),
                    ]),
                    html.Hr(),
                    html.H5("Price Comparison by Category", style={'textAlign': 'center', 'marginTop': '20px', 'marginBottom': '20px'}),
                    html.Div(style={'display': 'flex'}, children=[
                        dcc.Graph(id='box-property-type', style={'width': '50%'}),
                        dcc.Graph(id='box-furnishing-status', style={'width': '50%'}),
                    ])
                ])
            ]),

            # Tab 2: Purchase Factor Analysis
            dcc.Tab(label='Purchase Factor Analysis', children=[
                html.Div(style={'padding': '20px'}, children=[
                    html.H5("Purchase Decision Factor Analysis (Correlation Heatmap)", style={'textAlign': 'center'}),
                    html.P("Select up to 5 variables to analyze their correlation with the 'Purchase Decision'.", style={'textAlign': 'center', 'fontSize': '14px'}),
                    dcc.Dropdown(
                        id='factor-dropdown',
                        options=[{'label': col, 'value': col} for col in FACTOR_ANALYSIS_COLS],
                        multi=True,
                        placeholder="Select variables to analyze (up to 5)..."
                    ),
                    dcc.Graph(id='correlation-heatmap', style={'marginTop': '20px'})
                ])
            ]),

            # Tab 3: Buyer Financial Profile
            dcc.Tab(label='Buyer Financial Profile', children=[
                html.Div(style={'padding': '20px'}, children=[
                    html.H5("Customer Segment Analysis", style={'textAlign': 'center'}),
                    html.P("This scatter plot shows buyer segments based on their salary and loan amount. Hover over points for details.", style={'textAlign': 'center', 'fontSize': '14px', 'marginBottom': '20px'}),
                    dcc.Graph(id='customer-segment-scatter')
                ])
            ]),
        ]),
        
        # Modal for Data Descriptions
            dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Column Descriptions")),
                dbc.ModalBody(column_descriptions), 
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="btn-close-modal", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="desc-modal",
            is_open=False,
            size="lg",
            scrollable=True, 
        ),
    ])
])


# --- Helper Functions ---
def create_empty_figure(message="No data for selected filters."):
    """Creates a blank figure with a message."""
    return go.Figure().update_layout(
        annotations=[dict(text=message, showarrow=False, xref="paper", yref="paper", x=0.5, y=0.5)],
        xaxis=dict(visible=False), yaxis=dict(visible=False)
    )

# --- Dynamic Dropdown Callbacks ---
@app.callback(
    Output('city-dropdown', 'options'), Output('city-dropdown', 'value'),
    Input('country-dropdown', 'value'))
def update_city_options(selected_country):
    if not selected_country: return [], None
    cities = sorted(df[df['country'] == selected_country]['city'].unique())
    return [{'label': city, 'value': city} for city in cities], None

@app.callback(
    Output('property-type-dropdown', 'options'), Output('property-type-dropdown', 'value'),
    Input('city-dropdown', 'value'), State('country-dropdown', 'value'))
def update_property_type_options(selected_city, selected_country):
    if not selected_city: return [], None
    types = sorted(df[(df['country'] == selected_country) & (df['city'] == selected_city)]['property_type'].unique())
    return [{'label': prop_type, 'value': prop_type} for prop_type in types], None

@app.callback(
    Output('furnishing-status-dropdown', 'options'), Output('furnishing-status-dropdown', 'value'),
    Input('property-type-dropdown', 'value'), State('country-dropdown', 'value'), State('city-dropdown', 'value'))
def update_furnishing_status_options(selected_type, selected_country, selected_city):
    if not selected_type: return [], None
    statuses = sorted(df[(df['country'] == selected_country) & (df['city'] == selected_city) & (df['property_type'] == selected_type)]['furnishing_status'].unique())
    return [{'label': status, 'value': status} for status in statuses], None

# --- Modal Callback ---
@app.callback(
    Output("desc-modal", "is_open"),
    [Input("btn-open-modal", "n_clicks"), Input("btn-close-modal", "n_clicks")],
    [State("desc-modal", "is_open")],
    prevent_initial_call=True,
)
def toggle_modal(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open
    
# --- Tab 1 Callback: Market Overview ---
@app.callback(
    Output('kpi-properties', 'children'),
    Output('kpi-avg-price', 'children'),
    Output('kpi-avg-size', 'children'),
    Output('violin-price', 'figure'),
    Output('violin-size', 'figure'),
    Output('hist-year', 'figure'),
    Output('hist-rooms', 'figure'),
    Output('box-property-type', 'figure'),
    Output('box-furnishing-status', 'figure'),
    Input('country-dropdown', 'value'),
    Input('city-dropdown', 'value'),
    Input('property-type-dropdown', 'value'),
    Input('furnishing-status-dropdown', 'value')
)
def update_tab1_overview(country, city, prop_type, furnishing):
    dff = df.copy()
    if country: dff = dff[dff['country'] == country]
    if city: dff = dff[dff['city'] == city]
    if prop_type: dff = dff[dff['property_type'] == prop_type]
    if furnishing: dff = dff[dff['furnishing_status'] == furnishing]

    if dff.empty:
        empty_fig = create_empty_figure()
        kpi_no_data = [html.H4("0"), html.P("Properties")]
        kpi_no_price = [html.H4("$0"), html.P("Average Price")]
        kpi_no_size = [html.H4("0 sqft"), html.P("Average Size")]
        return kpi_no_data, kpi_no_price, kpi_no_size, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

    # KPI Calculations
    num_properties = len(dff)
    avg_price = dff['price'].mean()
    avg_size = dff['property_size_sqft'].mean()
    kpi_props_children = [html.H4(f"{num_properties:,}"), html.P("Properties")]
    kpi_price_children = [html.H4(f"${avg_price:,.0f}"), html.P("Average Price")]
    kpi_size_children = [html.H4(f"{avg_size:,.0f} sqft"), html.P("Average Size")]

    # Chart Creations
    violin_price = px.violin(dff, y='price', title='Price Distribution', box=True)
    violin_size = px.violin(dff, y='property_size_sqft', title='Property Size (sqft) Distribution', box=True)
    hist_year = px.histogram(dff, x='constructed_year', title='Construction Year Distribution')
    hist_rooms = px.histogram(dff, x='rooms', title='Room Count Distribution')
    box_prop_type = px.box(dff, x='property_type', y='price', title='Price by Property Type')
    box_furnishing = px.box(dff, x='furnishing_status', y='price', title='Price by Furnishing Status')
    
    for fig in [violin_price, violin_size, hist_year, hist_rooms, box_prop_type, box_furnishing]:
        fig.update_layout(margin=dict(l=40, r=20, t=50, b=30), title_x=0.5)

    return kpi_props_children, kpi_price_children, kpi_size_children, violin_price, violin_size, hist_year, hist_rooms, box_prop_type, box_furnishing

# --- Tab 2 Callback: Purchase Factor Analysis ---
@app.callback(
    Output('correlation-heatmap', 'figure'),
    Input('country-dropdown', 'value'),
    Input('city-dropdown', 'value'),
    Input('factor-dropdown', 'value')
)
def update_tab2_factors(country, city, selected_factors):
    dff = df.copy()
    if country: dff = dff[dff['country'] == country]
    if city: dff = dff[dff['city'] == city]
    
    if dff.empty:
        return create_empty_figure("No data for the selected filters.")
        
    if not selected_factors:
        return create_empty_figure("Please select variables to analyze.")
        
    # Limit to max 5 factors for readability
    selected_factors = selected_factors[:5]
    
    # Add 'decision' to the list for correlation calculation
    cols_to_correlate = selected_factors + ['decision']
    corr_matrix = dff[cols_to_correlate].corr()
    
    heatmap = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='RdBu_r',
        zmin=-1, zmax=1,
        title="Correlation Heatmap"
    )
    heatmap.update_layout(title_x=0.5)
    return heatmap

# --- Tab 3 Callback: Buyer Financial Profile ---
@app.callback(
    Output('customer-segment-scatter', 'figure'),
    Input('country-dropdown', 'value'),
    Input('city-dropdown', 'value'),
    Input('property-type-dropdown', 'value'),
    Input('furnishing-status-dropdown', 'value')
)
def update_tab3_segmentation(country, city, prop_type, furnishing):
    dff = df.copy()
    if country: dff = dff[dff['country'] == country]
    if city: dff = dff[dff['city'] == city]
    if prop_type: dff = dff[dff['property_type'] == prop_type]
    if furnishing: dff = dff[dff['furnishing_status'] == furnishing]
    
    # Analyze only customers who made a purchase
    dff = dff[dff['decision'] == 1]

    if dff.empty:
        return create_empty_figure("No purchase data for selected filters.")

    # Calculate average lines for quadrants
    avg_salary = dff['customer_salary'].mean()
    avg_loan = dff['loan_amount'].mean()

    fig = px.scatter(
        dff,
        x='customer_salary',
        y='loan_amount',
        color='property_type',
        title='Buyer Segments: Salary vs. Loan Amount',
        labels={'customer_salary': 'Customer Salary', 'loan_amount': 'Loan Amount'},
        hover_data=['city', 'price', 'property_size_sqft']
    )
    
    # Add quadrant lines
    fig.add_vline(x=avg_salary, line_width=1, line_dash="dash", line_color="grey")
    fig.add_hline(y=avg_loan, line_width=1, line_dash="dash", line_color="grey")
    
    fig.update_layout(
        title_x=0.5,
        margin=dict(l=40, r=20, t=50, b=30),
        xaxis_title="Customer Annual Salary",
        yaxis_title="Loan Amount"
    )

    return fig

# --- Download Callback ---
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    State('country-dropdown', 'value'),
    State('city-dropdown', 'value'),
    State('property-type-dropdown', 'value'),
    State('furnishing-status-dropdown', 'value'),
    prevent_initial_call=True,
)
def download_csv(n_clicks, country, city, prop_type, furnishing):
    dff = df.copy()
    if country: dff = dff[dff['country'] == country]
    if city: dff = dff[dff['city'] == city]
    if prop_type: dff = dff[dff['property_type'] == prop_type]
    if furnishing: dff = dff[dff['furnishing_status'] == furnishing]
    return dcc.send_data_frame(dff.to_csv, "filtered_properties.csv", index=False)


# Run the app
#if __name__ == '__main__':
#    app.run(debug=True)

# Run the server
server = app.server

# %%



