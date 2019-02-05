# This program is a part of my pseudo-ai Winston. It gathers and organizes
# stock data for a given stock and tick code for later analysis. Utilises 
# several diffrent apis and io functionality. 

from modules.winstock_analyzer import Winstock_Analyzer
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd 
# import seaborn as sns
import quandl
import json
import os


class Winstock:
    """
    Winstock is the gathering point for Winstons stock-functionality. It gathers, updates
    and manages all the stocks tracked by Winston.
    """
    API_KEY = os.environ['QUANDL_API_KEY']
    STOCK_INDEX_PATH = 'abilities/finance/winstock/data/indexes/'
    

    def __init__(self):
        self._setup_auth()
        self._load_stock_list()
        # self.update_stocks()
        # self._update_stock_index()

        self.analyzer = Winstock_Analyzer()


    #region public functions
    def update_stocks(self):
        """
        Updates all the tracked stocks with the latest data. 

        Checks to see if there is any new stock info, if there is 
        it appends it to the currently existing dataframe for each stock.
        """

        for stock in self.saved_stocks_list:
            name = stock['stock']
            symbol = stock['symbol']
            self.get_stock(name, symbol)
            self._update_stock(name, symbol)

    def get_stock(self, stock, symbol):
        """
        Get data for a specific stock.
        Returns the full stock history as a pandas df. 
        Also sets the stock data as accessible via self.stock

        stock: The name of the company (Apple Inc, Google, Nintendo etc)
        symbol: The stock symbol (AAPL, GOOGL, NTDOY etc)
        """
        if self._stock_saved(stock, symbol):
            self.stock = self._load_stock(stock, symbol)
            self._update_stock(stock, symbol) 
            return self.stock
        else:
            self.stock = self._download_stock(stock, symbol)
            return self.stock
    
    def get_stock_index(self, index_code='NASDAQOMX/OMXS30'):
        """
        Get data for a specific stock_index
        Return the full index history as a pandas df
        Also sets the stock data as accessible via self.stock_index

        index_code: The quandl code for the stock index (default='NASDAQOMX/OMXS30')
        """

        file_name = index_code.split('/')[1]
        path = self._create_path((self.STOCK_INDEX_PATH + index_code), file_name, 'csv')
        stock_index = pd.read_csv(path)
        stock_index['date'] = pd.to_datetime(stock_index['date'])
        return stock_index

    #endregion

    #region boilerplate stuff
    def _setup_auth(self):

        self.ts = TimeSeries(key=self.API_KEY, output_format='pandas')
        
        #Setup Quandl
        quandl.ApiConfig.api_key = 'z2SPBjmuebZ8sqUyyvxV'
    #endregion

    #region stock_list functions
    def _load_stock_list(self):
        p = Path(f'abilities/finance/winstock/data/stock/list.json').as_posix()
        with open(p, 'r') as file:
            self.saved_stocks_list = json.load(file)

    def _save_stock_list(self):
        p = Path(f'abilities/finance/winstock/data/stock/list.json').as_posix()
        with open(p, 'w') as file:
            json.dump(self.saved_stocks_list, file)

    def _add_stock_to_list(self, stock, symbol):
        stock = {'stock': stock, 'symbol': symbol}

        if stock not in self.saved_stocks_list:
            self.saved_stocks_list.append(stock)
            self._save_stock_list()

    def _remove_stock_from_list(self, stock, symbol):
        stock = {'stock': stock, 'symbol': symbol}
        
        if stock in self.saved_stocks_list:
            self.saved_stocks_list.remove(stock)
            self._save_stock_list()
    #endregion

    #region stock functions
    def _download_stock(self, stock, symbol):
        """
        Downloads stock data from the Alpha Vantage API. Returns a pandas dataframe
        
        stock: The name of the company (Apple Inc, Google, Nintendo etc)
        symbol: The stock symbol (AAPL, GOOGL, NTDOY etc)
        """
        
        self.stock = pd.DataFrame()
        self.stock, self.meta_data = self.ts.get_daily(symbol, outputsize='full') #pylint: disable=E0632
        self.stock.reset_index(inplace=True)
        self.meta_data['6. Stock'] = stock  #pylint: disable=E1137
        
        return self._save_stock(stock, symbol)

    def _update_stock(self, stock, symbol):
        """
        Checks if daily stock info is up to date. 
        If not then downloads, updates and saves updated version of stock data.

        stock: The name of the company (Apple Inc, Google, Nintendo etc)
        symbol: The stock symbol (AAPL, GOOGL, NTDOY etc)
        """

        last = self.stock.iloc[-1]['date'].date()
        current = datetime.now().date()

        if last < current: 
            update_df, _ = self.ts.get_daily(symbol, outputsize='compact')
            update_df.reset_index(inplace=True)
            update_df['date'] = pd.to_datetime(update_df['date'])
            update_df = update_df[update_df['date'] > last]
            self.stock = self.stock.append(update_df, ignore_index=True) 

            self._save_stock(stock, symbol)   

    def _save_stock(self, stock, symbol):
        """
        Saves stock to file in the data/stock/ folder. 
        Additionally saves some metainformation in a separate file called 'meta.csv'

        stock: The name of the company (Apple Inc, Google, Nintendo etc)
        symbol: The stock symbol (AAPL, GOOGL, NTDOY etc)
        """

        self.stock.to_csv(self._get_stock_path(stock, symbol), index=False)
        self._add_stock_to_list(stock, symbol)

        return self._load_stock(stock, symbol)

    def _load_stock(self, stock, symbol):
        """
        Loads saved stock data. Returns a pandas dataframe
        
        stock: The name of the company (Apple Inc, Google, Nintendo etc)
        symbol: The stock symbol (AAPL, GOOGL, NTDOY etc)
        """

        df = pd.read_csv(self._get_stock_path(stock, symbol))
        # df['date'] = pd.to_datetime(df.loc[:, 'date'])
        df['date'] = pd.to_datetime(df['date'])

        return df

    def _stock_saved(self, stock, symbol):
        """Checks whether there is data previously downloaded for the selected stock.
        
        returns a boolean.
        stock: The name of the company (Apple Inc, Google, Nintendo etc)
        symbol: The stock symbol (AAPL, GOOGL, NTDOY etc)
        """

        p = Path(f'abilities/finance/winstock/data/stock/{stock}/{symbol}/{symbol}.csv') 
        return p.exists()

    def _get_stock_path(self, stock, symbol):
        p = Path(f'abilities/finance/winstock/data/stock/{stock}/{symbol}')

        if not p.exists():
            p.mkdir(parents=True)

        return f'{p.as_posix()}/{symbol}.csv'
    
    def _get_meta_path(self, stock, symbol):
        p = Path(f'abilities/finance/winstock/data/stock/{stock}/{symbol}')

        if not p.exists():
            p.mkdir(parents=True)

        return f'{p.as_posix()}/meta.csv'
    #endregion

    #region stock_index functions
    def _download_stock_index(self, index_code='NASDAQOMX/OMXS30'):
        """
        Downloads data for the chosen stock index

        index_code: The quandl-code for the selected index ('NASDAQOMX/OMXS30')
        index_name: What the folder name of the saved index data will be
        """

        stock_index = quandl.get(index_code)
        stock_index.reset_index(inplace=True)
        stock_index.rename(columns={'Trade Date': 'date'}, inplace=True)

        path = f'{self.STOCK_INDEX_PATH + index_code}'
        file_name = index_code.split('/')[1]
        p = self._create_path(path, file_name, 'csv')
        stock_index.to_csv(p, index=False)

    def _update_stock_index(self, index_code='NASDAQOMX/OMXS30'):
        """
        Checks if stock-index data is up to date, if not then downloads and adds missing dates.
        Returns the stock index as a pandas dataframe.

        index_code: The quandl-code for the selected index ('NASDAQOMX/OMXS30')
        index_name: What the folder name of the saved index data will be
        """

        #Load file
        file_name = index_code.split('/')[1]
        path = self._create_path((self.STOCK_INDEX_PATH + index_code), file_name, 'csv')
        stock_index = pd.read_csv(path)
        stock_index['date'] = pd.to_datetime(stock_index['date'])

        #Check if update needed
        last = stock_index.iloc[-1]['date'].date()
        if last < datetime.now().date():
            stock_index_update = quandl.get(index_code, start_date=last + timedelta(days=1))
            stock_index_update.reset_index(inplace=True)
            stock_index_update.rename(columns={'Trade Date': 'date'}, inplace=True)
            stock_index = stock_index.append(stock_index_update, ignore_index=True) 
            dates = stock_index.pop('date')
            stock_index.insert(0, 'date', dates)
            stock_index.to_csv(path, index=False)
        
        return stock_index
    #endregion

    #region utility functions
    def _create_path(self, path, file_name=None, file_ending=None):
        """
        takes an url string, checks if the directory exists, if it doesn't it creates it.
        Returns a string with filename at end if filename was provided else returns None.

        path: The directory you want to create/check as a string ('abilities/finance/winstock'). 
        file_name: What you want the (optional) file to be named
        file_ending: What you want the file ending to be ('csv', 'json' etc)
        """

        p = Path(path)
        if not p.exists():
            p.mkdir(parents=True)
        if file_name and file_ending:
            return f"{p.as_posix()}/{file_name}.{file_ending}"
        
    #endregion


if __name__ == '__main__':
    winstock = Winstock()

    # stock = winstock.get_stock('Volvo-B', 'VOLV-B.ST')
    # stock = winstock.get_stock('Nintendo', 'NTDOY')
    stock = winstock.get_stock('Tesla', 'TSLA')
    stock_index = winstock.get_stock_index()
    result = winstock.analyzer.stock_to_index(stock, stock_index)
    
    
