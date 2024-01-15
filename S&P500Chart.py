#Hello World! 
#print("Hello World!") 
import yfinance as yf
import plotly.graph_objs as go

# Download data on S&P 500
sp500 = yf.download('^GSPC', start='2023-06-05', end='2023-06-11')

# Create a trace for the closing price of S&P 500
trace = go.Scatter(x=sp500.index, y=sp500['Close'], mode='lines', name='S&P 500 Closing Price')

# Create a layout for the chart
layout = go.Layout(title='S&P 500 Closing Price', xaxis=dict(title='Date'), yaxis=dict(title='Price'))

# Create a figure for the chart
fig = go.Figure(data=[trace], layout=layout)

# Show the chart
fig.show()

