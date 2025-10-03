# %%
import dash
from dash import dcc, html, Input, Output
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go 


df = pd.read_csv('global_house_purchase_dataset.csv')
print(df.head())
#print(df['price'].min())
#print(df['price'].max())


# 2. Initialize the Dash App 
app = dash.Dash(__name__)

# 3. Define the App Layout
app.layout = html.Div(style={'display': 'flex', 'fontFamily': 'Arial, sans-serif'}, children=[
    
    # --- Sidebar ---
    html.Div(style={'width': '25%', 'padding': '20px', 'backgroundColor': '#f8f9fa'}, children=[
        html.H3("Property Filters", style={'textAlign': 'center'}),
        html.Hr(),
        html.P("Filter the data to find the information you need.", style={'textAlign': 'center', 'fontSize': '14px'}),
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

        html.Label("Price Range"),
        dcc.RangeSlider(id='price-slider', min=df['price'].min(), max=df['price'].max(), step=50000, value=[df['price'].min(), df['price'].max()],
                        marks=None, tooltip={"placement": "bottom", "always_visible": True}),
                        html.Br(),
        html.Hr(),
        html.Details([
        html.Summary('View Column Descriptions', style={'cursor': 'pointer'}),
        dcc.Markdown("""
            - **price**: The final price of the property.
            - **property_size_sqft**: The total area of the property in square feet.
            - **constructed_year**: The year the property was originally built.
            - **previous_owners**: The number of previous owners.
            - **rooms**: The total number of rooms in the property.
            
            ---
            
            - **customer_salary**: The annual salary of the buyer.
            - **loan_amount**: The total amount of the loan taken for the property.
            - **loan_tenure_years**: The duration of the loan in years.
            - **monthly_expenses**: The buyer's average monthly expenses.
            - **down_payment**: The initial payment made by the buyer.
            - **emi_to_income_ratio**: The ratio of the monthly loan payment (EMI) to the buyer's monthly income. A lower value indicates less financial burden.
            
            ---
            
            - **satisfaction_score**: A satisfaction rating (1-10) from previous owners.
            - **neighbourhood_rating**: A rating (1-10) for the quality of the neighbourhood.
            - **connectivity_score**: A score (1-10) for how well the property is connected to transport and amenities.
            - **decision**: A binary outcome (0 or 1) which may indicate the result of a loan application or purchase decision.
        """, style={'marginTop': '10px'})
    ])
    ]),

    # --- Main Content Area ---
    html.Div(id='main-content', style={'width': '75%', 'padding': '20px'}, children=[
        dcc.Tabs(id="tabs-container", children=[
            
            # --- Tab 1: Market Overview ---
            dcc.Tab(label='Market Overview', children=[
                html.Div(style={'padding': '20px'}, children=[
                    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'textAlign': 'center'}, children=[
                        html.Div(id='kpi-properties', style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'width': '30%', 'backgroundColor': 'white'}),
                        html.Div(id='kpi-avg-price', style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'width': '30%', 'backgroundColor': 'white'}),
                        html.Div(id='kpi-avg-size', style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'width': '30%', 'backgroundColor': 'white'}),
                    ]),
                    html.Br(),
                    html.Div(style={'display': 'flex'}, children=[
                        dcc.Graph(id='graph-year-dist', style={'width': '50%'}), # ID 변경은 선택사항이지만 명확성을 위해 수정
                        dcc.Graph(id='graph-price-dist', style={'width': '50%'}),
                    ])
                ])
            ]),
            
            # --- Tab 2: Price Analysis ---
            dcc.Tab(label='Price Analysis', children=[
                html.Div(style={'padding': '20px'}, children=[
                    html.Div(style={'display': 'flex'}, children=[
                        dcc.Graph(id='graph-price-vs-size', style={'width': '50%'}),
                        dcc.Graph(id='graph-price-vs-year', style={'width': '50%'}),
                    ]),
                    html.Div(children=[
                        dcc.Graph(id='graph-price-vs-type'),
                    ])
                ])
            ]),

            # --- Tab 3: Customer Financials (MODIFIED) ---
            dcc.Tab(label='Customer Financials', children=[
                html.Div(style={'padding': '20px'}, children=[
                # Row 1
                    html.Div(style={'display': 'flex'}, children=[
                    dcc.Graph(id='graph-salary-expense', style={'width': '50%'}),
                    dcc.Graph(id='graph-price-downpayment', style={'width': '50%'})
                    ]),
                # Row 2
                    html.Div(style={'display': 'flex'}, children=[
                    dcc.Graph(id='graph-loan-tenure', style={'width': '50%'}),
                    dcc.Graph(id='graph-emi-ratio', style={'width': '50%'})
                    ])
                ])
            ]),

            # --- Tab 4: Ratings & Satisfaction ---
            dcc.Tab(label='Ratings & Satisfaction', children=[
                html.Div(style={'padding': '20px'}, children=[
                    html.Div(style={'display': 'flex'}, children=[
                        dcc.Graph(id='graph-price-rating', style={'width': '50%'}),
                        dcc.Graph(id='graph-satisfaction', style={'width': '50%'})
                    ])
                ])
            ]),
        ])
    ])
])


# 4. Define Callbacks
# ... (Chained dropdown callbacks are unchanged) ...
@app.callback(
    Output('city-dropdown', 'options'), Output('city-dropdown', 'value'),
    Input('country-dropdown', 'value'))
def update_city_options(selected_country):
    if not selected_country: return [], None
    filtered_df = df[df['country'] == selected_country]
    cities = sorted(filtered_df['city'].unique())
    return [{'label': city, 'value': city} for city in cities], None

@app.callback(
    Output('property-type-dropdown', 'options'), Output('property-type-dropdown', 'value'),
    Input('country-dropdown', 'value'), Input('city-dropdown', 'value'))
def update_property_type_options(selected_country, selected_city):
    if not selected_country or not selected_city: return [], None
    filtered_df = df[(df['country'] == selected_country) & (df['city'] == selected_city)]
    types = sorted(filtered_df['property_type'].unique())
    return [{'label': prop_type, 'value': prop_type} for prop_type in types], None

@app.callback(
    Output('furnishing-status-dropdown', 'options'), Output('furnishing-status-dropdown', 'value'),
    Input('country-dropdown', 'value'), Input('city-dropdown', 'value'), Input('property-type-dropdown', 'value'))
def update_furnishing_status_options(selected_country, selected_city, selected_type):
    if not selected_country or not selected_city or not selected_type: return [], None
    filtered_df = df[(df['country'] == selected_country) & (df['city'] == selected_city) & (df['property_type'] == selected_type)]
    statuses = sorted(filtered_df['furnishing_status'].unique())
    return [{'label': status, 'value': status} for status in statuses], None

# --- Main callback to update Tab 1 content (CHART MODIFIED) ---
@app.callback(
    Output('kpi-properties', 'children'),
    Output('kpi-avg-price', 'children'),
    Output('kpi-avg-size', 'children'),
    Output('graph-year-dist', 'figure'), # Output ID updated for clarity
    Output('graph-price-dist', 'figure'),
    Input('country-dropdown', 'value'),
    Input('city-dropdown', 'value'),
    Input('property-type-dropdown', 'value'),
    Input('furnishing-status-dropdown', 'value'),
    Input('price-slider', 'value')
)
def update_market_overview(country, city, prop_type, furnishing, price_range):
    dff = df.copy()
    # ... (Filtering logic is unchanged) ...
    if country: dff = dff[dff['country'] == country]
    if city: dff = dff[dff['city'] == city]
    if prop_type: dff = dff[dff['property_type'] == prop_type]
    if furnishing: dff = dff[dff['furnishing_status'] == furnishing]
    if price_range: dff = dff[(dff['price'] >= price_range[0]) & (dff['price'] <= price_range[1])]

    if dff.empty:
        # ... (No data logic is unchanged) ...
        empty_fig = go.Figure().update_layout(annotations=[dict(text="No data available", showarrow=False)])
        kpi_no_data = [html.H4("0"), html.P("Properties")]
        kpi_no_price = [html.H4("$0"), html.P("Average Price")]
        kpi_no_size = [html.H4("0 sqft"), html.P("Average Size")]
        return kpi_no_data, kpi_no_price, kpi_no_size, empty_fig, empty_fig

    # ... (KPI calculation is unchanged) ...
    num_properties = len(dff)
    avg_price = dff['price'].mean()
    avg_size = dff['property_size_sqft'].mean()
    kpi_props_children = [html.H4(f"{num_properties:,}"), html.P("Properties")]
    kpi_price_children = [html.H4(f"${avg_price:,.0f}"), html.P("Average Price")]
    kpi_size_children = [html.H4(f"{avg_size:,.0f} sqft"), html.P("Average Size")]

    # MODIFIED: Changed bar chart to histogram for constructed_year
    fig_year_dist = px.histogram(dff, x='constructed_year', title="Distribution by Constructed Year").update_layout(title_x=0.5, yaxis_title=None, xaxis_title="Construction Year")
    
    fig_price_dist = px.histogram(dff, x='price', title="Price Distribution").update_layout(title_x=0.5, yaxis_title=None, xaxis_title="Price")

    return kpi_props_children, kpi_price_children, kpi_size_children, fig_year_dist, fig_price_dist

# --- Main callback to update Tab 2 content (unchanged) ---
@app.callback(
    Output('graph-price-vs-size', 'figure'),
    Output('graph-price-vs-year', 'figure'),
    Output('graph-price-vs-type', 'figure'),
    Input('country-dropdown', 'value'),
    Input('city-dropdown', 'value'),
    Input('property-type-dropdown', 'value'),
    Input('furnishing-status-dropdown', 'value'),
    Input('price-slider', 'value')
)
def update_price_analysis(country, city, prop_type, furnishing, price_range):
    # ... (This entire function's logic is unchanged) ...
    dff = df.copy()
    if country: dff = dff[dff['country'] == country]
    if city: dff = dff[dff['city'] == city]
    if prop_type: dff = dff[dff['property_type'] == prop_type]
    if furnishing: dff = dff[dff['furnishing_status'] == furnishing]
    if price_range: dff = dff[(dff['price'] >= price_range[0]) & (dff['price'] <= price_range[1])]

    if dff.empty:
        empty_fig = go.Figure().update_layout(annotations=[dict(text="No data available", showarrow=False)])
        return empty_fig, empty_fig, empty_fig

    fig_price_size = px.scatter(dff, x='property_size_sqft', y='price', title="Price vs. Property Size", labels={'property_size_sqft': 'Size (sqft)', 'price': 'Price'}).update_layout(title_x=0.5)
    fig_price_year = px.scatter(dff, x='constructed_year', y='price', trendline="ols", title="Price vs. Construction Year", labels={'constructed_year': 'Construction Year', 'price': 'Price'}).update_layout(title_x=0.5)
    fig_price_type = px.box(dff, x='property_type', y='price', title="Price Distribution by Property Type", labels={'property_type': 'Property Type', 'price': 'Price'}).update_layout(title_x=0.5)

    return fig_price_size, fig_price_year, fig_price_type

@app.callback(
    # Output이 4개로 늘어남
    Output('graph-salary-expense', 'figure'),
    Output('graph-price-downpayment', 'figure'),
    Output('graph-loan-tenure', 'figure'),
    Output('graph-emi-ratio', 'figure'),
    [Input(i, 'value') for i in ['country-dropdown', 'city-dropdown', 'property-type-dropdown', 'furnishing-status-dropdown', 'price-slider']]
)
def update_customer_financials(country, city, prop_type, furnishing, price_range):
    dff = df.copy()
    if country: dff = dff[dff['country'] == country]
    if city: dff = dff[dff['city'] == city]
    if prop_type: dff = dff[dff['property_type'] == prop_type]
    if furnishing: dff = dff[dff['furnishing_status'] == furnishing]
    if price_range: dff = dff[(dff['price'] >= price_range[0]) & (dff['price'] <= price_range[1])]

    if dff.empty:
        empty_fig = go.Figure().update_layout(annotations=[dict(text="No data available", showarrow=False)])
        return empty_fig, empty_fig, empty_fig, empty_fig

    # 차트 1: 급여 vs 월 지출 (신규)
    fig_salary_expense = px.scatter(
        dff,
        x='customer_salary',
        y='monthly_expenses',
        title="Monthly Expenses vs. Customer Salary",
        labels={'customer_salary': 'Customer Salary', 'monthly_expenses': 'Monthly Expenses'}
    ).update_layout(title_x=0.5)

    # 차트 2: 가격 vs 계약금 (신규)
    fig_price_downpayment = px.scatter(
        dff,
        x='price',
        y='down_payment',
        title="Down Payment vs. Property Price",
        labels={'price': 'Property Price', 'down_payment': 'Down Payment'}
    ).update_layout(title_x=0.5)

    # 차트 3: 대출 기간 분포 (신규)
    tenure_counts = dff['loan_tenure_years'].value_counts().reset_index()
    tenure_counts.columns = ['loan_tenure_years', 'count'] 
    
    fig_loan_tenure = px.bar(
        tenure_counts,
        x='loan_tenure_years',
        y='count',
        title="Loan Tenure Distribution",
        labels={'loan_tenure_years': 'Loan Tenure (Years)', 'count': 'Number of Properties'}
    ).update_layout(title_x=0.5)

    # 차트 4: 소득 대비 월 상환액 비율 (기존)
    fig_emi_ratio = px.histogram(
        dff,
        x='emi_to_income_ratio',
        title="EMI to Income Ratio Distribution",
        labels={'emi_to_income_ratio': 'EMI to Income Ratio'}
    ).update_layout(title_x=0.5)
    
    return fig_salary_expense, fig_price_downpayment, fig_loan_tenure, fig_emi_ratio


# --- Callback to update Tab 4 content ---
@app.callback(
    Output('graph-price-rating', 'figure'),
    Output('graph-satisfaction', 'figure'),
    [Input(i, 'value') for i in ['country-dropdown', 'city-dropdown', 'property-type-dropdown', 'furnishing-status-dropdown', 'price-slider']]
)
def update_ratings_satisfaction(country, city, prop_type, furnishing, price_range):
   
    dff = df.copy()
    if country: dff = dff[dff['country'] == country]
    if city: dff = dff[dff['city'] == city]
    if prop_type: dff = dff[dff['property_type'] == prop_type]
    if furnishing: dff = dff[dff['furnishing_status'] == furnishing]
    if price_range: dff = dff[(dff['price'] >= price_range[0]) & (dff['price'] <= price_range[1])]

    if dff.empty:
        empty_fig = go.Figure().update_layout(annotations=[dict(text="No data available", showarrow=False)])
        return empty_fig, empty_fig

    # 가격 vs 주변 환경 등급 산점도
    fig_price_rating = px.scatter(
        dff,
        x='neighbourhood_rating',
        y='price',
        title="Price vs. Neighbourhood Rating",
        labels={'neighbourhood_rating': 'Neighbourhood Rating', 'price': 'Price'}
    ).update_layout(title_x=0.5)

    # 만족도 점수 분포 바 차트
    satisfaction_counts = dff['satisfaction_score'].value_counts().reset_index()
    satisfaction_counts.columns = ['satisfaction_score', 'count']
    fig_satisfaction = px.bar(
        satisfaction_counts,
        x='satisfaction_score',
        y='count',
        title="Satisfaction Score Distribution",
        labels={'satisfaction_score': 'Satisfaction Score', 'count': 'Number of Properties'}
    ).update_layout(title_x=0.5)

    return fig_price_rating, fig_satisfaction
# 5. Run the App
server = app.server

# %%



