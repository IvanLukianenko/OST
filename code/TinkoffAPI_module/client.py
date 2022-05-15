from openapi_client import openapi


SANDBOX_TOKEN = "t.dti3PE10t2_ANB9JE1cnwskzv3ZtwEHbH5Sn9p25W0yt0EZokCqVLIuQ75fqn3WZQGshizm8HCrvA7eqPEW49A"


class MyClient:
    def __init__(self, token=TOKEN):
        self.token = token
        self.client = openapi.api_client(self.token)
        self.pf = self.client.portfolio.portfolio_get()

    def get_my_stocks(self):
        stock_info = {}
        for stock in self.pf.payload.positions:
            stock_info[stock.name] = {
                "value": stock.average_position_price.value,
                "currency": stock.average_position_price.currency,
                "balance": stock.balance,
                "figi": stock.figi,
                "ticker": stock.ticker,
            }
        return stock_info

    def buy_stock(self, figi, lots):
        info = self.client.orders.orders_market_order_post(figi=figi,
                                                           market_order_request={
                                                               "lots": lots,
                                                               "operation": "Buy"
                                                           }
                                                           )
        print(f"Succesfully made market order to buy stock with figi = {figi}")
        return info

    def sell_stock(self, figi, lots):
        info = self.client.orders.orders_market_order_post(figi=figi,
                                                           market_order_request={
                                                               "lots": lots,
                                                               "operation": "Sell"
                                                           }
                                                           )
        print(f"Succesfully made market order to sell stock with figi = {figi}")
        return info
