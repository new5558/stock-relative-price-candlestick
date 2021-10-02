# stock-relative-price-candlestick

![image](https://user-images.githubusercontent.com/12471844/135728081-dc3a7327-ed81-44bf-bc1a-7047846e0408.png)

## Demo

[Heroku web application](https://candle-stick-streamlit.herokuapp.com/) (Will change to Streamlit cloud after being invited)

## Ideas

- Inspired by Crypto symbols that is not traded with stable coin etc `BNBBTC`, `ETHBTC`
- Use investpy-api to get OHLC data of SET index and stocks in Thailand
- Create as an interactable webapp using Streamlit
- Add some customizations!

## Potential usage

- Create beta neutral price action strategy from candlestick graph. This can be done using SET50 index future to hedge your stock position.
- Create statistical abritage strategy from price action. For example, we can buy stocks that is tempory underperform SET index and short sell temprty overperform SET index stocks
- Imply inividual stock's rolling relative strength with market by looking at historial candlestick.
- and many more..

## Run app locally
### Using docker
Run the following command

`docker build -t streamlitapp:latest .`  

`docker run streamlitapp`  

### Using python

Run the following command

`pip install -r requirements.txt`

`streamlit run main.py`

#### The application should be accesible on web brwoser via `localhost:8501`

## Contributions

Contributions are welcomed! Please open pull request on this repository.

## Disclaimer

This application is for educational purpose only. Please use it with your own risk. **The datasource used in this project are from from investpy API and may/should not be representative to the real market data.** For serious retail traders, I recommend seeking datasource from [authorized data providers by SET](https://www.set.or.th/en/products/info/data_vendors_p1.html) and do additonak research in this topic.
