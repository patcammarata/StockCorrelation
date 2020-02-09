from collections import deque
import PySimpleGUI as sg
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


'''

The following code is here solely for reference as a test case:

apple = ['AAPL']
tesla = ['TSLA']
apple_data = yf.download(apple, '2018-12-21', '2019-12-21')
tesla_data = yf.download(tesla, '2018-12-21', '2019-12-21')
apple_closing_prices = apple_data.iloc[:,-2]
tesla_closing_prices = tesla_data.iloc[:,-2]
apple_dates = ???
tesla_dates = ???

plt.plot(apple_closing_prices, label="AAPL")
plt.plot(tesla_closing_prices, label="TSLA")
plt.legend(loc="upper left")
plt.ylabel('Price ($)')
plt.xlabel('Time')
plt.show()

covariance = np.cov(apple_closing_prices, tesla_closing_prices)
apple_std = np.std(apple_closing_prices)
tesla_std = np.std(tesla_closing_prices)
normalized_covariance = (covariance)/((apple_std)*(tesla_std))
pearson = normalized_covariance[0,1]
print(pearson)

'''

sg.theme('Dark')


def correlation(a, b, start_date, end_date):
    ticker_1 = ['{}'.format(a)]
    ticker_2 = ['{}'.format(b)]
    one_data = yf.download(ticker_1, '{}'.format(start_date), '{}'.format(end_date), period='1mo', interval='1d')
    two_data = yf.download(ticker_2, '{}'.format(start_date), '{}'.format(end_date), period='1mo', interval='1d')
    one_closing_prices = one_data.iloc[:,-2]
    two_closing_prices = two_data.iloc[:,-2]
    one_dates_queue = deque()
    two_dates_queue = deque()
    one_dates = one_closing_prices.index.values
    two_dates = two_closing_prices.index.values
    '''
    isolates axes values (in this case, dates) but not in the right format
    for x in one_closing_prices.axes:
        one_dates_queue.append(x)
    for y in two_closing_prices.axes:
        two_dates_queue.append(y)
    '''
    for i in one_dates:
        one_dates_queue.append(i)
    for j in two_dates:
        two_dates_queue.append(j)
    # print(str(one_dates_queue[0])[:10]) reformats 2018-02-01T00:00:00.000000 to 2018-02-01 and prints the result
    start_date = (str(one_dates_queue[0])[:10])
    end_date = (str(one_dates_queue[-1])[:10])
    if len(one_dates_queue) < len(two_dates_queue):
        while len(one_dates_queue) < len(two_dates_queue):
            two_dates_queue.popleft()
        start_date = (str(two_dates_queue[0])[:10])
    if len(two_dates_queue) < len(one_dates_queue):
        while len(two_dates_queue) < len(one_dates_queue):
            one_dates_queue.popleft()
        start_date = (str(one_dates_queue[0])[:10])

    arr_1_queue = deque()
    arr_2_queue = deque()
    for i in one_closing_prices:
        arr_1_queue.append(i)
    for j in two_closing_prices:
        arr_2_queue.append(j)
    if len(arr_1_queue) < len(arr_2_queue):
        while len(arr_1_queue) < len(arr_2_queue):
            arr_2_queue.popleft()
    if len(arr_2_queue) < len(arr_1_queue):
        while len(arr_2_queue) < len(arr_1_queue):
            arr_1_queue.popleft()

    covariance = np.cov(arr_1_queue, arr_2_queue)
    arr_1_std = np.std(arr_1_queue)
    arr_2_std = np.std(arr_2_queue)
    normalized_covariance = (covariance)/((arr_1_std)*(arr_2_std))
    pearson_1 = round(normalized_covariance[0,1], 3)

    if 0 < pearson_1 <= 0.3:
        window['output'].update('{} and {} have a weak positive correlation of {} between {} and {}.'.format(a, b, pearson_1, start_date, end_date))
    if 0.3 < pearson_1 <= 0.7:
        window['output'].update('{} and {} have a moderate positive correlation of {} between {} and {}.'.format(a, b, pearson_1, start_date, end_date))
    if 0.7 < pearson_1 < 1:
        window['output'].update('{} and {} have a strong positive correlation of {} between {} and {}.'.format(a, b, pearson_1, start_date, end_date))
    if pearson_1 == 1:
        window['output'].update('{} and {} have a perfect positive correlation of {} between {} and {}.'.format(a, b, pearson_1, start_date, end_date))
    if pearson_1 == 0:
        window['output'].update('{} and {} have no correlation of {} between {} and {}.'.format(a, b, pearson_1, start_date, end_date))
    if pearson_1 == -1:
        window['output'].update('{} and {} have a perfect negative correlation of {} between {} and {}.'.format(a, b, pearson_1, start_date, end_date))
    if -1 < pearson_1 < -0.7:
        window['output'].update('{} and {} have a strong negative correlation of {} between {} and {}.'.format(a, b, pearson_1, start_date, end_date))
    if -0.7 <= pearson_1 < -0.3:
        window['output'].update('{} and {} have a moderate negative correlation of {} between {} and {}.'.format(a, b, pearson_1, start_date, end_date))
    if -0.3 <= pearson_1 < 0:
        window['output'].update('{} and {} have a weak negative correlation of {} between {} and {}.'.format(a, b, pearson_1, start_date, end_date))


def plot(a, b, start_date, end_date):
    ticker_1 = ['{}'.format(a)]
    ticker_2 = ['{}'.format(b)]
    one_data = yf.download(ticker_1, '{}'.format(start_date), '{}'.format(end_date), period='1mo', interval='1d')
    two_data = yf.download(ticker_2, '{}'.format(start_date), '{}'.format(end_date), period='1mo', interval='1d')
    one_closing_prices = one_data.iloc[:,-2]
    two_closing_prices = two_data.iloc[:,-2]
    style.use('ggplot')
    plt.plot(one_closing_prices, label="{}".format(a))
    plt.plot(two_closing_prices, label="{}".format(b))
    plt.legend(loc="upper left")
    plt.xlabel('Time')
    plt.ylabel('Price ($)')
    plt.show(block=False)


def error_output():
    window['output'].update('Please enter valid information.')


layout = [[sg.Text('Enter 2 valid ticker symbols (e.g. AAPL for Apple):')],
          [sg.Text('Ticker 1: ', size=(8,1)), sg.Input(key='a', size=(35,1))],
          [sg.Text('Ticker 2: ', size=(8,1)), sg.Input(key='b', size=(35,1))],
          [sg.Text('_' * 10)],
          [sg.Text('Enter a time frame (formatted as year-month-day): ')],
          [sg.Text('Start date: ', size=(8,1)), sg.Input(key='start', size=(35,1))],
          [sg.Text('End date: ', size=(8,1)), sg.Input(key='end', size=(35,1))],
          [sg.Text('_' * 10)],
          [sg.Text('NOTE: Dates may be automatically adjusted to ensure accuracy.')],
          [sg.Text('', size=(85,1), key='output')],
          [sg.Submit(), sg.Button('Plot'), sg.Cancel()]]

window = sg.Window('Stock Correlation Calculator', layout, default_element_size=(40, 1), grab_anywhere=False)

while True:  # Event Loop
    event, values = window.read()
    a = values['a']
    b = values['b']
    start_date = values['start']
    end_date = values['end']
    if event == 'Cancel':
        break
    elif event == 'Plot':
        try:
            plot(a, b, start_date, end_date)
        except ValueError:
            error_output()

    elif event == 'Submit':
        try:
            correlation(a, b, start_date, end_date)
        except ValueError:
            error_output()

    else:
        break

window.close()