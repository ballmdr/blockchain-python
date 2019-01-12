import numpy as np

blockchain = []

def get_last_blockchain():
    return blockchain[-1]

def add_value(transaction_amount, last_transaction=np.random.randint(100)):
    blockchain.append([last_transaction, transaction_amount])
    print(blockchain)

tx_amount = int(input('Your transaction amount: '))
add_value(tx_amount)
add_value(last_transaction=get_last_blockchain(), transaction_amount=np.random.randint(100))
add_value(np.random.randint(100), get_last_blockchain())
add_value(3021, last_transaction=get_last_blockchain())

