values = [
    ['cart', 'dev1', '123', 'dev1@1mg.com', 'dev2', '234', 'dev2@1mg.com', 'dev3', '345', 'dev3@1mg.com'],
    ['devops', 'dev2', '234', 'dev2@1mg.com', 'dev3', '345', 'dev3@1mg.com', 'dev4', '456', 'dev4@1mg.com'],
    ['merch', 'dev3', '345', 'dev3@1mg.com', 'dev4', '456', 'dev4@1mg.com', 'dev5', '567', 'dev5@1mg.com'],
    ['pharma', 'dev4', '456', 'dev4@1mg.com', 'dev5', '567', 'dev5@1mg.com', 'dev6', '678', 'dev6@1mg.com'],
    ['labs', 'dev5', '567', 'dev5@1mg.com', 'dev6', '678', 'dev6@1mg.com', 'dev7', '789', 'dev7@1mg.com'],
    ['fulfillment', 'dev6', '678', 'dev6@1mg.com', 'dev7', '789', 'dev7@1mg.com', 'dev8', '900', 'dev8@1mg.com'],
    ['payments', 'dev7', '789', 'dev7@1mg.com', 'dev8', '900', 'dev8@1mg.com', 'dev9', '1011', 'dev9@1mg.com']
]

team_name = 'xyz'

if team_name:
    if team_name != 'all':
        values = [row for row in values if row[0] == team_name]
        if not values:
            message = 'Invalid Team Name! Please check from https://docs.google.com/spreadsheets/d/1iMxqOcGNqflEmSdOCsubryoH7El7cWKTxvK2wUy5QsM/edit?usp=sharing'
            print(message)

    # Format the on-call information as a message
    message = 'Current On-Call:'
    for row in values:
        team = row[0]
        l1_dev = row[1]
        l1_contact = row[2] + ', ' + row[3]
        l2_dev = row[4]
        l2_contact = row[5] + ', ' + row[6]
        l3_dev = row[7]
        l3_contact = row[8] + ', ' + row[9]
        message += f'\n\nTeam: {team}\nL1: {l1_dev} ({l1_contact})\nL2: {l2_dev} ({l2_contact})\nL3: {l3_dev} ({l3_contact})'
        message += '\n\n For discrepancies, please edit here: https://docs.google.com/spreadsheets/d/1iMxqOcGNqflEmSdOCsubryoH7El7cWKTxvK2wUy5QsM/edit?usp=sharing'

else:
    message = ''

print(message)
