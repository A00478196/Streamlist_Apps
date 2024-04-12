import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time

def get_price_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": 365
    }
    response = requests.get(url, params=params)
    time.sleep(1)  # Add a delay of 1 second
    data = response.json()
    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

# Function to find max and min prices along with the corresponding dates
def find_max_min(prices_df):
    max_price = prices_df["price"].max()
    min_price = prices_df["price"].min()
    max_date = prices_df.loc[prices_df["price"].idxmax()]["timestamp"].date()
    min_date = prices_df.loc[prices_df["price"].idxmin()]["timestamp"].date()
    return max_price, max_date, min_price, min_date 


@st.cache_data
def fetch_coins_list():
    coins_list_url = "https://api.coingecko.com/api/v3/coins/list"
    coins_list_response = requests.get(coins_list_url)
    time.sleep(1)  # Add a delay of 1 second
    return coins_list_response.json()

def main():
    st.title("Cryptocurrency Price Analysis")
    
    # Fetching list of available cryptocurrencies
    coins_list = fetch_coins_list()
    
     # Check if coins_list is not a list of dictionaries
    if not isinstance(coins_list, list) or not all(isinstance(coin, dict) for coin in coins_list):
        st.error("Error: You've exceeded the Rate Limit. Please visit https://www.coingecko.com/en/api/pricing to subscribe to our API plans for higher rate limits. ")
        return
    
    # Create a dictionary mapping cryptocurrency names to their ids
    coins_dict = {coin["name"].lower(): coin["id"] for coin in coins_list}

    # print(coins_dict)
    # User input for cryptocurrency name
    coin_name = st.sidebar.selectbox("Select a cryptocurrency", [""] + list(coins_dict.keys()))
        
    if coin_name:
        coin_id = coins_dict[coin_name.lower()]
        
        # Fetching and plotting price data
        try:
            prices_df = get_price_data(coin_id)
            st.subheader(f"Price Chart for {coin_name}")
            st.line_chart(prices_df.set_index("timestamp"))
            
            # Finding max and min prices along with corresponding dates
            max_price, max_date, min_price, min_date = find_max_min(prices_df)
            st.write(f"Maximum Price: ${max_price} on {max_date}")
            st.write(f"Minimum Price: ${min_price} on {min_date}")
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")
    else:
        st.warning("Please select a cryptocurrency.")

if __name__ == "__main__":
    main()
