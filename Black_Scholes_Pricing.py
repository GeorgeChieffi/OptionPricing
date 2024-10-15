import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
st.set_page_config(layout='wide', page_title="Black Scholes Pricing")

class BS_Option:
    def __init__(self, spot: float, strike: float, ttm: float, vol: float, rfr: float):
        self.spotPrice = spot
        self.strikePrice = strike
        self.timeToMaturity = ttm
        self.sigma = vol
        self.riskFreeRate = rfr

        self.d1 = (np.log(self.spotPrice / self.strikePrice) + (self.riskFreeRate + self.sigma**2/2)*self.timeToMaturity) / (self.sigma * np.sqrt(self.timeToMaturity))
        self.d2 = self.d1 - self.sigma * np.sqrt(self.timeToMaturity)
        return None

    def getCallPrice(self):
        N = norm.cdf
        callPrice = self.spotPrice * N(self.d1) - self.strikePrice * np.exp(-self.riskFreeRate * self.timeToMaturity) * N(self.d2)
        return round(callPrice, 2)
    
    def getPutPrice(self):
        N = norm.cdf
        putPrice = self.strikePrice * np.exp(-self.riskFreeRate * self.timeToMaturity) * N(-self.d2) - self.spotPrice * N(-self.d1)
        return round(putPrice, 2)


def main():
    st.title("Welcome to Black Scholes Option Pricing")

    
    
    with st.sidebar:
        currentPrice = st.number_input("Current Price (spot price)", min_value=0.0, value=100.0, step=1.0)
        strikePrice = st.number_input("Strike Price", min_value=0.0, value=100.0, step=1.0)
        timeToMaturity = st.number_input("Time to Maturity (years)", min_value=0.0, value=1.0)
        sigma = st.number_input("Volatility (sigma)", min_value=0.0, value=0.2)
        riskFreeRate = st.number_input("Annualized Risk Free Rate", min_value=0.0, value=.01)

    option = BS_Option(currentPrice, strikePrice, timeToMaturity, sigma, riskFreeRate)


    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(label="Current Price", value=currentPrice)
    col2.metric(label="Strike Price", value=strikePrice)
    col3.metric(label="Volatility", value=round(sigma, 2))
    col4.metric(label="Time To Maturity", value=round(timeToMaturity, 2))
    col5.metric(label="Risk Free Rate", value=round(riskFreeRate, 2))

    st.divider()

    right, left = st.columns(2)
    with right:
        c1, c2 = st.columns(2)
        c1.header("Call Price:")
        c2.header(option.getCallPrice())
    with left:
        c1, c2 = st.columns(2)
        c1.header("Put Price:")
        c2.header(option.getPutPrice())

main()