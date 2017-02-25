#################
#### GENERAL ####
#################
tax_rate = 0.3
rrsp_withdrawal = 25000
home_apprec = 0.02

#####################
#### RENT INPUTS ####
#####################
roi = 0.04 ## what you can get elsewhere with your $$$ (after commission + capital gains tax)
rent_monthly = 1750 # $/month

# in Canada, this is the most they can raise rent without filing some official form
# however, if you switch to a different unit you are likely to see a much higher increase
rent_inflation = 0.025


#######################
#### BUYING INPUTS ####
#######################

##MORTAGE DETAILS
num_years = 30
int_rate = 2.8 / 100 ##starting interest rate
int_rate_incr = 0.25 / 100 #0.33 / 100 ##yearly interest rate increase


##HOUSE DETAILS
list_price = 400000
down_payment = 60000

tax = 2400 ##yearly tax
insurance = 200 ##yearly content insurance
condo_fees = 400 ##monthly condo fees

buy_cost = 3000 ##cost to purchase the home
sell_cost = 0.05

##total monthly costs
loan = list_price - down_payment
mortgage_payment = (int_rate*loan/12)/(1-(1+int_rate/12)**(-1*num_years*12))
home_monthly = mortgage_payment + condo_fees + (tax+insurance)/12

##should technically only subtract RRSP savings over a 5 year period (or however long it would take to refill 25000)

rent_equity = down_payment + buy_cost - rrsp_withdrawal*tax_rate
home_equity = down_payment

print ('Monthly mortgage payment: {0:.2f} Monthly interest amount (yr 1) {0:.2f}'.format(home_monthly,loan*int_rate/12))

print ('MONTH \t RENT EQUITY \t HOME EQUITY \t LOAN AMT')

sell_years = [5,10,15,20]

home_price = list_price
sell_dict = {}
for month in range(1,num_years*12+1):
    int_amount = loan * int_rate / 12
    equity_amount = mortgage_payment - int_amount
    loan -= equity_amount

    monthly_home_apprec = home_price*home_apprec/12
    home_price += monthly_home_apprec

    rent_equity += rent_equity*roi/12 + home_monthly - rent_monthly*(1+rent_inflation/12)
    home_equity += equity_amount + monthly_home_apprec

    int_rate += int_rate_incr/12

    sre = '$' + str(round(rent_equity,0))
    she = '$' + str(round(home_equity,0))
    # print ('%s \t %s \t %s \t %s' % (month,sre,she,'$'+str(round(loan,0))))

    ##recalculate mortgage_payment at new interest rate
    if month<360:
        mortgage_payment = (int_rate*loan/12)/(1-(1+int_rate/12)**(-1*(num_years-month/12)*12))
        home_monthly = mortgage_payment + condo_fees + (tax+insurance)/12

    if month in [x*12 for x in sell_years]:
        print ('home price after %s years is: %s' % (month/12,round(home_price,0)))
        temp_home_equity = home_price - loan - sell_cost*home_price
        sell_dict[month/12]={}
        sell_dict[month/12]['home_npv'] = (temp_home_equity-rent_equity)/((1+roi)**month/12)
        sell_dict[month/12]['rent_npv'] = (rent_equity-temp_home_equity)/((1+roi)**month/12)


for sell_year in sell_years:
    print ('After %s years \n Home NPV: $%0.2f \n Rent NPV: $%0.2f' %
        (sell_year, sell_dict[sell_year]['home_npv'],
        sell_dict[sell_year]['rent_npv']))
