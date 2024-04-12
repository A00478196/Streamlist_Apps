import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time


# Function to fetch list of available cryptocurrencies and cache the result
@st.cache_data
def fetch_coins_list():
    coins_list_url = "https://api.coingecko.com/api/v3/coins/list"
    coins_list_response = requests.get(coins_list_url)
    # print(coins_list_response)
    # print(coins_list_response)
    time.sleep(1)  # Add a delay of 1 second

    return coins_list_response.json()

@st.cache_data
# Function to fetch historical price data for a cryptocurrency
def get_price_data(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days
    }
    
    response = requests.get(url, params=params)
    time.sleep(1)  # Add a delay of 1 second
    # print(response)
    data = response.json()
    prices = data.get("prices", [])
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

# Function to plot price data for two cryptocurrencies
def plot_price_comparison(coin1_df, coin2_df, coin1_name, coin2_name):
    plt.figure(figsize=(10, 6))
    plt.plot(coin1_df["timestamp"], coin1_df["price"], label=coin1_name)
    plt.plot(coin2_df["timestamp"], coin2_df["price"], label=coin2_name)
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.title("Price Comparison")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

# Function to handle fetching price data and plotting when the time frame changes
def handle_time_frame_change(coin1_id, coin2_id, time_frame, coin1_name, coin2_name):
    time_frames = {"1 Week": 7, "1 Month": 30, "1 Year": 365, "5 Years": 1825}
    days = time_frames.get(time_frame)
    
    if days is None:
        st.error("Invalid time frame selected.")
        return
    
    coin1_df = get_price_data(coin1_id, days)
    coin2_df = get_price_data(coin2_id, days)
    
    # print(coin1_df)
    # print(coin2_df)
    
    if coin1_df.empty or coin2_df.empty:
        st.error("Sorry, no data available.")
        return
    
    plot_price_comparison(coin1_df, coin2_df, coin1_name, coin2_name)

# Main function to run the Streamlit app
def main():
    st.title("Cryptocurrency Price Comparison")
    
    # Fetching list of available cryptocurrencies
    coins_list = fetch_coins_list()
    
     # Check if coins_list is not a list of dictionaries
    if not isinstance(coins_list, list) or not all(isinstance(coin, dict) for coin in coins_list):
        st.error("Error: You've exceeded the Rate Limit. Please visit https://www.coingecko.com/en/api/pricing to subscribe to our API plans for higher rate limits. ")
        return
   
    # print(co)
    # Create a dictionary mapping cryptocurrency names to their ids
    coins_dict = {coin["name"].lower(): coin["id"] for coin in coins_list}

    # User input for first cryptocurrency
    coin1_name = st.sidebar.selectbox("Select first cryptocurrency", [""] + list(coins_dict.keys()))
    
    # User input for second cryptocurrency
    coin2_name = st.sidebar.selectbox("Select second cryptocurrency", [""] + list(coins_dict.keys()))
    
    # User input for time frame
    time_frame = st.sidebar.selectbox("Select time frame", ["1 Week", "1 Month", "1 Year", "5 Years"])

    # Handle time frame change
    if coin1_name and coin2_name:
        coin1_id = coins_dict[coin1_name]
        coin2_id = coins_dict[coin2_name]
        handle_time_frame_change(coin1_id, coin2_id, time_frame, coin1_name, coin2_name)
    else:
        st.warning("Please select two cryptocurrencies.")

# Run the app
if __name__ == "__main__":
    main()
