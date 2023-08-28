# Here we assume that we have a client coming to us asking for an automated Rental Property Calculator. 
# Our client's name is Brandon from a company called "Bigger Pockets". Below, you will find a video of what 
# Brandon usually does to calculate his Rental Property ROI.

# Using Visual Studio Code/Jupyter Notebook, and Object Oriented Programming create a program that will calculate 
# the Return on Investment(ROI) for a rental property. And now that we know a thing or two about making our programs 
# run more efficiently, try utilizing some of the strategies we talked about this week for optimization!


# -  Properties should be able to store multiple different types of incomes (i.e. rent, laundry, parking, etc)







# Still to do: update Property class to have multiple forms of income instead of just 1 lump sum, as well as being able to adjust attributes after initial setup

class UserDatabase():

    def __init__(self):
        self.users = {}
        self.current_user = None
    
    def add_user(self):
        name = input('What is going to be your username? ').lower()
        if name in self.users:
            print(f'The username {name} has already been taken')
        else:
            pw = input(f'What is your password for {name}? ')
            self.users[name] = User(name,pw)
            print(f'User {name} has been created with password {pw}')

    def delete_user(self):
        if self.current_user:
            choice = input(f"You would like to delete {self.current_user.name}, correct? (y/n) ").lower()
            if choice in {'y', 'ya', 'yes', 'yeah', 'correct'}:
                pw = input(f'In order to delete, please enter the password for {self.current_user.name} ')
                if self.current_user.check_password(pw):
                    print(f'{self.current_user.name} has been deleted from the system and you have been logged out')
                    name = self.current_user.name.lower()
                    self.current_user = None
                    self.users.pop(name)
                else:
                    print('Password is not valid, unable to delete')
                    self.logout()
            else:
                print(f'{self.current_user.name} was not deleted')
        else:
            name = input(f"What is the name of the user you would like to delete? ").lower()
            if name in self.users:
                pw = input(f'In order to delete, please enter the password for {name} ')
                if self.users[name].check_password(pw):
                    print(f'{name} has been deleted from the system')
                    self.users.pop(name)
                else:
                    print('Password is not valid, unable to delete')
            else:
                print(f'{name} is not a valid registered user')

    def login(self):
        if self.current_user:
            choice = input(f'{self.current_user.name} is already logged in.  Would you like to log them out?  (y/n) ').lower()
            if choice in {'y', 'ya', 'yes', 'yeah'}:
                self.logout()
            else:
                print(f'{self.current_user.name} will stay logged in')
        else:
            name = input('Please enter your username: ').lower()
            pw = input('Please enter your password: ').lower()
            if name in self.users and self.users[name].check_password(pw):
                print(f'Welcome back, {name}')
                self.current_user = self.users[name]
            else:
                print("Invalid user name and password combo")
    
    def logout(self):
        if self.current_user:
            print(f'{self.current_user.name} has been successfully logged out')
            self.current_user = None
        else:
            print('There is no user currently logged in')

class User():

    id_counter = 1

    def __init__(self, name, password):
        self.name = name.title()
        self.password = password
        self.id = User.id_counter
        User.id_counter += 1
        self.properties = {}

    def __repr__(self):
        return f"<User {self.id} | {self.name}>"
    
    def check_password(self, password_guess):
        return self.password[::-2] == password_guess[::-2]
    
    def add_property(self):
        prop_name = input('What is the name of this property? ').title()
        nameset = {value.name for value in self.properties.values()}
        if prop_name in nameset:
            print(f'You have already logged {prop_name}')
        else:
            self.properties[str(len(self.properties) +1)] = Property(prop_name)
            self.show_properties()

    def remove_property(self):
        for property in self.properties.items():
            print(property)
        deletion = input("Which property do you want to delete?  Type the number to delete it: ")
        if deletion in self.properties:
            print(f'{self.properties[deletion].name} has been deleted')
            self.properties.pop(deletion)
            self.show_properties()
        else:
            print(f'{deletion} is not a valid selection')

    def show_properties(self):
        print('You have logged the following properties:')
        for property in self.properties.items():
            print(property)

class Property():

    def __init__(self, name):
        self.name = name
        self.address = ""
        self.rent = 0
        self.laundry = 0
        self.storage = 0
        self.parking = 0
        self.misc_income = 0
        self.total_income = 0
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

    def __repr__(self):
        return f'{self.name.title()}: makes ${self.total_income} per month; ROI: {self.roi}%'

    def property_data(self):
        self.data['name'] = self.name
        self.data['address'] = self.address
        self.data['monthly income'] = '$' + str(self.total_income)
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
            # old, static code
        # while True:
        #     try:
        #         income = float(input(f"What is your total monthly income for {self.name}? $"))
        #         if income >= 0:
        #             self.income = income
        #             break
        #         else:
        #             print('You can not have a negative income')
        #     except:
        #         print('Please enter a valid sum of money for the income')

        # self.rent = 0
        # self.laundry = 0
        # self.storage = 0
        # self.parking = 0
        # self.misc_income = 0

        while True:
            try:
                rent = float(input(f'How much rent do you collect for {self.name}? $'))
                if rent <= 0:
                    print(f'You can not have a down payment of ${rent}')
                    continue
                laundry = float(input(f'How much do you collect for laundry for {self.name}? (Enter 0 if none) $'))
                if laundry < 0:
                    print(f'You can not have closing costs of ${laundry}')
                    continue
                storage = float(input(f'How much do you collect for storage for {self.name}? (Enter 0 if none) $'))
                if storage < 0:
                    print(f'You can not have a rehab budget of ${storage}')
                    continue
                parking = float(input(f'How much do you collect for parking for {self.name}? (Enter 0 if none) $'))
                if parking < 0:
                    print(f'You can not have a rehab budget of ${parking}')
                    continue
                misc_income = float(input(f'How much do you collect for miscellaneous income for {self.name}? (Enter 0 if none) $'))
                if misc_income < 0:
                    print(f'You can not have a rehab budget of ${misc_income}')
                    continue
                self.rent = rent
                self.laundry = laundry
                self.storage = storage
                self.parking = parking
                self.misc_income = misc_income
                self.total_income = rent + laundry + storage + parking + misc_income
                print(f'The total income for {self.name} is ${self.total_income}')
                break
            except:
                print('Please enter valid amounts of money')

    # Updates the expenses dictionary, as well as totaling up the expenses while doing so
    def update_expenses(self):
        add_expenses = input(f'Would you like to add any monthly expenses for {self.name}? (y/n) ').lower()
        if add_expenses in {'y', 'yes', 'yeah', 'ya', 'you bet your ass i do'}:
            total = self.total_expenses
            while True:    
                try:
                    expense_type = input(f"What is the expense you would like to add for {self.name}? ").lower()
                    expense_cost = float(input(f"What is your monthly cost for {expense_type}? $"))
                    if expense_cost >= 0 and expense_type not in self.individual_expenses:
                        self.individual_expenses[expense_type] = expense_cost
                        total += expense_cost
                        add_another = input(f'Your list of monthly expenses for {self.name} so far are \n {self.individual_expenses} \n and are ${total} in total. \
                                            \nWould you like to add another expense for {self.name}? (y/n) ').lower()
                        if add_another not in {'y', 'yes', 'yeah', 'ya', 'you bet your ass i do'}:
                            print(f'Your list of expenses for {self.name} are \n {self.individual_expenses} \n and are ${total} in total.')
                            self.total_expenses = total
                            break   
                    else:
                        if expense_type in self.individual_expenses:
                            change_cost = input(f'{expense_type} is already in your list of monthly expenses as ${self.individual_expenses[expense_type]}.  Do you want to update the cost to be ${expense_cost}? (y/n) ').lower()
                            if change_cost in {'y', 'yes', 'yeah', 'ya', 'you bet your ass i do'}:
                                total -= self.individual_expenses[expense_type]
                                self.individual_expenses[expense_type] = expense_cost
                                total += expense_cost
                            add_another = input(f'Your list of monthly expenses for {self.name} so far are \n {self.individual_expenses} \n and are ${total} in total. \
                                        \nWould you like to add another expense for {self.name}? (y/n) ').lower()
                            if add_another not in {'y', 'yes', 'yeah', 'ya', 'you bet your ass i do'}:
                                print(f'Your list of monthly expenses for {self.name} are \n {self.individual_expenses} \n and are ${total} in total.')
                                self.total_expenses = total
                                break 
                        else:
                            print(f'You can not have a negative amount for {expense_type}')
                except:
                    print(f'Please enter a valid sum of money for {expense_type}')
        
    # determines the current cash flow of the property
    def cash_flow(self):
        self.c_flow = self.total_income - self.total_expenses
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
        
print('Welcome to rental property calculator!')
users = UserDatabase()
while True:
    if users.current_user:
        choice = input("What would you like to do?  Delete Account (D), Login (L), Logout (O), Add Property (A), Remove Property (R), Show Properties (S), Quit (Q): ").lower()
        if choice in {'d', 'del', 'delete', 'delete account'}:
            users.delete_user()
        elif choice in {'l', 'login', 'log in'}:
            users.login()
        elif choice in {'o', 'logout', 'log out'}:
            users.logout()
        elif choice in {'a', 'add', 'add property'}:
            users.current_user.add_property()
        elif choice in {'r', 'remove', 'remove property'}:
            users.current_user.remove_property()
        elif choice in {'s', 'show', 'show properties'}:
            users.current_user.show_properties()
        elif choice in {'q', 'quit', 'exit'}:
            break
        else:
            print("Invalid selection")
    else:
        choice = input("What would you like to do?  Register (R), Delete Account (D), Login (L), Quit (Q): ").lower()
        if choice in {'r', 'reg', 'register'}:
            users.add_user()
        elif choice in {'d', 'del', 'delete', 'delete account'}:
            users.delete_user()
        elif choice in {'l', 'login', 'log in'}:
            users.login()
        elif choice in {'q', 'quit', 'exit'}:
            break
        else:
            print("Invalid selection")
print('Thank you for using rental property calculator!')