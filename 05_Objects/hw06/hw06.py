############
# Mutation #
############

def make_withdraw(balance, password):
    """Return a password-protected withdraw function.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> w(90, 'hax0r')
    'Insufficient funds'
    >>> w(25, 'hwat')
    'Incorrect password'
    >>> w(25, 'hax0r')
    50
    >>> w(75, 'a')
    'Incorrect password'
    >>> w(10, 'hax0r')
    40
    >>> w(20, 'n00b')
    'Incorrect password'
    >>> w(10, 'hax0r')
    "Your account is locked. Attempts: ['hwat', 'a', 'n00b']"
    >>> w(10, 'l33t')
    "Your account is locked. Attempts: ['hwat', 'a', 'n00b']"
    """
    incorrect_passwords = []
    locked = False

    def withraw(amount, word):
        nonlocal balance
        nonlocal incorrect_passwords
        nonlocal locked
        MAX_INCORRECT_PASSWORDS = 3
        if word == password and not locked:
            if amount <= balance:
                balance = balance - amount
                return balance
            else:
                return "Insufficient funds"
        elif locked:
            return "Your account is locked. Attempts: " + str(incorrect_passwords)
        else:
            incorrect_passwords.append(word)
            locked = len(incorrect_passwords) == MAX_INCORRECT_PASSWORDS
            return "Incorrect password"

    return withraw


def make_joint(withdraw, old_password, new_password):
    """Return a password-protected withdraw function that has joint access to
    the balance of withdraw.

    >>> w = make_withdraw(100, 'hax0r')
    >>> w(25, 'hax0r')
    75
    >>> make_joint(w, 'my', 'secret')
    'Incorrect password'
    >>> j = make_joint(w, 'hax0r', 'secret')
    >>> w(25, 'secret')
    'Incorrect password'
    >>> j(25, 'secret')
    50
    >>> j(25, 'hax0r')
    25
    >>> j(100, 'secret')
    'Insufficient funds'

    >>> j2 = make_joint(j, 'secret', 'code')
    >>> j2(5, 'code')
    20
    >>> j2(5, 'secret')
    15
    >>> j2(5, 'hax0r')
    10

    >>> j2(25, 'password')
    'Incorrect password'
    >>> j2(5, 'secret')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> j(5, 'secret')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> w(5, 'hax0r')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    >>> make_joint(w, 'hax0r', 'hello')
    "Your account is locked. Attempts: ['my', 'secret', 'password']"
    """
    def joint_withdraw(amount, password_attempt):
        if password_attempt == new_password:
            return withdraw(amount, old_password)
        return withdraw(amount, password_attempt)

    creation_result = withdraw(0, old_password)
    if type(creation_result) == str:
        return creation_result
    else:
        return joint_withdraw


###########
# Objects #
###########

class VendingMachine:
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Machine is out of stock.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'You must deposit $10 more.'
    >>> v.deposit(7)
    'Current balance: $7'
    >>> v.vend()
    'You must deposit $3 more.'
    >>> v.deposit(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.deposit(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.deposit(15)
    'Machine is out of stock. Here is your $15.'

    >>> w = VendingMachine('soda', 2)
    >>> w.restock(3)
    'Current soda stock: 3'
    >>> w.deposit(2)
    'Current balance: $2'
    >>> w.vend()
    'Here is your soda.'
    """
    def __init__(self, item, item_price):
        self.item = item
        self.item_price = item_price
        self.stock = 0
        self.balance = 0

    def vend(self):
        if self.stock > 0 and self.balance >= self.item_price:
            self.balance -= self.item_price
            change = self.balance
            self.balance = 0
            if change > 0:
                return "Here is your " + str(self.item) + \
                    " and $" + str(change) + " change."
            else:
                return "Here is your " + str(self.item) + "."
        elif self.stock <= 0:
            return "Machine is out of stock."
        else:
            return "You must deposit $" + \
                str(self.item_price - self.balance) + " more."

    def restock(self, quantity):
        self.stock += quantity
        return "Current " + str(self.item) + " stock: " + str(self.stock)

    def deposit(self, amount):
        if self.stock <= 0:
            return "Machine is out of stock. Here is your $" + str(amount) + "."
        else:
            self.balance += amount
            return "Current balance: $" + str(self.balance)



class MissManners:
    """A container class that only forward messages that say please.

    >>> v = VendingMachine('teaspoon', 10)
    >>> v.restock(2)
    'Current teaspoon stock: 2'

    >>> m = MissManners(v)
    >>> m.ask('vend')
    'You must learn to say please first.'
    >>> m.ask('please vend')
    'You must deposit $10 more.'
    >>> m.ask('please deposit', 20)
    'Current balance: $20'
    >>> m.ask('now will you vend?')
    'You must learn to say please first.'
    >>> m.ask('please hand over a teaspoon')
    'Thanks for asking, but I know not how to hand over a teaspoon.'
    >>> m.ask('please vend')
    'Here is your teaspoon and $10 change.'

    >>> double_fussy = MissManners(m) # Composed MissManners objects
    >>> double_fussy.ask('deposit', 10)
    'You must learn to say please first.'
    >>> double_fussy.ask('please deposit', 10)
    'Thanks for asking, but I know not how to deposit.'
    >>> double_fussy.ask('please please deposit', 10)
    'Thanks for asking, but I know not how to please deposit.'
    >>> double_fussy.ask('please ask', 'please deposit', 10)
    'Current balance: $10'
    """
    def __init__(self, obj):
        self.obj = obj

    def ask(self, message, *args):
        magic_word = 'please '
        if not message.startswith(magic_word):
            return 'You must learn to say please first.'
        else:
            words = message.split()[1:]
            words_and_spaces = [word + " " for word in words]
            attr = "".join(words_and_spaces)
            attr = attr[:len(attr) - 1]
            if hasattr(self.obj, attr):
                command = getattr(self.obj, attr)
                return command(*args)
            else:
                return  "Thanks for asking, but I know not how to " + attr + "."
