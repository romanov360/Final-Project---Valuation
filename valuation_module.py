import pandas as pd
import numpy as np
import random as rd
import numpy_financial as npf

stocks_csv = pd.read_csv('Stocks.csv')



def info():
    """Tells the user what the stock market is."""
    return 'The stock market is like astrology for gambling addicts.\
            \nIf you can convince somebody that you can predict their financial success,\
            \n(even if you can\'t), they\'ll trust you as a guide.'



def company_names():
    """Tells the user what companies they can pick."""
    names_string = 'Which company would you like to know about? You can pick from 25 companies: \n'
    
    # This loop adds the 25 company names into a string that the user will use to
    # chooose a company to learn about. They are split into five rows, containing
    # five names each. Before the last name, the word 'and' is placed, because grammar.
    
    for i in range(len(stocks_csv['Name'])-1):
        names_string = names_string + stocks_csv['Name'][i] + ', '
        if (i+1) % 5 == 0:
            names_string = names_string + '\n'
    names_string = names_string + 'or ' + stocks_csv['Name'][len(stocks_csv['Name'])-1]
    return names_string



def company_business(entered_name):
    """Tells the user how the company makes money."""
    
        # First, some error handling. We want to make sure that they're entering a valid company name.
        # If they enter a valid company name, then the index of the name is remembered, to make the next part cleaner.
        
    try:
        name_index = stocks_csv.loc[stocks_csv['Name'] == entered_name].index[0]
    except:
        print('Whoops, that\'s not a company name. Copy-and-paste to ensure accuracy.')
        return
        
        # Then, we print out the corresponding value in the column Business,
        #  which contains info on how that company makes its money.
        
    return entered_name + '\'s business is ' + stocks_csv.T[name_index]['Business'] + '.'




def company_earnings(entered_name):
    """Tells the user how much the company profited last year."""
    
    try:
        name_index = stocks_csv.loc[stocks_csv['Name'] == entered_name].index[0]
    except:
        print('Whoops, that\'s not a company name. Copy-and-paste to ensure accuracy.')
        return
        
    # Did they make or lose money? We'll format the string using this fact.
    
    made_or_lost = ' made $'
    if stocks_csv.T[name_index]['Earnings'] <= 0:
        made_or_lost = ' lost $'
    
    # How much did they make or lose? Data is in $1,000,000's, hence the multiplier.
    # I got the string format trick from kite.com.
    
    profit = "{:,}".format(abs(stocks_csv.T[name_index]['Earnings'] * 1000000))
    
        
    return entered_name + made_or_lost + profit + ' last year.'



def future(entered_name):
    """Guesses how much a company is predicted to grow or shrink"""
    
    try:
        name_index = stocks_csv.loc[stocks_csv['Name'] == entered_name].index[0]
    except:
        print('Whoops, that\'s not a company name. Copy-and-paste to ensure accuracy.')
        return
        
    # Creating a row vector which will soon contain a company's future earnings.
    
    earnings_over_time = np.zeros(50)
    earnings_over_time[0] = stocks_csv.T[name_index]['Earnings']
    
    # The price of the stock can be used to guess how much Wall Street thinks the company will grow (or shrink).
    # Let's say that a company grows by 10% a year. The Net Present Value of the sequence of a company's earnings,
    # where each value is 10% greater than the previous, gives an estimate of the company's true price.
    # (Net Present Value is a brilliant formula which values future cash in terms of today's cash)
    # This price is compared with the current price of the stock. If the stock's price is higher, then 
    # Wall Street predicts that it will grow more than 10% a year. If it is lower, then it is predicted
    # to grow at less than 10% a year. The following algorithm tries to predict how much Wall Street
    # thinks it will grow by guessing a value and checking it.
    
    good_guess = False
    
    # Loop breaks when a good guess is found.
    while good_guess == False:
        
        # Gotta start somewhere.
        
        guess = rd.randint(-5,25)
        
        # If they lost money last year, the model will predict that they will stop losing money next year,
        # and start growing the year after that, starting with -1/4 of their losses. So that the formula doesn't break.
        
        counter = 1
        if earnings_over_time[0] < 0:
            earnings_over_time[2] = -.25 * earnings_over_time[0]
            counter = 3
        
        # Loop breaks when the earnings vector is populated with future earnings, using the guessed value.
        
        while counter < 50:
            earnings_over_time[counter] = earnings_over_time[counter-1] * (1 + (guess / 100))
            counter += 1
        
        # Market capitalization (Wall Street's price) is calculated by shares x share price.
        # The function that does this is two below this one.
        
        market_cap = market_capitalization(entered_name)
        
        
        # Pretending that risk is 6%. In reality, there are floors on top of floors of people trying to determine risk.
        # A good guess is one that falls close to the expected value. When a good guess is made, the loop breaks.
        
        if npf.npv(.06, earnings_over_time) < 1.2 * market_cap and npf.npv(.06, earnings_over_time) > market_cap * .88:
            good_guess = True
        
    # If the company lost money last year, but Wall Street expects them to make a comeback,
    # some special string formatting is factored into the prediction
    
    comeback = '.'
    if earnings_over_time[0] <= 0:
        comeback = ', after recovering from its losses next year, \
            \nand then making $' + "{:,}".format(int(earnings_over_time[2]*1000000)) + ' the year after.'
    
    # Some more things that will make the final string nicer.
    
    grow_or_shrink = '\'s income to grow '
    if guess <=0:
        grow_or_shrink = '\'s income to shrink '
        
    # The string containing Wall Street's prediction is returned.
        
    return 'Wall Street expects ' + entered_name + grow_or_shrink + str(abs(guess)) + '% yearly' + comeback



def ticker(entered_name):
    """Returns the company's stock ticker."""
    try:
        name_index = stocks_csv.loc[stocks_csv['Name'] == entered_name].index[0]
    except:
        print('Whoops, that\'s not a company name. Copy-and-paste to ensure accuracy.')
        return
        
    # It's good to know a company's ticker.
        
    return stocks_csv.T[name_index]['Ticker']



def summary(entered_name):
    """Combines multiple functions into one, giving the user a summary of their company of choice."""
    
    # Just a bunch of string formatting and function calling to output one super-detailed summary.
    
    try:
        stocks_csv.loc[stocks_csv['Name'] == entered_name].index[0]
    except:
        print('Whoops, that\'s not a company name. Copy-and-paste to ensure accuracy.')
        return
    
    summary_string = company_business(entered_name) + \
    '\nTheir ticker, which is like an abbreviation, is ' + ticker(entered_name) + '.\n' + \
    company_earnings(entered_name) + '\n' + \
    future(entered_name)
    
    return summary_string



def market_capitalization(entered_name):
    """Returns a company\'s market capitalization'"""
    
    try:
        name_index = stocks_csv.loc[stocks_csv['Name'] == entered_name].index[0]
    except:
        print('Whoops, that\'s not a company name. Copy-and-paste to ensure accuracy.')
        return
        
    # Market capitalization (Wall Street's price) is calculated by shares x share price.
    
    market_cap = stocks_csv.T[name_index]['S/O'] * stocks_csv.T[name_index]['Price'] / 1000
    
    return market_cap



def trillionaires():
    """Tells the user who the big players are"""
    
    trillionaires_string = 'The companies worth over $1T are: \n'
    
    # A loop that stringifies the stock market behemoths.
    
    for i in range(len(stocks_csv['Name'])):
        if market_capitalization(stocks_csv['Name'][i]) > 1000000:
            trillionaires_string = trillionaires_string + stocks_csv['Name'][i] + '\n'
            
    return trillionaires_string