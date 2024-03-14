from trainee import db
# method that is used to update a player's specific attribute (i.e. pace or shooting) dependent on the  
# session focus joined 
def update_player_stats(users, sessionFocus, errorPlayers): 
    print(sessionFocus, 'stats updating for ', users)
    
    #table used to relate session focus to player attributes
    focus_column = {
        'Shooting': 'shooting',
        'Passing': 'passing',
        'Dribbling': 'dribbling',
        'Defending': 'defending',
        'Fitness': 'pace',
        'Strength': 'physicality'
    }

    #creates a variable that allows us to interact with Player attributes
    playerAttribute = focus_column.get(sessionFocus)

    for user in users: 
        if user.user_player is None: # if user does not have associated Player object
            errorPlayers.append(user) # store for future use
            continue

        player = user.user_player
        attributeValue = getattr(player, str(playerAttribute)) # retrives attribtue value
        if playerAttribute: # ensures no error
            setattr(player, playerAttribute, attributeValue+3) # updates attribute value