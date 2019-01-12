def newBlockchain():
    amt = int(input('insert amount: '))
    if (len(blockchain) < 1):
        blockchain.append([amt])
    else:
        blockchain.append([blockchain[-1], amt])

def printBlockchain():
    print(blockchain)

def valid():
    is_valid = True
    i = 0
    for block in blockchain:
        if i != 0:
            print(i)
            if (block[0] != blockchain[i-1]):
                is_valid = False
        i += 1

    return is_valid

blockchain = []

isWorking = True

while isWorking:
    userChoice = input('User choice: ')

    if (userChoice == '1'):
        newBlockchain()
    elif (userChoice == '2'):
        printBlockchain()
    elif (userChoice == 'h'):
        blockchain[0] = [2]
    elif (userChoice == 'q'):
        isWorking = False

    if not valid():
        print('blockchain not valid!!!')
        break
    else:
        print('valid')
