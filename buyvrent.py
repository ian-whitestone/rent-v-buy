from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict

###################################################################
############################ CONSTANTS ############################
###################################################################


#################
#### GENERAL ####
#################
TAX_RATE = 0.3
RRSP_WITHDRAWAL = 0 #25000
HOME_APPREC = 0.03

#####################
#### RENT INPUTS ####
#####################
ROI = 0.04 ## what you can get elsewhere with your $$$ (after commission + capital gains tax)
RENT = 1750 # $/month

# in Canada, this is the most they can raise rent without filing some official form
# however, if you switch to a different unit you are likely to see a much higher increase
RENT_INFLATION = 0.025


#######################
#### BUYING INPUTS ####
#######################

##MORTAGE DETAILS
MORTGAGE_LEN = 30
INT_RATE = 2.8 / 100 ##starting interest rate
INT_RATE_INCR = 0 #0.25 / 100 ## yearly interest rate increase

##SELL YEAR
SELL_YEAR = 5

##HOUSE DETAILS
LIST_PRICE = 450000
DOWN_PAYMENT = 0.3 ##percent

TAX = 2400 ##yearly tax
INSURANCE = 200 ##yearly content insurance
CONDO_FEES = 450 ##monthly condo fees

BUY_FEE = 3000 ##cost to purchase the home --> includes condo doc review
SELL_FEE_RATE = 0.05
SELL_FEE = 3000 ##need to research this

######################################################################
############################ CALCULATIONS ############################
######################################################################
## enter the ranges you want to test for each variable
## order them as: [lowest, highest, base_case]
## base case must equal the value you set above

## TODO: change this to % factors
stress_test = {
    'RENT': [1500, 2000, RENT],
    'ROI': [0.03, 0.05, ROI],
    'LIST_PRICE': [400000, 500000, LIST_PRICE],
    'CONDO_FEES': [350, 550, CONDO_FEES],
    'DOWN_PAYMENT': [0.2, 0.4, DOWN_PAYMENT],
    'HOME_APPREC': [0.01, 0.05, HOME_APPREC],
    'INT_RATE': [0.020, 0.045, INT_RATE],
    'SELL_YEAR': [3, 10, SELL_YEAR]
}

npv = {}
stress_levels = [-1, 1, 0]

for var, values in stress_test.items():
    npv[var] = {}
    for value, x in zip(values, stress_levels):
        exec('%s = %s' % (var, value)) ## set the variable equal to it's new value

        ##total monthly costs
        loan = LIST_PRICE - DOWN_PAYMENT*LIST_PRICE
        mortgage_payment = (INT_RATE*loan/12)/(1-(1+INT_RATE/12)**(-1*MORTGAGE_LEN*12))
        home_monthly = mortgage_payment + CONDO_FEES + (TAX+INSURANCE)/12

        ##should technically only subtract RRSP savings over a 5 year period (or however long it would take to refill 25000)
        rent_equity = DOWN_PAYMENT*LIST_PRICE + BUY_FEE - RRSP_WITHDRAWAL*TAX_RATE
        home_equity = DOWN_PAYMENT

        home_price = LIST_PRICE

        for month in range(1,MORTGAGE_LEN*12+1):
            int_amount = loan * INT_RATE / 12
            equity_amount = mortgage_payment - int_amount
            loan -= equity_amount

            monthly_home_apprec = home_price*HOME_APPREC/12
            home_price += monthly_home_apprec

            rent_equity += rent_equity*ROI/12 + home_monthly - RENT*(1+RENT_INFLATION/12)
            home_equity += equity_amount + monthly_home_apprec

            INT_RATE += INT_RATE_INCR/12

            ## recalculate mortgage_payment at new interest rate
            ## if INT_RATE_INCR = 0 it won't change
            if month<360:
                mortgage_payment = (INT_RATE*loan/12)/(1-(1+INT_RATE/12)**(-1*(MORTGAGE_LEN-month/12)*12))
                home_monthly = mortgage_payment + CONDO_FEES + (TAX+INSURANCE)/12

            if month == SELL_YEAR*12:
                temp_home_equity = home_price - loan - SELL_FEE_RATE*home_price - SELL_FEE
                npv[var][x] = round((temp_home_equity-rent_equity)/((1+ROI)**month/12),0)

pprint(npv)

legend = []
# b g r c m k
colours = ['bo', 'go', 'ro', 'co', 'mo', 'ko', 'b^', 'g^']

fig = plt.figure()
ax = fig.add_subplot(111)

i = 0
for var, values in npv.items():
    x = [-1, 0, 1]
    y = [values[i] for i in x]
    legend.append(var)
    ax.plot(x, y, colours[i]) ## scatter plot
    # ax.plot(x, y) ## line plot
    i += 1

ax.set_xlim(xmin=-1.5, xmax=1.5)
ax.legend(legend, loc='upper left')

stepsize = 5000
start, end = ax.get_ylim()
ax.yaxis.set_ticks(np.arange(start, end, stepsize))


plt.show()
