# Here we assume that we have a client coming to us asking for an automated Rental Property Calculator. 
# Our client's name is Brandon from a company called "Bigger Pockets". Below, you will find a video of what 
# Brandon usually does to calculate his Rental Property ROI.

# Using Visual Studio Code/Jupyter Notebook, and Object Oriented Programming create a program that will calculate 
# the Return on Investment(ROI) for a rental property. And now that we know a thing or two about making our programs 
# run more efficiently, try utilizing some of the strategies we talked about this week for optimization!

# Your Program should have the following (this is not an exhaustive list but just base functionality):

# -  There should be some sort of Driver code for users to choose what to do next 

# -  There should be a way to store multiple users and for users to be able to have multiple different properties 
#    (This might be done by creating a User Class & a Property class similarly to how we did it with the Codeflix program)

# -  Properties should be able to store multiple different types of expenses (i.e. taxes, mortgage, insurance, etc) and 
#    multiple different types of incomes (i.e. rent, laundry, parking, etc)

# -  The ROI needs to be calculated & displayed to the user and should also be stored for that specific property.







# Still to do: flesh out User class, create UserDatabase class, create general flow of things, update Property class to have multiple forms of income instead of just 1 lump sum


class User():

    id_counter = 1
    def __init__(self, name, password):
        self.name = name.lower()
        self.password = password
        self.id = User.id_counter
        User.id_counter += 1
        self.properties = {}

    def check_password(self, password_guess):
        return self.password == password_guess[::-2]
    
    def add_property(self, property):
        self.properties[len(self.properties) +1] = Property()

    def remove_property(self):
        pass

    def show_properties(self):
        print(f'You currently have {len(self.properties)}:')
        for property in self.properties:
            print(property)

class Property():

    def __init__(self):
        self.name = ""
        self.address = ""
        self.income = 0
        self.individual_expenses = {}
        self.total_expenses = 0
        self.c_flow = 0
        self.down_payment = 0
        self.closing_costs = 0
        self.rehab_budget = 0
        self.misc_costs = 0
        self.initial_investment = 0
        self.roi = 0
        self.data = {}
        self.generate_info()

    def property_data(self):
        self.data['name'] = self.name
        self.data['address'] = self.address
        self.data['monthly income'] = '$' + str(self.income)
        self.data['monthly expenses'] = self.individual_expenses
        self.data['total expenses'] = '$' + str(self.total_expenses)
        self.data['monthly cash flow'] = '$' + str(self.c_flow)
        self.data['down payment'] = '$' + str(self.down_payment)
        self.data['closing costs'] = '$' + str(self.closing_costs)
        self.data['rehab budget'] = '$' + str(self.rehab_budget)
        self.data['miscellaneous costs'] = '$' + str(self.misc_costs)
        self.data['initial investment'] = '$' + str(self.initial_investment)
        self.data['roi'] = str(self.roi) + '%'
        print(f'The data for {self.name} is now:')
        for key,value in self.data.items():
            print(f'{key.title()}: {value}')
        
    # May just want to have the user also generate name and address as well    
    def generate_info(self):

        self.name = input('What is the name of this property? ').title()
        self.address = input(f'What is the address of {self.name}? ')

        # Getting the monthly income
        self.update_monthly_income()

        # Creating the expenses dictionary, as well as totaling up the expenses while doing so
        self.update_expenses()

        # Determining the cash flow:
        self.cash_flow() 

        # Determining the initial investment
        self.purchasing_costs()

        # Determines current Cash on Cash ROI
        self.cash_on_cash()

        # Storing all of the property's data in a dictionary for later use, like the user wanting to see certain things about a property
        self.property_data()

    # Updating the monthy income (need to add the ability to change the monthly income after initially setting it
    # when this function is called outside of generate_info)
    def update_monthly_income(self):
        while True:
            try:
                income = float(input(f"What is your total monthly income for {self.name}? $"))
                if income >= 0:
                    self.income = income
                    break
                else:
                    print('You can not have a negative income')
            except:
                print('Please enter a valid sum of money for the income')

    # Updates the expenses dictionary, as well as totaling up the expenses while doing so
    def update_expenses(self):
        add_expenses = input(f'Would you like to add any expenses for {self.name}? (y/n) ').lower()
        if add_expenses in {'y', 'yes', 'yeah', 'ya', 'you bet your ass i do'}:
            total = self.total_expenses
            while True:    
                try:
                    expense_type = input(f"What is the expense you would like to add for {self.name}? ").lower()
                    expense_cost = float(input(f"What is your monthly cost for {expense_type}? $"))
                    if expense_cost >= 0 and expense_type not in self.individual_expenses:
                        self.individual_expenses[expense_type] = expense_cost
                        total += expense_cost
                        add_another = input(f'Your list of expenses for {self.name} so far are \n {self.individual_expenses} \n and are ${total} in total. \
                                            \nWould you like to add another expense for {self.name}? (y/n) ').lower()
                        if add_another not in {'y', 'yes', 'yeah', 'ya', 'you bet your ass i do'}:
                            print(f'Your list of expenses for {self.name} are \n {self.individual_expenses} \n and are ${total} in total.')
                            self.total_expenses = total
                            break   
                    else:
                        if expense_type in self.individual_expenses:
                            change_cost = input(f'{expense_type} is already in your list of expenses as ${self.individual_expenses[expense_type]}.  Do you want to update the cost to be ${expense_cost}? (y/n) ').lower()
                            if change_cost in {'y', 'yes', 'yeah', 'ya', 'you bet your ass i do'}:
                                total -= self.individual_expenses[expense_type]
                                self.individual_expenses[expense_type] = expense_cost
                                total += expense_cost
                            add_another = input(f'Your list of expenses for {self.name} so far are \n {self.individual_expenses} \n and are ${total} in total. \
                                        \nWould you like to add another expense for {self.name}? (y/n) ').lower()
                            if add_another not in {'y', 'yes', 'yeah', 'ya', 'you bet your ass i do'}:
                                print(f'Your list of expenses for {self.name} are \n {self.individual_expenses} \n and are ${total} in total.')
                                self.total_expenses = total
                                break 
                        else:
                            print(f'You can not have a negative amount for {expense_type}')
                except:
                    print(f'Please enter a valid sum of money for {expense_type}')
        
    # determines the current cash flow of the property
    def cash_flow(self):
        self.c_flow = self.income - self.total_expenses
        print(f'The cash flow for {self.name} is currently ${self.c_flow}')

    # Determines the initial investment (needs to add functionality in case user wants to update this information, and checking to make sure they want to update it)
    def purchasing_costs(self):
        while True:
            try:
                down_payment = float(input(f'What was the down payment for {self.name}? $'))
                if down_payment <= 0:
                    print(f'You can not have a down payment of ${down_payment}')
                    continue
                closing_costs = float(input(f'What were the closing costs for {self.name}? $'))
                if closing_costs <= 0:
                    print(f'You can not have closing costs of ${closing_costs}')
                    continue
                rehab_budget = float(input(f'What was the rehab budget for {self.name}? (Enter 0 if none) $'))
                if rehab_budget < 0:
                    print(f'You can not have a rehab budget of ${rehab_budget}')
                    continue
                misc_costs = float(input(f'What were the miscellaneous costs for {self.name} when purchasing/renovating? (Enter 0 if none) $'))
                if misc_costs < 0:
                    print(f'You can not have miscellaneous costs of ${misc_costs}')
                    continue
                self.down_payment = down_payment
                self.closing_costs = closing_costs
                self.rehab_budget = rehab_budget
                self.misc_costs = misc_costs
                self.initial_investment = down_payment + closing_costs + rehab_budget + misc_costs
                print(f'The total inital investment for {self.name} is ${self.initial_investment}')
                break
            except:
                print('Please enter valid amounts of money')

    # Determines the current Cash on Cash ROI
    def cash_on_cash(self):
        self.roi = 100*((12*self.c_flow)/self.initial_investment)
        print(f"{self.name}'s cash on cash ROI is currently {self.roi}%")
        
my_property = Property()