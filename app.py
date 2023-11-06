#Import the required libraries
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import numpy as np
import pandas as pd
import plotly.express as px

#read the data
df1 = pd.read_excel('QSR_dataset.xlsx',index_col=0)

#Create new dataframe from the original dataframe with only numerical features to be used for correlation plot
df_ = df1.select_dtypes(include='number')

#create the Average spent per hour by by dividing the sales column by the ticket column
df_['AVS Per Hour'] = df_['Sales']/df_['Ticket']

#transform the dataframe using pd.melt()function
df2 = df1.melt(id_vars=['Date', 'Time', 'Ticket', 'Sales'],
             var_name='Items', 
             value_name='Quantity')

#create more features from the current features like days, months weeks and so on
df2 = df2[['Date','Time','Items','Quantity','Ticket','Sales']]
df2['Date'] = pd.to_datetime(df2['Date'],dayfirst=True)
df2['AVS Per Hour'] = df2['Sales'] / df2['Ticket']
df2['Month'] = df2['Date'].dt.month_name()
df2['Week Days'] = df2['Date'].dt.day_name()
df2['Month Weeks'] = (df2['Date'].dt.day-1)//7+1
df2['Month Weeks'] = df2['Month Weeks'].apply(lambda x: x if x <= 4 else 1)
df2=df2[['Date','Month','Month Weeks', 'Week Days','Time', 'Items', 'Quantity', 'Ticket', 'Sales', 'AVS Per Hour']]
df2['Month Weeks'] = np.where(df2['Month Weeks'] == 4, 'Fourth Week',
                             np.where(df2['Month Weeks'] == 3, 'Third Week',
                                      np.where(df2['Month Weeks'] == 2, 'Second Week', 'First Week')))

#categorize the features into groups with which to filter the dataset with to make it readable
cereal_packages = [
            'Backup Max', 
            'Backup',  
            'Mid Meal', 
            'Backup Max Chripsy PC', 
            'Monster Meal',
            'Backup Chrispy Meal', 
            'Backup Max Cubes', 
            'Mid Chrispy Meal',  
            'R & B', 
            'Fried Rice', 
            '8PC Meal', 
            '10PC Meal', 
            'Backup Cubes Meal',
            'Pasta', 
            'Crew Meal', 
            'Mid',  
            'Mid Chrispy', 
            '1/4 Rot Lite Meal', 
            '4PC Love Meal', 
            'Lovers Cube Meal', 
            'Face-up Meal', 
            'Plain Rice', 
            'Face-up',  
            'Jollof Rice', 
            'Love Meal',
            'PC Mixed Rice and Drink', 
            '1/4 Rot Mixed Rice and Drink', 
            '1/4 Rot Mixed Rice', 
            'PC Mixed Rice', 
            'Max Jollof Rice', 
            'Max Fried Rice', 
            '1/4 Rot Meal',
            '1/2 Rot Meal'
            ]

chicken_packages = [ 
            '8PC Chripsy', 
            '1PC',  
            '1/4 Rot', 
            '2PC Chrispy',
            'Rot', 
            '4PC Chrispy', 
            '1PC Chrispy', 
            '8PC Chrispy', 
            '4PC', 
            '2PC',  
            '1PC Rot',  
            '4PC Rot',  
            '8PC Rot', 
            '2PC Rot', 
            '1/2 Rot',            
            ]

call_to_order = [ 
            'Cubes', 
            '270g Chips', 
            'Burger', 
            'SW', 
            '1/4 Rot Chips', 
            'Sharwama',  
            'Max SW Meal',  
            'Burger Meal',  
            'Shawama Meal', 
            'Max SW', 
            'Express Meal', 
            'Express Chripsy Meal', 
            '180g Chips', 
            'SW Meal', 
            'Express', 
            '1/2 Rot Chips', 
            'Express Chripsy',  
            'Max Spicy SW',
            'Spicy SW', 
            'Max Spicy SW Meal ', 
            'Spicy SW Meal', 
            'Mid Chips Meal', 
            'Mid Chips', 
            'Mid Chrispy Chips Meal', 
            '200g Cubes'
            ]

others = [
            '50cl Drink', 
            'Veg Salad',
            'Chicken Pie', 
            'Meat Pie', 
            'Moin Moin', 
            'Chicken Salad Meal',
            'Salad',  
            'Chicken Salad', 
            'Monster',  
            '75cl Water', 
            'R & B Sauce', 
            'Cheese', 
            'Coffee', 
            'Plastic Pack', 
            '60cl Zero',  
            '200g Salad', 
            '200g Veg Salad',  
            'Ketchup', 
            '350ml Cup',
            "250ml Cup", 
            'Cone',
            ]

#instantiate the app
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP,{
                    'rel':"stylesheet",
                    'href':"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css", 
                    'integrity':"sha512-z3gLpd7yknf1YoNbCzqRKc4qyor8gaKU1qmn+CShxbuBusANI9QpRohGBreCFkKxLhei6S9CQXFEbbKuqLg0DA==",
                    'crossorigin':"anonymous",
                    'referrerpolicy':"no-referrer"
                }],
                title='QSR Sales Dashboard',
                meta_tags=[
                    {'charset':"UTF-8"},
                    {'http-equiv':"X-UA-Compatible", 'content':"IE=edge"},
                    {'name':"viewport", 'content':"width=device-width, initial-scale=1.0"}
                ]
)

#the app layout
app.layout = html.Div([
    html.Header([
        #navigation bar
        html.Nav([
            html.Div([
                html.I(
                    className="fa-solid fa-bars fa-xl",
                    id='toggle-icon_menu'
                ),
            ],id='main_header__sidebar_toggle', className='main_header_icon_and_dropdown'),
            html.Div([
                    dcc.Dropdown(
                        id='dataset_group',
                        options=[
                            {'label':'Cereal Packs','value':'cereal_packages'},
                            {'label':'Chicken Packs','value':'chicken_packages'},
                            {'label':'Call To Order','value':'call_to_order'},
                            {'label':'Others','value':'others'}
                        ],
                        value = 'cereal_packages'
                    ),
                    dcc.Dropdown(
                        id='data_aggregator',
                        options=[
                            {'label':'Minimum','value':'Minimum'},
                            {'label':'Average','value':'Average'},
                            {'label':'Maximum','value':'Maximum'},
                            {'label':'Total','value':'Total'}
                        ],
                        value='Average'
                    )
            ],id='main_header-dropdown', )
        ],className='main_header_icon_and_dropdown')
    ], id='main_header'),
    html.Section([
        html.Div(id='overlay'),
        #the sidebar
        html.Div([
            html.Div([
                html.Div([
                     html.H3([
                         html.Span(['D'],className='dtext'),
                         'ATA',
                         html.Span(['R'],className='dtext'),
                         'EALM'],id='brand_text'),
                ],id='brand')
            ],id='sidebar_header'),
            html.Div([
                dcc.DatePickerRange(
                    id='date-picker',
                    display_format='DD-MM-YYYY',
                    min_date_allowed='24-11-2021',
                    max_date_allowed='30-04-2023'
                ),
            ]),
            html.Div([
                dbc.Tabs([
                    dbc.Tab([
                        html.H6('Intoduction'),
                        html.P("Having been around for sometime now, significant number of people have resorted to them for their daily source of food. Depending on the location, a particular brand of QRS will have a variation in product demand from one store to the other as a result of customers' irrationality. This situation leads to poor planning and management in the individual stores to meet up with daily needs of the customers in the area of what products, what raw materials, how many working team etc, should be available at a given period to meet up with the daily need of the customers as each QRS work to minimize cost and maximize profit."),
                        html.H6('Statemenrt of Problem'),
                        html.P("Due to large customer base and limited resources such as staffing, raw materials and the likes,QSR are faced with a challenge in satisfing the needs of different customers in different times of the day. In this project, daily product sales data from an arbitrary QSR store from the time the store was openned are analyzed so as to note how customers come in at different hours of the day, how they spend what items they buy at these hours to enable the store's management in making proper planning."),
                        html.H6('The Dataset'),
                        html.P("The Dataset comprises of daily sales in quantity of products, number of tickets and amount of sales for every hour of the day from 24th November, 2021 to 30th April,2023. From the given features, other features were introduced such as Average Spent per hour. Other features are the month, the week, the day of the week the sales took place. This was necessary to see how product sales trend at  period."),
                        html.H6('Data Intergrity'),
                        html.P("Some technical challenges affected the data which are as follows:"),
                        html.Ol([
                            html.Li("System Failure: Due to system failures, some orders were not tendered at the time of purchase. At these times the orders were tenders at the close of shifts basically when the system has been respored."),
                            html.Li("Error Tender: Sometimes, due to upskilling of the team or excessive rush at some hours of the day, it is common to record some errors in the process of taking some order. There is room to correct to wrongly taken orders but not in the event that they have tendered and not reported."),
                            html.Li("Product Skip: Some cashiers may skip some products while taking an order occassionally. In such situations, the skiped products are tendered at the end of day after internal product control."),
                            html.Li("National Holidays: Some national holidays prohibit the opening of social center to enable citizen execise their rights such as election days."),
                        ]),
                        html.P("In the above situation, data have either been misinputted or lost entirely. In the situation where data are misimputed, the extent to which existing data are impacted are examined. The wrongly imputed data are replaced with the mean at that particular time. In the event that the data are entered at rhe end of the day at late hours, the data for that entire day are discarded. On national holidays, there are no data at all."),
                        html.H6('Analytic Strategy'),
                        html.P("The strategy employed was to group the dataset by hour of the day and monitor the products that were sold at each hour of sales in minmum, average, maximum and total sales. Then, the dataset is grouped by product and then monitor how each product perform at different hours of the day."),
                        html.P([
                            html.Span(['Note:'],id='red'),
                            "This project is based on randomly generated data due to the authors experience and interest in QRS. It is mainly to be used for eductional purpose. Random names have been used to represent products and as such, any resemblence to real life data is a pure coincidence."
                        ])
                    ],label='Project',tab_id='project_tab',className='tab_ind'),
                    dbc.Tab([
                        html.P("The dataset was classified into four product categories namely: Cereal Packs, Chicken Packs, Call to Order and others to facilitate readability due to large number of products."),
                        html.Ol([
                            html.Li("Cereal Packs: The products here are products that must go with cereal."),
                            html.Li("Chicken Packs: Chicken Packs are packages that only include chicken products."),
                            html.Li("Call to Order: This peoduct category has to do with only products that are made when there are ordered."),
                            html.Li("Others: This category has to do with other miscelleanous products that can be found in the store."),
                        ]),
                        html.H6('Aggretating Functions'),
                        html.P("Four major aggregating fuctions were used to aggregate the dataset which are as follows:"),
                        html.Ol([
                            html.Li("Minimum: To compute the minimum of the numerical variables in consideration."),
                            html.Li("Average: To compute the mean of the varriables of the variables in consideration."),
                            html.Li("Maximum: to compute the maximum values within the variables under consideration."),
                            html.Li("Total: To compute the sum of the variables of interests."),
                        ]),
                        html.P("The aggregating functions can be accessed from the Navigation bar. The aggregating functions control the first three sections of the layout."),
                        html.H6('Layout'),
                        html.P("Structurally, the layout is indirectly divided into four:"),
                        html.Ol([
                            html.Li("Section 1: This section contains four cards, a barchart and a doughnut chart. This is where the results from filtering the dataset by time and  grouping by product is displayed. When a time is selected, the dataset is grouped by the products. The sum of the variables depending on the aggregating function are displayed in the cards. The barchart plots the products sold at the selected time will be plotted. The doughnut chat plots the percentage contribution of the each of products against the rest of the products at the selected time."),
                            html.Li("Section 2: This section contains three plots: a doughnut chart, a bobble chart and a line chart. This is where the results of filtering the dataset by product and by time is displayed. The doughnut chart displays the percentage of the quantity of the selected product that sold by the selected time against the other hours of the day. In the bobble chart, the quantity of the product selected is plotted against the number of tickets and the size of the markers emphasize the sales at the time. In the line chart, the quantity of the selected product as sold throughout the hours of the day is plotted. In the line chart, it is possible to monitor sales per hour, ticket per hour and AVS per hour by selecting the appropriate option from the dropdown above the chart."),
                            html.Li("Section 3: This section contains only a single chart. The chart is a grouped barchart where different (or same) products can be compared to each other over diiferent or same period. To compare, the dataset is filtered from the dropdowns by the left and the ones by the right."),
                            html.P("Note: The three sections as described above are controlled by the aggregating function. That is, the values displayed could be minimum, average, maximum or sum depending on the aggregating function selected."),
                            html.Li("Section 4: This section is where the correlation chart is plotted. All the numerical features can be plotted against each other to moniter how they correlate with each other."),
                        ]),
                        html.P("Explaining the charts used for this project is boyond the primary focus of the project. They are vast materials online that explan the charts. Feel free to sort for these materials if need be.")
                    ],label='Guide',tab_id='note_tab',className='tab_ind'),
                    dbc.Tab([
                        html.Label('Month',className='control_label'),
                        dcc.Dropdown(id='sidebar_month_selector',
                                        multi=True),
                        html.Label('Week',className='control_label'),
                        dcc.Dropdown(id='sidebar_week_selector',
                                        multi=True),
                        html.Label('Week Day',className='control_label'),
                        dcc.Dropdown(id='sidebar_weekday_selector',
                                        multi=True)
                    ],label='Filter',tab_id='filter_tab',className='tab_ind'),
                ],id='tabs',
                  active_tab='filter_tab'
                )               
            ], id='tab_container'),
            html.Div([
                html.Img(
                    src=app.get_asset_url('ra1.jpg'),
                    id='image', 
                    className='shadow'),
                html.Div([
                    html.A(
                        html.I(id='github', className='fa-brands fa-square-github fa-2xl'),
                        href='https://github.com/amaechi01',
                        target='_blank'
                    ),    
                    html.A(
                        html.I(id='linkedin', className='fa-brands fa-linkedin fa-2xl'),
                        href='http://linkedin.com/in/oshim-amaechi',
                        target='_blank'
                    ),  
                    html.A(
                        html.I(id='skype', className='fa-brands fa-skype fa-2xl'),
                        href='https://join.skype.com/invite/BXEEHj5bHDv2',
                        target='_blank'
                    ),    
                ],id='contact')
            ],className='info')            
        ],id='sidebar'),
        #project title
        html.Div([
            html.Div([
                 html.I(
                    className="fa-solid fa-bowl-food fa-bounce fa-2xl t_icon",
                ),
            ],id='product-logo', className='three columns'),
            html.Div([
                html.H1('QSR Sales Data Analysis',id='Main_title')
            ],className='six columns title_text'),
            html.Div([
                'Oshim Amaechi'
            ],id='author',className='three columns'),
        ],id='title_container',className='row flex-display'),
        html.Div([
            html.Div([
                html.Label('Time'),
                dcc.Dropdown(id='hour',className='time_item')
            ],id='hour_dropdown', className='body_dropdown four columns'),
            html.Div([  
                html.A( 
                    html.Img(
                        src=app.get_asset_url('dash-logo.png'),
                        id='plotly'
                    ),
                    href='https://dash.plotly.com',
                    target='_blank'
                )             
            ],id='plotly_img_container', className='three columns')
        ],id='plotly_img_row',className='row flex-display '),
        #section1: Cards
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.P(id='quantity_aggregate'),
                        html.H3(id='quantity_aggregate_value')
                    ],className='card_info'),
                    html.Div([
                        html.I(
                            className='fa-solid fa-list-ol fa-2xl icon'
                        )
                    ],className='card_icon')
                ],id='card1',className='card_container four columns'),
                html.Div([
                    html.Div([
                        html.P(id='ticket_aggregate'),
                        html.H3(id='ticket_aggregate_value')
                    ],className='card_info'),
                    html.Div([
                        html.I(
                            className='fa-solid fa-users fa-2xl icon'
                    )
                    ],className='card_icon')
                ],id='card2',className='card_container four columns'),
            ],className='pair pair2'),
            html.Div([
                html.Div([
                    html.Div([
                        html.P(id='sales_aggregate'),
                        html.H3(id='sales_aggregate_value')
                    ],className='card_info'),
                    html.Div([
                        html.I(
                            className='fa-solid fa-money-bill fa-2xl icon')
                    ],className='card_icon'),
                ],id='card3',className='card_container four columns'),
                html.Div([
                    html.Div([
                        html.P(id='avs_aggregate'),
                        html.H3(id='avs_aggregate_value')
                    ],className='card_info'),
                    html.Div([
                        html.I(
                            className='fa-solid fa-gauge fa-2xl icon'
                        )
                    ],className='card_icon')    
                ],id='card4',className='card_container four columns'),
            ],className='pair pair1'),
        ],id='cards',className='card-container row flex-display'),
        #section1: Barchart and Doughnut Chart
        html.Div([
            html.Div([
                html.H5(id='product_by_hour',className='graph_title'),
                html.Div([
                    dcc.Loading([
                        dcc.Graph(id='products_by_hour',className='graph'),
                    ],color='#021d3a')
                ],className='scroll'),  
            ],className='graph-container seven columns'),
            html.Div([
                html.H5(id='item_percentage_by_hour',className='graph_title'),
                dcc.Dropdown(id='select_product'),
                html.Div([
                    dcc.Loading([
                        dcc.Graph(id='percentage_item_by_hour',className='graph')
                    ],color='#021d3a')
                ],className='scroll'),
            ],className='graph-container five columns adj'),
        ],className='row flex-display'),
        html.Div([
            html.Div([
                html.Label('Product'),
                dcc.Dropdown(id='item',className='time_item')
            ],id='item_dropdown',className='body_dropdown four columns')
        ],id='item_dropdown_row',className='row flex-display'),
        #section2: doughtnut chart and bobble chart
        html.Div([
            html.Div([
                html.H5(id='hourly_item_quantity_percentage',className='graph_title'),
                dcc.Dropdown(id='select_time'),
                html.Div([
                    dcc.Loading([
                        dcc.Graph(id='hourly_quantity_percent',className='graph')
                    ],color='#021d3a')
                ],className='scroll'),
            ],className='graph-container five columns'),
            html.Div([
                html.H5(id='bobble_chart_title',className='graph_title'),
                html.Div([
                    dcc.Loading([
                        dcc.Graph(id='bobble_chart',className='graph')
                    ],color='#021d3a')
                ],className='scroll'),                
            ],className='graph-container seven columns adj')
        ],className='row flex-display'),
        #section2: line chart
        html.Div([
            html.Div([               
                html.H5(id='trend_plot_title',className='graph_title'),
                dcc.Dropdown(
                    id='feature_',
                    options=[
                        {'label':'Quantity', 'value':'Quantity'},
                        {'label':'Ticket', 'value':'Ticket'},
                        {'label':'Sales', 'value':'Sales'},
                        {'label':'AVS Per Hour', 'value':'AVS Per Hour'},
                    ],
                    value='Quantity'
                ),
                html.Div([
                    dcc.Loading([
                        dcc.Graph(id='trend_plot',className='graph') 
                    ],color='#021d3a') 
                ],className='scroll'),      
            ],className='full twelve columns graph-container')
        ],id='full1',className='row flex-display'),
        #compertion graph
        html.Div([
            html.Div([
                html.Div([
                    html.Label('Date'),
                    dcc.DatePickerRange(
                        id='comp_date-picker1',
                        display_format='DD-MM-YYYY',
                        min_date_allowed='24-11-2021',
                        max_date_allowed='30-04-2023'
                    ),
                    html.Label('Month'),
                    dcc.Dropdown(id='comp_month_selector1',className='select'),
                    html.Label('Week'),
                    dcc.Dropdown(id='comp_week_selector1',className='select'),
                    html.Label('Week Day'),
                    dcc.Dropdown(id='comp_weekday_selector1',className='select'),
                    html.Label('Product'),
                    dcc.Dropdown(id='comp_product_selector1',className='select')
                ],id='control1', className='two columns control'),
                html.Div([
                    html.H5(id='comp_plot_title',className='graph_title'),
                    html.Div([
                        dcc.Loading([
                            dcc.Graph(id='comp_plot',className='graph')
                        ],color='#021d3a')
                    ],className='scroll'),
                ],className='eight columns'),            
                html.Div([
                    html.Label('Date'),
                    dcc.DatePickerRange(
                        id='comp_date-picker2',
                        display_format='DD-MM-YYYY',
                        min_date_allowed='24-11-2021',
                        max_date_allowed='30-04-2023'
                    ),
                    html.Label('Month'),
                    dcc.Dropdown(id='comp_month_selector2',className='select'),
                    html.Label('Week'),
                    dcc.Dropdown(id='comp_week_selector2',className='select'),
                    html.Label('Week Day'),
                    dcc.Dropdown(id='comp_weekday_selector2',className='select'),
                    html.Label('Product'),
                    dcc.Dropdown(id='comp_product_selector2',className='select')
                ],id='control2', className='two columns control')
            ],className='twelve columns graph-container comp')
        ],id='full2',className='row flex-display'),
        #correlation plot
        html.Div([
            html.Div([
                html.H5(id='scatter_plot_title', className='graph_title'),
                html.Div([
                    html.Div([
                        dcc.Dropdown(id='feature1',
                                    options=[{'label':val, 'value':val} for val in df_.columns],
                                    value='Ticket'),
                    ],className='correlation_control_container'),
                    html.Div([
                        dcc.Dropdown(id='feature2',
                                    options=[{'label':val, 'value':val} for val in df_.columns],
                                    value='AVS Per Hour')
                    ],className='correlation_control_container'),
                ],className='correlation_control'),
                html.Div([
                    dcc.Loading([
                        dcc.Graph(id='scatter_plot',className='graph')
                    ],color='#021d3a')
                ],className='scroll'),
            ],className='twelve columns graph-container')
        ],id='full3',className='row flex-display')
    ],id='layout-section')
],id='main-container')

#toggle callback function to display or hide the sidebar
@app.callback(
    Output('sidebar', 'className'),
    Output('toggle-icon_menu', 'className'),
    Output('overlay', 'className'),
    Input('toggle-icon_menu', 'n_clicks'),
    State('sidebar', 'className'),
    State('overlay', 'className'),
    prevent_initial_call=True
)
def toggle_sidebar(toggle_icon_clicks, sidebar_class, overlay_class):
    # Check the number of clicks to toggle the sidebar
    if toggle_icon_clicks % 2 == 1:
        sidebar_class = 'open'
        overlay_class = 'active'
        toggle_icon_class = 'fa-solid fa-xmark fa-xl'              
    else:
        sidebar_class = ''
        overlay_class = ''
        toggle_icon_class = 'fa-solid fa-bars fa-xl'
    return sidebar_class, toggle_icon_class, overlay_class

#the approach is to use the dropdowns to filter the dataset
#when a value is selected the resulting dataset is expected to have only the values available
#within the range selected

#filter by group and output options to date picker
@app.callback(
    Output('date-picker','start_date'),
    Output('date-picker','end_date'),
    Input('dataset_group', 'value')
)
def group_dataset(group):
    #set the default value to cereal packs
    if not group:
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        start_date = grouped_df2['Date'].min()
        end_date = grouped_df2['Date'].max()
    elif group =='cereal_packages':
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        start_date = grouped_df2['Date'].min()
        end_date = grouped_df2['Date'].max()
    elif group == 'chicken_packages':
        grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
        start_date = grouped_df2['Date'].min()
        end_date = grouped_df2['Date'].max()
    elif group == 'call_to_order':
        grouped_df2 = df2[df2['Items'].isin(call_to_order)]
        start_date = grouped_df2['Date'].min()
        end_date = grouped_df2['Date'].max()
    else:
        grouped_df2 = df2[df2['Items'].isin(others)]
        start_date = grouped_df2['Date'].min()
        end_date = grouped_df2['Date'].max()
    return start_date, end_date

#filter by date and output options to month selector
@app.callback(
    Output('sidebar_month_selector', 'options'),
    Output('sidebar_month_selector', 'value' ),
    Input('dataset_group', 'value'),
    Input('date-picker','start_date'),
    Input('date-picker', 'end_date')
)
def date_filter(group, start_date, end_date):
    if not group:
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
    elif group =='cereal_packages':
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
    elif group == 'chicken_packages':
        grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
    elif group == 'call_to_order':
        grouped_df2 = df2[df2['Items'].isin(call_to_order)]
    else:
        grouped_df2 = df2[df2['Items'].isin(others)]

    date_filtered_df2 = grouped_df2[(grouped_df2['Date']>=start_date) & (grouped_df2['Date']<=end_date)]
    options = [{'label':val,'value':val} for val in date_filtered_df2['Month'].unique()]
    value = [val for val in date_filtered_df2['Month'].unique()]
    return options, value

#filter by month and output options to week selector
@app.callback(
    Output('sidebar_week_selector', 'options'),
    Output('sidebar_week_selector', 'value'),
    Input('dataset_group', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('sidebar_month_selector', 'value')
)
def month_filter(group, start_date, end_date, month):
    if not group:
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
    elif group =='cereal_packages':
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
    elif group == 'chicken_packages':
        grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
    elif group == 'call_to_order':
        grouped_df2 = df2[df2['Items'].isin(call_to_order)]
    else:
        grouped_df2 = df2[df2['Items'].isin(others)]

    date_filtered_df2 = grouped_df2[(grouped_df2['Date']>=start_date) & (grouped_df2['Date']<=end_date)]
    
    if not month:
        month_filtered_df2 = date_filtered_df2
    else:
        try:
            month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'] == month]
        except ValueError:
            month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'].isin(month)]
    
    options = [{'label':val,'value':val} for val in  month_filtered_df2 ['Month Weeks'].unique()]
    value = [val for val in  month_filtered_df2['Month Weeks'].unique()]
    return options, value

#filter by week and output weekday selector
@app.callback(
    Output('sidebar_weekday_selector', 'options'),
    Output('sidebar_weekday_selector', 'value'),
    Input('dataset_group', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('sidebar_month_selector', 'value'),
    Input('sidebar_week_selector', 'value')
)
def week_filter(group, start_date, end_date, month, week):
    if not group:
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
    elif group =='cereal_packages':
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
    elif group == 'chicken_packages':
        grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
    elif group == 'call_to_order':
        grouped_df2 = df2[df2['Items'].isin(call_to_order)]
    else:
        grouped_df2 = df2[df2['Items'].isin(others)]

    date_filtered_df2 = grouped_df2[(grouped_df2['Date']>=start_date) & (grouped_df2['Date']<=end_date)]
    
    if not month:
        month_filtered_df2 = date_filtered_df2
    else:
        try:
            month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'] == month]
        except ValueError:
            month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'].isin(month)]
    
    if not week:
        week_filtered_df2 = month_filtered_df2
    else:
        try:
            week_filtered_df2 = month_filtered_df2[month_filtered_df2['Month Weeks'] == week]
        except ValueError:
            week_filtered_df2 = month_filtered_df2[month_filtered_df2['Month Weeks'].isin(week)]
    
    options = [{'label':val,'value':val} for val in week_filtered_df2['Week Days'].unique()]
    value = [val for val in week_filtered_df2['Week Days'].unique()]
    
    return options, value

# filter by weekday and and by hour
@app.callback(
    Output('hour', 'options'),
    Output('hour','value'),
    Output('item', 'options'),
    Output('item', 'value'),
    Input('dataset_group', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('sidebar_month_selector', 'value'),
    Input('sidebar_week_selector', 'value'),
    Input('sidebar_weekday_selector','value')
)
def weekday_filter(group, start_date, end_date, month, week, weekday):
    if not group:
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
    elif group =='cereal_packages':
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
    elif group == 'chicken_packages':
        grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
    elif group == 'call_to_order':
        grouped_df2 = df2[df2['Items'].isin(call_to_order)]
    else:
        grouped_df2 = df2[df2['Items'].isin(others)]

    date_filtered_df2 = grouped_df2[(grouped_df2['Date']>=start_date) & (grouped_df2['Date']<=end_date)]
    
    if not month:
        month_filtered_df2 = date_filtered_df2
    else:
        try:
            month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'] == month]
        except ValueError:
            month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'].isin(month)]
    
    if not week:
        week_filtered_df2 = month_filtered_df2
    else:
        try:
            week_filtered_df2 = month_filtered_df2[month_filtered_df2['Month Weeks'] == week]
        except ValueError:
            week_filtered_df2 = month_filtered_df2[month_filtered_df2['Month Weeks'].isin(week)]
    
    if not weekday:
        weekday_filtered_df2 = week_filtered_df2
    else:
        try:
            weekday_filtered_df2 = week_filtered_df2[week_filtered_df2['Week Days']==weekday]
        except ValueError:
            weekday_filtered_df2 = week_filtered_df2[week_filtered_df2['Week Days'].isin(weekday)]
    options1 = [{'label':val,'value':val} for val in weekday_filtered_df2['Time'].unique()]
    value1 = weekday_filtered_df2['Time'].unique()[0]
    options2 = [{'label':val,'value':val} for val in weekday_filtered_df2['Items'].unique()]
    value2 = weekday_filtered_df2['Items'].unique()[0]
    
    return options1, value1, options2, value2

#plot the barchart in section 1 and output options to product selector for doughnut plot
#populate the cards with info
@app.callback(
    Output('select_product','options'),
    Output('select_product','value'),
    Output('quantity_aggregate','children'),
    Output('quantity_aggregate_value','children'),
    Output('ticket_aggregate','children'),
    Output('ticket_aggregate_value','children'),
    Output('sales_aggregate','children'),
    Output('sales_aggregate_value','children'),
    Output('avs_aggregate','children'),
    Output('avs_aggregate_value','children'),
    Output('products_by_hour','figure'),
    Output('product_by_hour','children'),
    Input('dataset_group', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('sidebar_month_selector', 'value'),
    Input('sidebar_week_selector', 'value'),
    Input('sidebar_weekday_selector','value'),
    Input('hour','value'),
    Input('data_aggregator','value'),
)
def hourly_update(group, start_date, end_date, month, week, weekday, hour, aggregator):
    try:   
        if not group:
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group =='cereal_packages':
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group == 'chicken_packages':
            grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
        elif group == 'call_to_order':
            grouped_df2 = df2[df2['Items'].isin(call_to_order)]
        else:
            grouped_df2 = df2[df2['Items'].isin(others)]

        date_filtered_df2 = grouped_df2[(grouped_df2['Date']>=start_date) & (grouped_df2['Date']<=end_date)]
        
        if not month:
            month_filtered_df2 = date_filtered_df2
        else:
            try:
                month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'] == month]
            except ValueError:
                month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'].isin(month)]
        
        if not week:
            week_filtered_df2 = month_filtered_df2
        else:
            try:
                week_filtered_df2 = month_filtered_df2[month_filtered_df2['Month Weeks'] == week]
            except ValueError:
                week_filtered_df2 = month_filtered_df2[month_filtered_df2['Month Weeks'].isin(week)]
        
        if not weekday:
            weekday_filtered_df2 = week_filtered_df2
        else:
            try:
                weekday_filtered_df2 = week_filtered_df2[week_filtered_df2['Week Days']==weekday]
            except ValueError:
                weekday_filtered_df2 = week_filtered_df2[week_filtered_df2['Week Days'].isin(weekday)]

        if not hour:
            hourly_filtered_df2 = weekday_filtered_df2[weekday_filtered_df2['Time']==weekday_filtered_df2['Time'].unique()[0]]
            title=f'{aggregator} Quantity of Items Sold from {weekday_filtered_df2["Time"].unique()[0]}'
        else:
            hourly_filtered_df2 = weekday_filtered_df2[weekday_filtered_df2['Time']==hour]
            title=f'{aggregator} Quantity of Products Sold from {hour}'
        if not aggregator:
            aggregatted_df = hourly_filtered_df2.groupby('Items')[['Quantity','Ticket','Sales','AVS Per Hour']].mean().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Product Percentage'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df['ROTT'] = 100 - aggregatted_df['Product Percentage']
        elif aggregator == 'Average':
            aggregatted_df = hourly_filtered_df2.groupby('Items')[['Quantity','Ticket','Sales','AVS Per Hour']].mean().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Product Percentage'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df['ROTT'] = 100 - aggregatted_df['Product Percentage']
        elif aggregator == 'Minimum':
            aggregatted_df = hourly_filtered_df2.groupby('Items')[['Quantity','Ticket','Sales','AVS Per Hour']].min().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Product Percentage'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df['ROTT'] = 100 - aggregatted_df['Product Percentage']
        elif aggregator == 'Maximum':
            aggregatted_df = hourly_filtered_df2.groupby('Items')[['Quantity','Ticket','Sales','AVS Per Hour']].max().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Product Percentage'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df['ROTT'] = 100 - aggregatted_df['Product Percentage']
        else:
            aggregatted_df = hourly_filtered_df2.groupby('Items')[['Quantity','Ticket','Sales','AVS Per Hour']].sum().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Product Percentage'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df['ROTT'] = 100 - aggregatted_df['Product Percentage']
            
        options = [{'label':val,'value':val} for val in aggregatted_df['Items'].unique()]
        
        if not aggregatted_df.empty:
            value = aggregatted_df['Items'].unique()[0]
        else:
            value = None

        card1_h6 = f'{aggregator} Item Quantity'
        card1_h3 = f'{(aggregatted_df["Quantity"].sum()/aggregatted_df.shape[0]):,.2f}'
        card2_h6 = f'{aggregator} Ticket'
        card2_h3 = f'{(aggregatted_df["Ticket"].sum()/aggregatted_df.shape[0]):,.2f}'
        card3_h6 = f'{aggregator} Sales'
        card3_h3 = f'{(aggregatted_df["Sales"].sum()/aggregatted_df.shape[0]):,.2f}'
        card4_h6 = f'{aggregator} AVS Per Hour'
        card4_h3 = f'{(aggregatted_df["AVS Per Hour"].sum()/aggregatted_df.shape[0]):,.2f}'

        figure = px.bar(aggregatted_df, x='Items', y='Quantity', color_discrete_sequence=['#021d3a'])
        figure.update_layout(
                paper_bgcolor='#ece1dd',
                plot_bgcolor='#ece1dd'
        )    
        
        return options, value, card1_h6, card1_h3, card2_h6, card2_h3, card3_h6, card3_h3, card4_h6, card4_h3, figure, title
    except ValueError:
        return dash.no_update

#plot the doughnut chart in section 1
@app.callback(
    Output('percentage_item_by_hour','figure'),
    Output('item_percentage_by_hour','children'),
    Input('dataset_group', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('sidebar_month_selector', 'value'),
    Input('sidebar_week_selector', 'value'),
    Input('sidebar_weekday_selector','value'),
    Input('hour','value'),
    Input('data_aggregator','value'),
    Input('select_product', 'value')
)
def product_percent_update(group, start_date, end_date, month, week, weekday, hour, aggregator, product):
    try:   
        if not group:
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group =='cereal_packages':
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group == 'chicken_packages':
            grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
        elif group == 'call_to_order':
            grouped_df2 = df2[df2['Items'].isin(call_to_order)]
        else:
            grouped_df2 = df2[df2['Items'].isin(others)]

        date_filtered_df2 = grouped_df2[(grouped_df2['Date']>=start_date) & (grouped_df2['Date']<=end_date)]
        
        if not month:
            month_filtered_df2 = date_filtered_df2
        else:
            try:
                month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'] == month]
            except ValueError:
                month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'].isin(month)]
        
        if not week:
            week_filtered_df2 = month_filtered_df2
        else:
            try:
                week_filtered_df2 = month_filtered_df2[month_filtered_df2['Month Weeks'] == week]
            except ValueError:
                week_filtered_df2 = month_filtered_df2[month_filtered_df2['Month Weeks'].isin(week)]
        
        if not weekday:
            weekday_filtered_df2 = week_filtered_df2
        else:
            try:
                weekday_filtered_df2 = week_filtered_df2[week_filtered_df2['Week Days']==weekday]
            except ValueError:
                weekday_filtered_df2 = week_filtered_df2[week_filtered_df2['Week Days'].isin(weekday)]

        if not hour:
            hourly_filtered_df2 = weekday_filtered_df2[weekday_filtered_df2['Time']==weekday_filtered_df2['Time'].unique()[0]]
        else:
            hourly_filtered_df2 = weekday_filtered_df2[weekday_filtered_df2['Time']==hour]
        
        if not aggregator:
            aggregatted_df = hourly_filtered_df2.groupby('Items')[['Quantity','Ticket','Sales','AVS Per Hour']].mean().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Others'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df[f'{product}'] = 100 - aggregatted_df['Others']
        elif aggregator == 'Average':
            aggregatted_df = hourly_filtered_df2.groupby('Items')[['Quantity','Ticket','Sales','AVS Per Hour']].mean().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Others'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df[f'{product}'] = 100 - aggregatted_df['Others']
        elif aggregator == 'Minimum':
            aggregatted_df = hourly_filtered_df2.groupby('Items')[['Quantity','Ticket','Sales','AVS Per Hour']].min().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Others'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df[f'{product}'] = 100 - aggregatted_df['Others']
        elif aggregator == 'Maximum':
            aggregatted_df = hourly_filtered_df2.groupby('Items')[['Quantity','Ticket','Sales','AVS Per Hour']].max().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Others'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df[f'{product}'] = 100 - aggregatted_df['Others']
        else:
            aggregatted_df = hourly_filtered_df2.groupby('Items')[['Quantity','Ticket','Sales','AVS Per Hour']].sum().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Others'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df[f'{product}'] = 100 - aggregatted_df['Others']            

        if not product:
            df_ = aggregatted_df[aggregatted_df['Items'] == aggregatted_df['Items'].unique()[0]]
            title=f'Percentage of {aggregatted_df["Items"].unique()[0]} VS Other Products Sold from {hour}'
        else:
            df_= aggregatted_df[aggregatted_df['Items'] == product]
            title=f'Percentage of {product} VS Other Products Sold from {hour}'
        if not aggregatted_df.empty:
            df_ = pd.DataFrame({
            'Columns':[df_.columns[5],df_.columns[6]],
            'Value':[df_[f'{product}'].values[0],df_['Others'].values[0]]
            })
            figure = px.pie(df_, names='Columns', values='Value', hole=0.6,color_discrete_sequence=['rgba(29,55,70,0.7)','#021d3a'])
            figure.update_layout(
                paper_bgcolor='#ece1dd',
                plot_bgcolor='#ece1dd',
                legend=dict(orientation='h'),
                barmode='group'
            )    
        else:
            df_ = None
            figure = None

        return figure, title
    except ValueError:
        return dash.no_update
    except IndexError:
        return dash.no_update

#plot the bobble chart and the line chart and output options to plot the doughnut chart in section 2
@app.callback(
    Output('select_time','options'),
    Output('select_time', 'value'),
    Output('bobble_chart','figure'),
    Output('trend_plot','figure'),
    Output('bobble_chart_title','children'),
    Output('trend_plot_title','children'),
    Input('dataset_group', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('sidebar_month_selector', 'value'),
    Input('sidebar_week_selector', 'value'),
    Input('sidebar_weekday_selector','value'),
    Input('item','value'),
    Input('data_aggregator','value'),
    Input('feature_','value')
  )  
def product_update(group, start_date, end_date, month, week, weekday, item, aggregator,feature):
    if not group:
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
    elif group =='cereal_packages':
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
    elif group == 'chicken_packages':
        grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
    elif group == 'call_to_order':
        grouped_df2 = df2[df2['Items'].isin(call_to_order)]
    else:
        grouped_df2 = df2[df2['Items'].isin(others)]

    date_filtered_df2 = grouped_df2[(grouped_df2['Date']>=start_date) & (grouped_df2['Date']<=end_date)]
    
    if not month:
        month_filtered_df2 = date_filtered_df2
    else:
        try:
            month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'] == month]
        except ValueError:
            month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'].isin(month)]
    
    if not week:
        week_filtered_df2 = month_filtered_df2
    else:
        try:
            week_filtered_df2 = month_filtered_df2[month_filtered_df2['Month Weeks'] == week]
        except ValueError:
            week_filtered_df2 = month_filtered_df2[month_filtered_df2['Month Weeks'].isin(week)]
    
    if not weekday:
        weekday_filtered_df2 = week_filtered_df2
    else:
        try:
            weekday_filtered_df2 = week_filtered_df2[week_filtered_df2['Week Days']==weekday]
        except ValueError:
            weekday_filtered_df2 = week_filtered_df2[week_filtered_df2['Week Days'].isin(weekday)]

    if not item:
        item_filtered_df2 = weekday_filtered_df2[weekday_filtered_df2['Items']==weekday_filtered_df2['Items'].unique()[0]]
    else:
        item_filtered_df2 = weekday_filtered_df2[weekday_filtered_df2['Items']==item]
    
    if not aggregator:
        aggregatted_df = item_filtered_df2.groupby('Time')[['Quantity','Ticket','Sales','AVS Per Hour']].mean().reset_index()
        aggregatted_df = aggregatted_df.dropna()
        aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
        aggregatted_df['Hour Percentage'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
        aggregatted_df['ROTT'] = 100 - aggregatted_df['Hour Percentage']
    elif aggregator == 'Average':
        aggregatted_df = item_filtered_df2.groupby('Time')[['Quantity','Ticket','Sales','AVS Per Hour']].mean().reset_index()
        aggregatted_df = aggregatted_df.dropna()
        aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
        aggregatted_df['Hour Percentage'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
        aggregatted_df['ROTT'] = 100 - aggregatted_df['Hour Percentage']
    elif aggregator == 'Minimum':
        aggregatted_df = item_filtered_df2.groupby('Time')[['Quantity','Ticket','Sales','AVS Per Hour']].min().reset_index()
        aggregatted_df = aggregatted_df.dropna()
        aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
        aggregatted_df['Hour Percentage'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
        aggregatted_df['ROTT'] = 100 - aggregatted_df['Hour Percentage']
    elif aggregator == 'Maximum':
        aggregatted_df = item_filtered_df2.groupby('Time')[['Quantity','Ticket','Sales','AVS Per Hour']].max().reset_index()
        aggregatted_df = aggregatted_df.dropna()
        aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
        aggregatted_df['Hour Percentage'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
        aggregatted_df['ROTT'] = 100 - aggregatted_df['Hour Percentage']
    else:
        aggregatted_df = item_filtered_df2.groupby('Time')[['Quantity','Ticket','Sales','AVS Per Hour']].sum().reset_index()
        aggregatted_df = aggregatted_df.dropna()
        aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
        aggregatted_df['Hour Percentage'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
        aggregatted_df['ROTT'] = 100 - aggregatted_df['Hour Percentage']
        
    options = [{'label':val,'value':val} for val in aggregatted_df['Time'].unique()]
    
    if not aggregatted_df.empty:
        value = aggregatted_df['Time'].unique()[0]
    else:
    
        value = None

    figure1 = px.scatter(aggregatted_df, x='Quantity', y='Ticket', size='Sales',color_discrete_sequence=['#021d3a'])
    figure1.update_layout(
            paper_bgcolor='#ece1dd',
            plot_bgcolor='#ece1dd'
    )

    if not feature:
        figure2 = px.line(aggregatted_df, x ='Time', y='Quantity',color_discrete_sequence=['#021d3a'],markers=True)
        figure2.update_layout(
                paper_bgcolor='#ece1dd',
                plot_bgcolor='#ece1dd'
        )
    elif feature == 'Sales':
        figure2 = px.line(aggregatted_df, x ='Time', y='Sales',color_discrete_sequence=['#1d3746'],markers=True)
        figure2.update_layout(
                paper_bgcolor='#ece1dd',
                plot_bgcolor='#ece1dd'
        )
    elif feature == 'Ticket':
        figure2 = px.line(aggregatted_df, x ='Time', y='Ticket',color_discrete_sequence=['#1d3746'],markers=True)
        figure2.update_layout(
                paper_bgcolor='#ece1dd',
                plot_bgcolor='#ece1dd'
        )
    elif feature == 'Quantity':
        figure2 = px.line(aggregatted_df, x ='Time', y='Quantity',color_discrete_sequence=['#021d3a'],markers=True)
        figure2.update_layout(
                paper_bgcolor='#ece1dd',
                plot_bgcolor='#ece1dd'
        )
    else:
        figure2 = px.line(aggregatted_df, x ='Time', y='AVS Per Hour',color_discrete_sequence=['#021d3a'],markers=True)
        figure2.update_layout(
                paper_bgcolor='#ece1dd',
                plot_bgcolor='#ece1dd'
        )
    title1 = f'{aggregator} Quantity Sales of {item} Against {aggregator} Ticket'
    title2 = f'{item}: {aggregator} {feature} Trend'
    return options, value, figure1, figure2, title1, title2

#plot the doughnut cahrt in section 2
@app.callback(
    Output('hourly_quantity_percent','figure'),
    Output('hourly_item_quantity_percentage','children'),
    Input('dataset_group', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('sidebar_month_selector', 'value'),
    Input('sidebar_week_selector', 'value'),
    Input('sidebar_weekday_selector','value'),
    Input('item','value'),
    Input('data_aggregator','value'),
    Input('select_time', 'value')
  )  
def product_percent_update(group, start_date, end_date, month, week, weekday, item, aggregator, hour):
    try:    
        if not group:
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group =='cereal_packages':
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group == 'chicken_packages':
            grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
        elif group == 'call_to_order':
            grouped_df2 = df2[df2['Items'].isin(call_to_order)]
        else:
            grouped_df2 = df2[df2['Items'].isin(others)]

        date_filtered_df2 = grouped_df2[(grouped_df2['Date']>=start_date) & (grouped_df2['Date']<=end_date)]
        
        if not month:
            month_filtered_df2 = date_filtered_df2
        else:
            try:
                month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'] == month]
            except ValueError:
                month_filtered_df2 = date_filtered_df2[date_filtered_df2['Month'].isin(month)]
        
        if not week:
            week_filtered_df2 = month_filtered_df2
        else:
            try:
                week_filtered_df2 = month_filtered_df2[month_filtered_df2['Month Weeks'] == week]
            except ValueError:
                week_filtered_df2 = month_filtered_df2[month_filtered_df2['Month Weeks'].isin(week)]
        
        if not weekday:
            weekday_filtered_df2 = week_filtered_df2
        else:
            try:
                weekday_filtered_df2 = week_filtered_df2[week_filtered_df2['Week Days']==weekday]
            except ValueError:
                weekday_filtered_df2 = week_filtered_df2[week_filtered_df2['Week Days'].isin(weekday)]

        if not item:
            item_filtered_df2 = weekday_filtered_df2[weekday_filtered_df2['Items']==weekday_filtered_df2['Items'].unique()[0]]
        else:
            item_filtered_df2 = weekday_filtered_df2[weekday_filtered_df2['Items']==item]
        
        if not aggregator:
            aggregatted_df = item_filtered_df2.groupby('Time')[['Quantity','Ticket','Sales','AVS Per Hour']].mean().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Others'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df[f'{hour}'] = 100 - aggregatted_df['Others']
        elif aggregator == 'Average':
            aggregatted_df = item_filtered_df2.groupby('Time')[['Quantity','Ticket','Sales','AVS Per Hour']].mean().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Others'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df[f'{hour}'] = 100 - aggregatted_df['Others']
        elif aggregator == 'Minimum':
            aggregatted_df = item_filtered_df2.groupby('Time')[['Quantity','Ticket','Sales','AVS Per Hour']].min().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Others'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df[f'{hour}'] = 100 - aggregatted_df['Others']
        elif aggregator == 'Maximum':
            aggregatted_df = item_filtered_df2.groupby('Time')[['Quantity','Ticket','Sales','AVS Per Hour']].max().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Others'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df[f'{hour}'] = 100 - aggregatted_df['Others']
        else:
            aggregatted_df = item_filtered_df2.groupby('Time')[['Quantity','Ticket','Sales','AVS Per Hour']].sum().reset_index()
            aggregatted_df = aggregatted_df.dropna()
            aggregatted_df = aggregatted_df[~(aggregatted_df==0).any(axis=1)]
            aggregatted_df['Others'] = (aggregatted_df['Quantity']/aggregatted_df['Quantity'].sum())*100
            aggregatted_df[f'{hour}'] = 100 - aggregatted_df['Others']

        if not hour:
            df_ = aggregatted_df[aggregatted_df['Time'] == aggregatted_df['Time'].unique()[0]]
        else:
            df_= aggregatted_df[aggregatted_df['Time'] == hour]

        if not aggregatted_df.empty:
            df_ = pd.DataFrame({
            'Columns':[df_.columns[5],df_.columns[6]],
            'Value':[df_[f'{hour}'].values[0],df_['Others'].values[0]]
            })
            figure = px.pie(df_, names='Columns', values='Value', hole=0.6,color_discrete_sequence=['rgba(29,55,70,0.7)','#021d3a'])
            figure.update_layout(
                paper_bgcolor='#ece1dd',
                plot_bgcolor='#ece1dd',
                legend=dict(orientation='h'),
                barmode='group'
            )
        else:
            df_ = None
            figure = None
        title = f'Percentage {aggregator} Quantity of {item} From {hour}'
        return figure,title
    except ValueError:
        return dash.no_update
    except IndexError:
        return dash.no_update

# the next six callbacks will follow the same approach as in the last callabcks
# only that two dropdowns are targeted at a time  
@app.callback(
    Output('comp_date-picker1', 'start_date'),
    Output('comp_date-picker1','end_date'),
    Output('comp_date-picker2', 'start_date'),
    Output('comp_date-picker2','end_date'),
    Input('dataset_group','value')
)
def comp_dataset_filter(group):
    if not group:
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
    elif group =='cereal_packages':
        grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
    elif group == 'chicken_packages':
        grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
    elif group == 'call_to_order':
        grouped_df2 = df2[df2['Items'].isin(call_to_order)]
    else:
        grouped_df2 = df2[df2['Items'].isin(others)]

    start_date1 = grouped_df2['Date'].min()
    end_date1 = grouped_df2['Date'].max()
    start_date2 = grouped_df2['Date'].min()
    end_date2 = grouped_df2['Date'].max()

    return start_date1, end_date1, start_date2, end_date2

@app.callback(
    Output('comp_month_selector1', 'options'),
    Output('comp_month_selector1', 'value' ),
    Output('comp_month_selector2', 'options'),
    Output('comp_month_selector2', 'value' ),
    Input('dataset_group','value'),
    Input('comp_date-picker1','start_date'),
    Input('comp_date-picker1','end_date'),
    Input('comp_date-picker2','start_date'),
    Input('comp_date-picker2','end_date'),
)
def comp_date_filter(group,start_date1,end_date1,start_date2,end_date2):
    try:    
        if not group:
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group =='cereal_packages':
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group == 'chicken_packages':
            grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
        elif group == 'call_to_order':
            grouped_df2 = df2[df2['Items'].isin(call_to_order)]
        else:
            grouped_df2 = df2[df2['Items'].isin(others)]

        date_filtered1 = grouped_df2[(grouped_df2['Date']>=start_date1) & (grouped_df2['Date']<=end_date1)]
        date_filtered2 = grouped_df2[(grouped_df2['Date']>=start_date2) & (grouped_df2['Date']<=end_date2)]
        
        options1 = [{'label':val,'value':val} for val in date_filtered1['Month'].unique()]
        value1 = date_filtered1['Month'].unique()[0]
        options2 = [{'label':val,'value':val} for val in date_filtered2['Month'].unique()]
        value2 = date_filtered2['Month'].unique()[0]

        return options1, value1, options2, value2
    except IndexError:
        return dash.no_update

@app.callback(
    Output('comp_week_selector1', 'options'),
    Output('comp_week_selector1', 'value' ),
    Output('comp_week_selector2', 'options'),
    Output('comp_week_selector2', 'value' ),
    Input('dataset_group','value'),
    Input('comp_date-picker1','start_date'),
    Input('comp_date-picker1','end_date'),
    Input('comp_date-picker2','start_date'),
    Input('comp_date-picker2','end_date'),
    Input('comp_month_selector1','value'),
    Input('comp_month_selector2','value'),
)
def comp_month_filter(group,start_date1,end_date1,start_date2,end_date2,month1,month2):
    try:
        if not group:
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group =='cereal_packages':
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group == 'chicken_packages':
            grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
        elif group == 'call_to_order':
            grouped_df2 = df2[df2['Items'].isin(call_to_order)]
        else:
            grouped_df2 = df2[df2['Items'].isin(others)]

        date_filtered1 = grouped_df2[(grouped_df2['Date']>=start_date1) & (grouped_df2['Date']<=end_date1)]
        date_filtered2 = grouped_df2[(grouped_df2['Date']>=start_date2) & (grouped_df2['Date']<=end_date2)]
        
        if not month1:
            month_filtered1 = date_filtered1
        else:
            try:
                month_filtered1 = date_filtered1[date_filtered1['Month'] == month1]
            except ValueError:
                month_filtered1 = date_filtered1[date_filtered1['Month'].isin(month1)]
        
        if not month2:
            month_filtered2 = date_filtered2
        else:
            try:
                month_filtered2 = date_filtered2[date_filtered2['Month'] == month2]
            except ValueError:
                month_filtered2 = date_filtered2[date_filtered2['Month'].isin(month2)]

        options1 = [{'label':val,'value':val} for val in month_filtered1['Month Weeks'].unique()]
        value1 = month_filtered1['Month Weeks'].unique()[0]
        options2 = [{'label':val,'value':val} for val in month_filtered2['Month Weeks'].unique()]
        value2 = month_filtered2['Month Weeks'].unique()[0]

        return options1, value1, options2, value2
    except IndexError:
        return dash.no_update

@app.callback(
    Output('comp_weekday_selector1', 'options'),
    Output('comp_weekday_selector1', 'value' ),
    Output('comp_weekday_selector2', 'options'),
    Output('comp_weekday_selector2', 'value' ),
    Input('dataset_group','value'),
    Input('comp_date-picker1','start_date'),
    Input('comp_date-picker1','end_date'),
    Input('comp_date-picker2','start_date'),
    Input('comp_date-picker2','end_date'),
    Input('comp_month_selector1','value'),
    Input('comp_month_selector2','value'),
    Input('comp_week_selector1','value'),
    Input('comp_week_selector2','value')
)
def comp_week_filter(group,start_date1,end_date1,start_date2,end_date2,month1,month2,week1,week2):
    try:   
        if not group:
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group =='cereal_packages':
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group == 'chicken_packages':
            grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
        elif group == 'call_to_order':
            grouped_df2 = df2[df2['Items'].isin(call_to_order)]
        else:
            grouped_df2 = df2[df2['Items'].isin(others)]

        date_filtered1 = grouped_df2[(grouped_df2['Date']>=start_date1) & (grouped_df2['Date']<=end_date1)]
        date_filtered2 = grouped_df2[(grouped_df2['Date']>=start_date2) & (grouped_df2['Date']<=end_date2)]
        
        if not month1:
            month_filtered1 = date_filtered1
        else:
            try:
                month_filtered1 = date_filtered1[date_filtered1['Month'] == month1]
            except ValueError:
                month_filtered1 = date_filtered1[date_filtered1['Month'].isin(month1)]
        
        if not month2:
            month_filtered2 = date_filtered2
        else:
            try:
                month_filtered2 = date_filtered2[date_filtered2['Month'] == month2]
            except ValueError:
                month_filtered2 = date_filtered2[date_filtered2['Month'].isin(month2)]

        if not week1:
            week_filtered1 = month_filtered1
        else:
            try:
                week_filtered1 = month_filtered1[month_filtered1['Month Weeks'] == week1]
            except ValueError:
                week_filtered1 = month_filtered1[month_filtered1['Month Weeks'].isin(week1)]

        if not week2:
            week_filtered2 = month_filtered2
        else:
            try:
                week_filtered2 = month_filtered2[month_filtered2['Month Weeks'] == week2]
            except ValueError:
                week_filtered2 = month_filtered2[month_filtered2['Month Weeks'].isin(week2)]
        
        options1 = [{'label':val,'value':val} for val in week_filtered1['Week Days'].unique()]
        value1 = week_filtered1['Week Days'].unique()[0]
        options2 = [{'label':val,'value':val} for val in week_filtered2['Week Days'].unique()]
        value2 = week_filtered2['Week Days'].unique()[0]
        
        return options1, value1, options2, value2
    except IndexError:
        return dash.no_update

@app.callback(
    Output('comp_product_selector1', 'options'),
    Output('comp_product_selector1', 'value' ),
    Output('comp_product_selector2', 'options'),
    Output('comp_product_selector2', 'value' ),
    Input('dataset_group','value'),
    Input('comp_date-picker1','start_date'),
    Input('comp_date-picker1','end_date'),
    Input('comp_date-picker2','start_date'),
    Input('comp_date-picker2','end_date'),
    Input('comp_month_selector1','value'),
    Input('comp_month_selector2','value'),
    Input('comp_week_selector1','value'),
    Input('comp_week_selector2','value'),
    Input('comp_weekday_selector1','value'),
    Input('comp_weekday_selector2','value'),
)
def comp_day_filter(group,start_date1,end_date1,start_date2,end_date2,month1,month2,week1,week2,day1,day2):
    try:
        if not group:
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group =='cereal_packages':
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group == 'chicken_packages':
            grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
        elif group == 'call_to_order':
            grouped_df2 = df2[df2['Items'].isin(call_to_order)]
        else:
            grouped_df2 = df2[df2['Items'].isin(others)]

        date_filtered1 = grouped_df2[(grouped_df2['Date']>=start_date1) & (grouped_df2['Date']<=end_date1)]
        date_filtered2 = grouped_df2[(grouped_df2['Date']>=start_date2) & (grouped_df2['Date']<=end_date2)]
        
        if not month1:
            month_filtered1 = date_filtered1
        else:
            try:
                month_filtered1 = date_filtered1[date_filtered1['Month'] == month1]
            except ValueError:
                month_filtered1 = date_filtered1[date_filtered1['Month'].isin(month1)]
        
        if not month2:
            month_filtered2 = date_filtered2
        else:
            try:
                month_filtered2 = date_filtered2[date_filtered2['Month'] == month2]
            except ValueError:
                month_filtered2 = date_filtered2[date_filtered2['Month'].isin(month2)]

        if not week1:
            week_filtered1 = month_filtered1
        else:
            try:
                week_filtered1 = month_filtered1[month_filtered1['Month Weeks'] == week1]
            except ValueError:
                week_filtered1 = month_filtered1[month_filtered1['Month Weeks'].isin(week1)]

        if not week2:
            week_filtered2 = month_filtered2
        else:
            try:
                week_filtered2 = month_filtered2[month_filtered2['Month Weeks'] == week2]
            except ValueError:
                week_filtered2 = month_filtered2[month_filtered2['Month Weeks'].isin(week2)]
        
        if not day1:
            weekday_filtered1 = week_filtered1
        else:
            try:
                weekday_filtered1 = week_filtered1[week_filtered1['Week Days']==day1]
            except ValueError:
                weekday_filtered1 = week_filtered1[week_filtered1['Week Days'].isin(day1)]    

        if not day2:
            weekday_filtered2 = week_filtered2
        else:
            try:
                weekday_filtered2 = week_filtered2[week_filtered2['Week Days']==day2]
            except ValueError:
                weekday_filtered2 = week_filtered2[week_filtered1['Week Days'].isin(day2)]    

        options1 = [{'label':val,'value':val} for val in weekday_filtered1['Items'].unique()]
        value1 = weekday_filtered1['Items'].unique()[0]
        options2 = [{'label':val,'value':val} for val in weekday_filtered2['Items'].unique()]
        value2 = weekday_filtered2['Items'].unique()[2]
        
        return options1, value1, options2, value2
    except IndexError:
        return dash.no_update

@app.callback(
    Output('comp_plot', 'figure' ),
    Output('comp_plot_title','children'),
    Input('dataset_group','value'),
    Input('comp_date-picker1','start_date'),
    Input('comp_date-picker1','end_date'),
    Input('comp_date-picker2','start_date'),
    Input('comp_date-picker2','end_date'),
    Input('comp_month_selector1','value'),
    Input('comp_month_selector2','value'),
    Input('comp_week_selector1','value'),
    Input('comp_week_selector2','value'),
    Input('comp_weekday_selector1','value'),
    Input('comp_weekday_selector2','value'),
    Input('comp_product_selector1','value'),
    Input('comp_product_selector2','value'),
    Input('data_aggregator','value'),
)
def comp_plotter(group,start_date1,end_date1,start_date2,end_date2,month1,month2,week1,week2,day1,day2,product1,product2,aggregator):
    try:    
        if not group:
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group =='cereal_packages':
            grouped_df2 = df2[df2['Items'].isin(cereal_packages)]
        elif group == 'chicken_packages':
            grouped_df2 = df2[df2['Items'].isin(chicken_packages)]
        elif group == 'call_to_order':
            grouped_df2 = df2[df2['Items'].isin(call_to_order)]
        else:
            grouped_df2 = df2[df2['Items'].isin(others)]

        date_filtered1 = grouped_df2[(grouped_df2['Date']>=start_date1) & (grouped_df2['Date']<=end_date1)]
        date_filtered2 = grouped_df2[(grouped_df2['Date']>=start_date2) & (grouped_df2['Date']<=end_date2)]
        
        if not month1:
            month_filtered1 = date_filtered1
        else:
            try:
                month_filtered1 = date_filtered1[date_filtered1['Month'] == month1]
            except ValueError:
                month_filtered1 = date_filtered1[date_filtered1['Month'].isin(month1)]
        
        if not month2:
            month_filtered2 = date_filtered2
        else:
            try:
                month_filtered2 = date_filtered2[date_filtered2['Month'] == month2]
            except ValueError:
                month_filtered2 = date_filtered2[date_filtered2['Month'].isin(month2)]

        if not week1:
            week_filtered1 = month_filtered1
        else:
            try:
                week_filtered1 = month_filtered1[month_filtered1['Month Weeks'] == week1]
            except ValueError:
                week_filtered1 = month_filtered1[month_filtered1['Month Weeks'].isin(week1)]

        if not week2:
            week_filtered2 = month_filtered2
        else:
            try:
                week_filtered2 = month_filtered2[month_filtered2['Month Weeks'] == week2]
            except ValueError:
                week_filtered2 = month_filtered2[month_filtered2['Month Weeks'].isin(week2)]
        
        if not day1:
            weekday_filtered1 = week_filtered1
        else:
            try:
                weekday_filtered1 = week_filtered1[week_filtered1['Week Days']==day1]
            except ValueError:
                weekday_filtered1 = week_filtered1[week_filtered1['Week Days'].isin(day1)]    

        if not day2:
            weekday_filtered2 = week_filtered2
        else:
            try:
                weekday_filtered2 = week_filtered2[week_filtered2['Week Days']==day2]
            except ValueError:
                weekday_filtered2 = week_filtered2[week_filtered1['Week Days'].isin(day2)]    

        if not product1:
            product_filtered1 = weekday_filtered1[weekday_filtered1['Items']==weekday_filtered1['Items'].unique()[0]]
        else:
            product_filtered1 = weekday_filtered1[weekday_filtered1['Items']==product1]

        if not product2:
            product_filtered2 = weekday_filtered2[weekday_filtered2['Items']==weekday_filtered2['Items'].unique()[0]]
        else:
            product_filtered2 = weekday_filtered2[weekday_filtered2['Items']==product2]
        
        if not aggregator:
            aggregatted_df1 = product_filtered1.groupby('Time')[['Quantity']].mean().reset_index()
            # aggregatted_df1 = aggregatted_df1.dropna()
            # aggregatted_df1 = aggregatted_df1[~(aggregatted_df1==0).any(axis=1)]
            aggregatted_df2 = product_filtered2.groupby('Time')[['Quantity']].mean().reset_index()
            # aggregatted_df2 = aggregatted_df2.dropna()
            # aggregatted_df2 = aggregatted_df2[~(aggregatted_df2==0).any(axis=1)]

        elif aggregator == 'Average':
            aggregatted_df1 = product_filtered1.groupby('Time')[['Quantity']].mean().reset_index()
            # aggregatted_df1 = aggregatted_df1.dropna()
            # aggregatted_df1 = aggregatted_df1[~(aggregatted_df1==0).any(axis=1)]
            aggregatted_df2 = product_filtered2.groupby('Time')[['Quantity']].mean().reset_index()
            # aggregatted_df2 = aggregatted_df2.dropna()
            # aggregatted_df2 = aggregatted_df2[~(aggregatted_df2==0).any(axis=1)]
        elif aggregator == 'Minimum':
            aggregatted_df1 = product_filtered1.groupby('Time')[['Quantity']].min().reset_index()
            # aggregatted_df1 = aggregatted_df1.dropna()
            # aggregatted_df1 = aggregatted_df1[~(aggregatted_df1==0).any(axis=1)]
            aggregatted_df2 = product_filtered2.groupby('Time')[['Quantity']].min().reset_index()
            # aggregatted_df2 = aggregatted_df2.dropna()
            # aggregatted_df2 = aggregatted_df2[~(aggregatted_df2==0).any(axis=1)]
        elif aggregator == 'Maximum':
            aggregatted_df1 = product_filtered1.groupby('Time')[['Quantity']].max().reset_index()
            # aggregatted_df1 = aggregatted_df1.dropna()
            # aggregatted_df1 = aggregatted_df1[~(aggregatted_df1==0).any(axis=1)]
            aggregatted_df2 = product_filtered2.groupby('Time')[['Quantity']].max().reset_index()
            # aggregatted_df2 = aggregatted_df2.dropna()
            # aggregatted_df2 = aggregatted_df2[~(aggregatted_df2==0).any(axis=1)]
        else:
            aggregatted_df1 = product_filtered1.groupby('Time')[['Quantity']].sum().reset_index()
            # aggregatted_df1 = aggregatted_df1.dropna()
            # aggregatted_df1 = aggregatted_df1[~(aggregatted_df1==0).any(axis=1)]
            aggregatted_df2 = product_filtered2.groupby('Time')[['Quantity']].sum().reset_index()
            # aggregatted_df2 = aggregatted_df2.dropna()
            # aggregatted_df2 = aggregatted_df2[~(aggregatted_df2==0).any(axis=1)]

        df_ = pd.merge(aggregatted_df1,aggregatted_df2, on='Time', suffixes=(f' Of {product1} (Left Filter)', f' Of {product2} (Right Filter)'), how='outer').fillna(0)

        
        figure = px.bar(df_, x='Time', y=[f'Quantity Of {product1} (Left Filter)', f'Quantity Of {product2} (Right Filter)'],
                color_discrete_map={f'Quantity Of {product1} (Left Filter)' : 'rgba(29,55,70,0.7)',  f'Quantity Of {product2} (Right Filter)': '#021d3a'},
                barmode='group')
        figure.update_layout(
            paper_bgcolor='#ece1dd',
            legend_title='',
            plot_bgcolor='#ece1dd',
            legend=dict(orientation='h',yanchor='bottom',y=1.02,xanchor='right',x=1),
            barmode='group'
        )
        title = f'Comparing {product1} And {product2}'   
        return figure, title
    except ValueError:
        return dash.no_update
#plot the correlation chart   
@app.callback(
    Output('scatter_plot','figure'),
    Output('scatter_plot_title','children'),
    Input('feature1','value'),
    Input('feature2','value'),
)    
def scatter_plot(feature1, feature2):
    if not ((feature1) or (feature2)):
        figure = px.scatter(df_, x = 'Ticket', y = 'AVS Per Hour')
        figure.update_layout(
            paper_bgcolor='#ece1dd',
            plot_bgcolor='#ece1dd'
        )
    else:
        figure = px.scatter(df_, x=feature1, y=feature2,color_discrete_sequence=['rgba(29,55,70,0.7)','#021d3a'])
        figure.update_layout(
            paper_bgcolor='#ece1dd',
            plot_bgcolor='#ece1dd'
        )
        figure.update_traces(
            marker=dict(size=10)
        )
    title = f'Correlation Between {feature1} And {feature2}'
    return figure, title

#run the app
if __name__ == '__main__':
    app.run_server(debug=True)