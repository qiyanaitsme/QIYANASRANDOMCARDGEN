from flask import Flask, request, render_template
import random

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-cards', methods=['POST'])
def generate_cards():
    bin_number = request.form.get('bin')
    expiry_date = request.form.get('expiry')
    cvv = request.form.get('cvv')
    quantity = int(request.form.get('quantity'))

    cards = []
    for _ in range(quantity):
        card_number = generate_credit_card(bin_number)
        valid = luhn_algorithm(card_number)
        cards.append((card_number, expiry_date, cvv, valid))

    return render_template('cards.html', cards=cards)

def generate_credit_card(bin_number):
    card_number = bin_number + ''.join(str(random.randint(0, 9)) for _ in range(12))

    while is_duplicate(card_number):
        card_number = bin_number + ''.join(str(random.randint(0, 9)) for _ in range(12))
    return card_number

def luhn_algorithm(card_number):
    card_number = [int(x) for x in str(card_number)]
    check_digit = card_number.pop()

    card_number.reverse()

    for i in range(0, len(card_number), 2):
        card_number[i] *= 2
        if card_number[i] > 9:
            card_number[i] -= 9

    return (sum(card_number) + check_digit) % 10 == 0

def is_duplicate(card_number):
    return random.randint(0, 1) == 1

if __name__ == "__main__":
    app.run(debug=True)