# Run this app with `python app.py` and
# visit http://127.0.0.1:8051/ in your web browser.

from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
import yfinance as yf
import numpy as np

# Lets choose the ticker and the desired expiration dates
tk0 = "MSFT"
tk = yf.Ticker(tk0)
dates = tk.options


# Possible inputs
F1 = "2022-07-15"
F2 = "2023-03-17"
dates # If you want to check the available ones
A = 270 # Short call strike
B = 280 # Long call strike


# Lets get all the data we need
optsc = tk.option_chain(F1)
optlc = tk.option_chain(F2)

# This will be the feed of the "info" square

# Define in which row is the info we need
ISC = optsc.calls.loc[optsc.calls['strike']==(A)].index[0] # For the short call
ILC = optlc.calls.loc[optlc.calls["strike"]==(B)].index[0] # For the Long call

# Profit between the options
p = optsc.calls.iloc[(ISC),3] / optlc.calls.iloc[(ILC),3]
p = p * 100
p = p.round(decimals = 2)

# Premium
pr = optsc.calls.iloc[(ISC),3]
pr = pr * 100

# Strike wide
sw =  - optsc.calls.iloc[(ISC),2] + optlc.calls.iloc[(ILC),2]

# Needed capital to open the position
c = optlc.calls.iloc[(ILC),3]
c = c * 100
c = c.round(decimals = 0)

# Now we create the dataframe for the plot, joining price and profit for the -5//+5 prices for the Short call

# Get the premiums in the y axis and the price in the x axis
yaxis = []
for ix in range(-5, 6):
    yaxis.append(optsc.calls.iloc[(ISC + ix), 3])

xaxis = []
for iy in range(-5, 6):
    xaxis.append(optsc.calls.iloc[(ISC + iy), 2])

# Create the pandas dataframe premium / price
plotdf = pd.DataFrame(list(zip(yaxis, xaxis)), columns=["premium", "price"])

# Lets create the title as a variable
Title = "Poor Man´s Covered call"
Stitle =(["A poor man’s covered call is a long call diagonal debit spread that is used to replicate a covered call "
          "position. The strategy gets its name from the reduced risk and capital requirement relative to a standard "
          "covered call. "])



data = plotdf

#Define the componentes for the dashboard
df = plotdf


fig = (px.line(df, x="price", y="premium", markers=True))
fig2 = (px.line(df, x="price", y="premium", markers=True))


app = Dash(__name__)

# see https://plotly.com/python/px-arguments/ for more options


app.layout = html.Div(children=[
    html.H1(children= Title ),

    html.Div(children= Stitle),


html.H2(children= "Short Call"),
    html.Div(children=[
            html.Label('Expiration'),
            dcc.Dropdown(tk.options, 'Date')]),

    html.Div(children=[
            html.Label('Price'),
            dcc.Dropdown(tk.options, 'Date')]),


html.H2(children= "Long Call"),
    html.Div(children=[
            html.Label('Expiration'),
            dcc.Dropdown(tk.options, 'Date')]),

    html.Div(children=[
            html.Label('Price'),
            dcc.Dropdown(tk.options, 'Date')]),


html.H3(children= "Premium VS Price"),
    html.Div(children=[
            html.Label(''),
        dcc.Graph(
            id='example-graph', figure=fig)]),


html.H3(children= "Strategy Resume"),
    dash_table.DataTable(data=df.to_dict('records')),

])

if __name__ == '__main__':
    app.run_server(debug=True, port = 8051)

