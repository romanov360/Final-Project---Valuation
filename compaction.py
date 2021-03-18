from modules import valuation_module as vm

# The other module does all of the hard work. This model just calls the functions in valuation_module,
# to make the Jupyter Notebook as clean and user-friendly as possible.

def box1():
    
    # When the first box is run, it briefly explains the gist of the stock market, and then
    # prompts the user to click a button. This button, when touched, tells the user
    # which companies they can choose to learn about.
    
    print(vm.info() + '\n\nThat\'s great. Now let\'s choose a company to learn about. Click the button.')
    from IPython.display import display
    import ipywidgets as widgets

    def start_clicked(arg):
        print('\n' + vm.company_names() + '\n\nPick one, don\'t be scared. Then run the next box.\n')

    
    start_button = widgets.Button(description = 'the button')   
    start_button.on_click(start_clicked)
    display(start_button)
    
def box2():
    
    # When run, the Notebook's second box allows the user to input a company of their choosing,
    # after which the company is summarized. Predicting future cash is revealed to be the key to good valuation.
    
    entered_company = input('I choose: ')
    print(vm.summary(entered_company) + '\n\nA wise man once said, a company is worth the money it will make in its lifetime,\
    \nin terms of today\'s dollars. Run the next cell to see the biggest companies on the list.')

def box3():
    
    # The most highly valued companies on the list are revealed.
    
    print(vm.trillionaires() +\
         '\nThanks for checking out my project!\
         \nI hope you learned something about one of the world\'s big, beautiful businesses.')