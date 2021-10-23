import discord
import random

client = discord.Client()
roll = 1  #  global variable for storing how many rolls have been used (I think it's easiest to use a global variable)
#  varaibles for the dice
d1 = 0
d2 = 0
d3 = 0
d4 = 0
d5 = 0
d1_keep = 0  #  0 is if the dice was not kept and is free to be rolled, 1 if it is kept
d2_keep = 0
d3_keep = 0
d4_keep = 0
d5_keep = 0  
#  variables for the scores - if they are set to -1, they haven't been scored for yet
ones = -1
twos = -1
threes = -1
fours = -1
fives = -1
sixes = -1
upper_1 = 0
upper_bonus = 0
upper_total = 0
three_kind = -1
four_kind = -1
full_house = -1
sm_straight = -1
lg_straight = -1
yahtzee = -1
chance = -1
yahtzee_bonus = -1
lower_total = 0
grand_total = 0

def check_two(arr, big):  #  used for checking for full house
    if big != 1:  #  big variable is used to make sure we don't count the upper part of the full house as the lower part
        if arr.count(1) >= 2:
            return 1
    if big != 2:
        if arr.count(2) >= 2:
            return 1
    if big != 3: 
        if arr.count(3) >= 2:
            return 1
    if big != 4:
        if arr.count(4) >= 2:
            return 1
    if big != 5:
        if arr.count(5) >= 2:
            return 1
    if big != 6:
        if arr.count(6) >= 2:
            return 1
    return 0

def check_three(arr):
    if arr.count(1) >= 3:  #  we check if there are 3 1's rolled and if not, check the other possible values for dice
        return 1
    elif arr.count(2) >= 3:
        return 1
    elif arr.count(3) >= 3:
        return 1
    elif arr.count(4) >= 3:
        return 1
    elif arr.count(5) >= 3:
        return 1
    elif arr.count(6) >= 3:
        return 1
    else:
        return 0

def check_four(arr):
    if arr.count(1) >= 4:
        return 1
    elif arr.count(2) >= 4:
        return 1
    elif arr.count(3) >= 4:
        return 1
    elif arr.count(4) >= 4:
        return 1
    elif arr.count(5) >= 4:
        return 1
    elif arr.count(6) >= 4:
        return 1
    else:
        return 0

def check_full(arr):
    if arr.count(1) == 3:  #  check for the 3 of a kind, then pass to function to check for 2 of kind, which needs which dice was the 3 of a kind
        if check_two(arr, 1) == 1:
            return 1
    elif arr.count(2) == 3:
        if check_two(arr, 2) == 1:
            return 1
    elif arr.count(3) == 3:
        if check_two(arr, 3) == 1:
            return 1
    elif arr.count(4) == 3:
        if check_two(arr, 4) == 1:
            return 1
    elif arr.count(5) == 3:
        if check_two (arr, 5) == 1:
            return 1
    elif arr.count(6) == 3:
        if check_two(arr, 6) == 1:
            return 1
    else:
        return 0

def check_sm(arr):  # we literally just check if the numbers required for every version of a small straight are present in the dice
    if 1 in arr and 2 in arr and 3 in arr and 4 in arr:
        return 1
    elif 2 in arr and 3 in arr and 4 in arr and 5 in arr:
        return 1
    elif 3 in arr and 4 in arr and 5 in arr and 6 in arr:
        return 1
    else:
        return 0

def check_lg(arr):
    if 1 in arr and 2 in arr and 3 in arr and 4 in arr and 5 in arr:
        return 1
    elif 2 in arr and 3 in arr and 4 in arr and 5 in arr and 6 in arr:
        return 1
    else:
        return 0

def check_yahtzee(arr):
    if arr.count(1) == 5:
        return 1
    elif arr.count(2) == 5:
        return 1
    elif arr.count(3) == 5:
        return 1
    elif arr.count(4) == 5:
        return 1
    elif arr.count(5) == 5:
        return 1
    elif arr.count(6) == 5:
        return 1
    else:
        return 0

def check_all():
    v = 1  # if any category hasn't been scored, returns 0 for false, otherwise returns 1 for true
    if ones == -1:
        v = 0
    elif twos == -1:
        v = 0
    elif threes == -1:
        v = 0
    elif fours == -1:
        v = 0
    elif fives == -1:
        v = 0
    elif sixes == -1:
        v = 0
    elif three_kind == -1:
        v = 0
    elif four_kind == -1:
        v = 0
    elif full_house == -1:
        v = 0
    elif sm_straight == -1:
        v = 0
    elif lg_straight == -1:
        v = 0
    elif yahtzee == -1:
        v = 0
    elif chance == -1:
        v = 0
    return v

@client.event
async def on_ready():
    try:
        print('Logged in as {0.user}'.format(client))
    except:
        print("Could not login")

@client.event
async def on_message(message):
    if message.author == client.user:  #  so we don't respond to our own messages- we shouldn't but just in case
        return
    if message.content.startswith("!help"):  #  if they want a list of the functions of the bot
        await message.channel.send("Bot for playing Yahtzee (currently just 1 player)")
        await message.channel.send("!roll to roll your dice")
        await message.channel.send("!keep to keep certain dice")
        await message.channel.send("each dice will have to be a separate command (i.e. !keep d1 and !keep d2 to keep the first two dice")
        await message.channel.send("the dice you keep will stay kept between rolls, use !unkeep to remove the hold on them")
        await message.channel.send("!list to list the dice you have rolled this turn")
        await message.channel.send("!take to take the dice for a certain score")
        await message.channel.send("if you want to know the syntax for taking for a specific category, use !cat")
        await message.channel.send("!zero to take a zero for a specific category")
        await message.channel.send("!score to list your current scoreboard")
        await message.channel.send("!end to finish the game and to print out your final score")
    elif message.content.startswith("!roll"):  #  if the player wants to roll their dice
        global roll, d1_keep, d2_keep, d3_keep, d4_keep, d5_keep, d1, d2, d3, d4, d5
        if roll == 1:  #  if this is the first roll of the player's turn
            d1 = random.randint(1,6)
            d2 = random.randint(1,6)
            d3 = random.randint(1,6)
            d4 = random.randint(1,6)
            d5 = random.randint(1,6)
            await message.channel.send("You have rolled: " + str(d1) + ", " + str(d2) + ", " + str(d3) + ", " + str(d4) + ", " + str(d5))
            roll = roll + 1
        elif roll == 2:  # if this is the second roll of the player's turn
            print_str = ""
            if d1_keep == 0:  
                d1 = random.randint(1,6)
            if d2_keep == 0:  
                d2 = random.randint(1,6)
            if d3_keep == 0:  
                d3 = random.randint(1,6)
            if d4_keep == 0:  
                d4 = random.randint(1,6)
            if d5_keep == 0:  
                d5 = random.randint(1,6)
            await message.channel.send("The dice you have are: " + str(d1) + ", " + str(d2) + ", " + str(d3) + ", " + str(d4) + ", " + str(d5))
            if d1_keep == 1:
                print_str += "dice 1, "
            if d2_keep == 1:
                print_str += "dice 2, "
            if d3_keep == 1:
                print_str += "dice 3, "
            if d4_keep == 1:
                print_str += "dice 4, "
            if d5_keep == 1:
                print_str += "dice 5"
            await message.channel.send("The dice you are keeping are: " + print_str)  #  reminding the player which dice they are keeping
            roll = roll + 1
        elif roll == 3:  # if this is the final roll of the player's turn
            if d1_keep == 0:  
                d1 = random.randint(1,6)
            if d2_keep == 0:  
                d2 = random.randint(1,6)
            if d3_keep == 0:  
                d3 = random.randint(1,6)
            if d4_keep == 0:  
                d4 = random.randint(1,6)
            if d5_keep == 0:  
                d5 = random.randint(1,6)
            await message.channel.send("The dice you have are: " + str(d1) + ", " + str(d2) + ", " + str(d3) + ", " + str(d4) + ", " + str(d5))
            roll = 0  #  setting this so they cannot roll again
        elif roll == 0:  #  if they have already rolled the maximum amount of times
            await message.channel.send("You have already rolled the maximum amount of times this turn, please choose how you will score")
            await message.channel.send("The dice you have are: " + str(d1) + ", " + str(d2) + ", " + str(d3) + ", " + str(d4) + ", " + str(d5))
    elif message.content.startswith("!keep"):  #  if the player wants to keep a die
        kept = message.content  #  stripping down to the desired dice
        kept = kept.replace("!keep", "")
        kept = kept.strip()
        if kept == "d1":
            d1_keep = 1
            await message.channel.send("You have decided to keep dice 1, which has a value of " + str(d1))
        if kept == "d2":
            d2_keep = 1
            await message.channel.send("You have decided to keep dice 2, which has a value of " + str(d2))
        if kept == "d3":
            d3_keep = 1
            await message.channel.send("You have decided to keep dice 3, which has a value of " + str(d3))
        if kept == "d4":
            d4_keep = 1
            await message.channel.send("You have decided to keep dice 4, which has a value of " + str(d4))
        if kept == "d5":
            d5_keep = 1
            await message.channel.send("You have decided to keep dice 5, which has a value of " + str(d5))
        print_str = ""
        if d1_keep == 1:
            print_str += "dice 1, "
        if d2_keep == 1:
            print_str += "dice 2, "
        if d3_keep == 1:
            print_str += "dice 3, "
        if d4_keep == 1:
            print_str += "dice 4, "
        if d5_keep == 1:
            print_str += "dice 5"
        await message.channel.send("The dice you are keeping are: " + print_str)
    elif message.content.startswith("!unkeep"):  #  if the player wants to not keep a die
        kept = message.content  #  stripping down to the desired dice
        kept = kept.replace("!unkeep", "")
        kept = kept.strip()
        if kept == "d1":
            d1_keep = 0
            await message.channel.send("You have decided not to keep dice 1, which has a value of " + str(d1))
        if kept == "d2":
            d2_keep = 0
            await message.channel.send("You have decided not to keep dice 2, which has a value of " + str(d2))
        if kept == "d3":
            d3_keep = 0
            await message.channel.send("You have decided not to keep dice 3, which has a value of " + str(d3))
        if kept == "d4":
            d4_keep = 0
            await message.channel.send("You have decided not to keep dice 4, which has a value of " + str(d4))
        if kept == "d5":
            d5_keep = 0
            await message.channel.send("You have decided not to keep dice 5, which has a value of " + str(d5))
        print_str = ""
        if d1_keep == 1:
            print_str += "dice 1, "
        if d2_keep == 1:
            print_str += "dice 2, "
        if d3_keep == 1:
            print_str += "dice 3, "
        if d4_keep == 1:
            print_str += "dice 4, "
        if d5_keep == 1:
            print_str += "dice 5"
        await message.channel.send("The dice you are keeping are: " + print_str)
    elif message.content.startswith("!list"):  #  if the player wants to list the dice they have currently
        await message.channel.send("The dice you have are: " + str(d1) + ", " + str(d2) + ", " + str(d3) + ", " + str(d4) + ", " + str(d5))
        print_str = ""
        if d1_keep == 1:
            print_str += "dice 1, "
        if d2_keep == 1:
            print_str += "dice 2, "
        if d3_keep == 1:
            print_str += "dice 3, "
        if d4_keep == 1:
            print_str += "dice 4, "
        if d5_keep == 1:
            print_str += "dice 5"
        await message.channel.send("The dice you are keeping are: " + print_str)
    elif message.content.startswith("!cat"):  #  if the player wants to know how to take specific categories
        await message.channel.send("To keep for ones, use !take ones")
        await message.channel.send("To keep for twos, use !take twos")
        await message.channel.send("To keep for threes, use !take threes")
        await message.channel.send("To keep for fours, use !take fours")
        await message.channel.send("To keep for fives, use !take fives")
        await message.channel.send("To keep for sixes, use !take sixes")
        await message.channel.send("To keep for 3 of a kind, use !take 3kind")
        await message.channel.send("To keep for 4 of a kind, use !take 4kind")
        await message.channel.send("To keep for Full House, use !take house or !take full")
        await message.channel.send("To keep for Small Straight, use !take small")
        await message.channel.send("To keep for Large Straight, use !take large")
        await message.channel.send("To keep for YAHTZEE, use !take yahtzee (this will auto assign to YAHTZEE bonus if you have already rolled a yahtzee)")
        await message.channel.send("To keep for Chance, use !take chance")
        await message.channel.send("The totals for the upper and lower sections will automatically be populated as will be the bonus for the upper section")
        await message.channel.send("The syntax is the same for taking a 0, just use !zero instead of !take")
    elif message.content.startswith("!take"):  #  if the player wants to take the dice for a specific score
        global ones, twos, threes, fours, fives, sixes, upper_1, three_kind, four_kind, full_house, sm_straight, lg_straight, yahtzee, yahtzee_bonus, chance, lower_total
        category = message.content  #  splitting down to the part we want
        category = category.replace("!take", "")
        category = category.strip()
        sub_total = 0
        if category == 'ones':
            if ones == -1:  #  if ones haven't already been scored
                if d1 == 1:
                    sub_total += 1
                if d2 == 1:
                    sub_total += 1
                if d3 == 1:
                    sub_total += 1
                if d4 == 1:
                    sub_total += 1
                if d5 == 1:
                    sub_total += 1
                ones = sub_total  #  we store the total amount of ones and then we reset the dice that were being kept for the next roll
                upper_1 += sub_total
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have scored " + str(sub_total) + " for the ones category")
            else:  #  if there is already a score for the ones
                await message.channel.send("You have already scored in your ones category")
        elif category == 'twos':
            if twos == -1:
                if d1 == 2:
                    sub_total += 2
                if d2 == 2:
                    sub_total += 2
                if d3 == 2:
                    sub_total += 2
                if d4 == 2:
                    sub_total += 2
                if d5 == 2:
                    sub_total += 2
                twos = sub_total
                upper_1 += sub_total
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have scored " + str(sub_total) + " for the twos category")
            else:
                await message.channel.send("You have already scored in your twos category")
        elif category == 'threes':
            if threes == -1:
                if d1 == 3:
                    sub_total += 3
                if d2 == 3:
                    sub_total += 3
                if d3 == 3:
                    sub_total += 3
                if d4 == 3:
                    sub_total += 3
                if d5 == 3:
                    sub_total += 3
                threes = sub_total
                upper_1 += sub_total
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have scored " + str(sub_total) + " for the threes category")
            else:
                await message.channel.send("You have already scored in your threes category")
        elif category == 'fours':
            if fours == -1:
                if d1 == 4:
                    sub_total += 4
                if d2 == 4:
                    sub_total += 4
                if d3 == 4:
                    sub_total += 4
                if d4 == 4:
                    sub_total += 4
                if d5 == 4:
                    sub_total += 4
                fours = sub_total
                upper_1 += sub_total
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have scored " + str(sub_total) + " for the fours category")
            else:
                await message.channel.send("You have already scored in your fours category")
        elif category == 'fives':
            if fives == -1:
                if d1 == 5:
                    sub_total += 5
                if d2 == 5:
                    sub_total += 5
                if d3 == 5:
                    sub_total += 5
                if d4 == 5:
                    sub_total += 5
                if d5 == 5:
                    sub_total += 5
                fives = sub_total
                upper_1 += sub_total
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have scored " + str(sub_total) + " for the fives category")
            else:
                await message.channel.send("You have already scored in your fives category")
        elif category == 'sixes':
            if sixes == -1:
                if d1 == 6:
                    sub_total += 6
                if d2 == 6:
                    sub_total += 6
                if d3 == 6:
                    sub_total += 6
                if d4 == 6:
                    sub_total += 6
                if d5 == 6:
                    sub_total += 6
                sixes = sub_total
                upper_1 += sub_total
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have scored " + str(sub_total) + " for the sixes category")
            else:
                await message.channel.send("You have already scored in your sixes category")
        elif category == "3kind":
            if three_kind == -1:
                arr = [d1,d2,d3,d4,d5]  #  store the dice into an array and pass it to a function to check if there's actually a 3 of a kind
                count = check_three(arr)
                if count == 1:
                    total = d1 + d2 + d3 + d4 + d5
                    three_kind = total
                    lower_total += total
                    d1_keep = 0
                    d2_keep = 0
                    d3_keep = 0
                    d4_keep = 0
                    d5_keep = 0
                    roll = 1
                    await message.channel.send("You have scored " + str(total) + " for the 3 of a kind category")
                else:
                    await message.channel.send("That is not 3 of a kind")
            else:
                await message.channel.send("You have already scored in your 3 of a kind category")
        elif category == "4kind":
            if four_kind == -1:
                arr = [d1,d2,d3,d4,d5]
                count = check_four(arr)
                if count == 1:
                    total = d1 + d2 + d3 + d4 +d5
                    four_kind = total
                    lower_total += total
                    d1_keep = 0
                    d2_keep = 0
                    d3_keep = 0
                    d4_keep = 0
                    d5_keep = 0
                    roll = 1
                    await message.channel.send("You have scored " + str(total) + " for the 4 of a kind category")
                else:
                    await message.channel.send("That is not 4 of a kind")
            else:
                await message.channel.send("You have already scored in your 4 of a kind category")
        elif category == "house" or category == "full":
            if full_house == -1:
                arr = [d1,d2,d3,d4,d5]
                count = check_full(arr)
                if count == 1:
                    full_house = 25
                    lower_total += 25
                    d1_keep = 0
                    d2_keep = 0
                    d3_keep = 0
                    d4_keep = 0
                    d5_keep = 0
                    roll = 1
                    await message.channel.send("You have scored 25 for the Full House category")
                else:
                    await message.channel.send("That is not a Full House")
            else:
                await message.channel.send("You have already scored in your Full House category")
        elif category == "small":
            if sm_straight == -1:
                arr = [d1,d2,d3,d4,d5]
                count = check_sm(arr)
                if count == 1:
                    sm_straight = 30
                    lower_total += 30
                    d1_keep = 0
                    d2_keep = 0
                    d3_keep = 0
                    d4_keep = 0
                    d5_keep = 0
                    roll = 1
                    await message.channel.send("You have scored 30 for the Small Straight category")
                else:
                    await message.channel.send("That is not a Small Straight")
            else:
                await message.channel.send("You have already scored in your Small Straight category")
        elif category == "large":
            if lg_straight == -1:
                arr = [d1,d2,d3,d4,d5]
                count = check_lg(arr)
                if count == 1:
                    lg_straight = 40
                    lower_total += 40
                    d1_keep = 0
                    d2_keep = 0
                    d3_keep = 0
                    d4_keep = 0
                    d5_keep = 0
                    roll = 1
                    await message.channel.send("You have scored 40 for the Large Straight category")
                else:
                    await message.channel.send("That is not a Large Straight")
            else:
                await message.channel.send("You have already scored in your Large Straight category")
        elif category == "yahtzee":
            if yahtzee == -1:  #  if there hasn't been a yahtzee
                arr = [d1,d2,d3,d4,d5]
                count = check_yahtzee(arr)
                if count == 1:
                    yahtzee = 50
                    lower_total += 50
                    d1_keep = 0
                    d2_keep = 0
                    d3_keep = 0
                    d4_keep = 0
                    d5_keep = 0
                    roll = 1
                    await message.channel.send("You have scored 50 for the YAHTZEE category")
                else:
                    await message.channel.send("That is not a YAHTZEE")
            elif yahtzee_bonus > 300 and yahtzee_bonus != 0:  #  if there's still yahtzee bonus points left over and there hasn't been a 0 taken for yahtzee
                arr = [d1,d2,d3,d4,d5]
                count = check_yahtzee(arr)
                if count == 1:
                    yahtzee_bonus += 100
                    lower_total += 100
                    d1_keep = 0
                    d2_keep = 0
                    d3_keep = 0
                    d4_keep = 0
                    d5_keep = 0
                    roll = 1
                    await message.channel.send("You have scored 100 for the YAHTZEE BONUS category")
                else:
                    await message.channel.send("That is not a YAHTZEE")
            else:  #  somehow the player got 4 yahtzees
                await message.channel.send("You have already scored every yahtzee that you are allowed to")
        elif category == "chance":
            if chance == -1:
                total = d1 + d2 + d3 + d4 + d5  # don't need to verify anything for chance
                chance = total
                lower_total += total
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have scored " + str(total) + " for the Chance category")
            else:
                await message.channel.send("You have already scored in your Chance category")
    elif message.content.startswith("!zero"):  #  if the player wants to take a 0 for a category
        category = message.content  #  splitting down to the part we want
        category = category.replace("!zero", "")
        category = category.strip()
        if category == "ones":
            if ones == -1:  #  if the category hasn't already been scored for
                ones = 0
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have taken a 0 for ones")
            else:  #  if the category already has a score
                await message.channel.send("You have already scored for ones")
        elif category == "twos":
            if twos == -1:  #  if the category hasn't already been scored for
                twos = 0
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have taken a 0 for twos")
            else:  #  if the category already has a score
                await message.channel.send("You have already scored for twos")
        elif category == "threes":
            if threes == -1:  #  if the category hasn't already been scored for
                threes = 0
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have taken a 0 for threes")
            else:  #  if the category already has a score
                await message.channel.send("You have already scored for threes")
        elif category == "fours":
            if fours == -1:  #  if the category hasn't already been scored for
                fours = 0
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have taken a 0 for fours")
            else:  #  if the category already has a score
                await message.channel.send("You have already scored for fours")
        elif category == "fives":
            if fives == -1:  #  if the category hasn't already been scored for
                fives = 0
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have taken a 0 for fives")
            else:  #  if the category already has a score
                await message.channel.send("You have already scored for fives")
        elif category == "sixes":
            if sixes == -1:  #  if the category hasn't already been scored for
                sixes = 0
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have taken a 0 for sixes")
            else:  #  if the category already has a score
                await message.channel.send("You have already scored for sixes")
        elif category == "3kind":
            if three_kind == -1:  #  if the category hasn't already been scored for
                three_kind = 0
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have taken a 0 for 3 of a kind")
            else:  #  if the category already has a score
                await message.channel.send("You have already scored for 3 of a kind")
        elif category == "4kind":
            if four_kind == -1:  #  if the category hasn't already been scored for
                four_kind = 0
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have taken a 0 for 4 of a kind")
            else:  #  if the category already has a score
                await message.channel.send("You have already scored for 4 of a kind")
        elif category == "house" or category == "full":
            if full_house == -1:  #  if the category hasn't already been scored for
                full_house = 0
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have taken a 0 for Full House")
            else:  #  if the category already has a score
                await message.channel.send("You have already scored for Full House")
        elif category == "small":
            if sm_straight == -1:  #  if the category hasn't already been scored for
                sm_straight = 0
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have taken a 0 for Small Straight")
            else:  #  if the category already has a score
                await message.channel.send("You have already scored for Small Straight")
        elif category == "large":
            if lg_straight == -1:  #  if the category hasn't already been scored for
                lg_straight = 0
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have taken a 0 for Large Straight")
            else:  #  if the category already has a score
                await message.channel.send("You have already scored for Large Straight")
        elif category == "yahtzee":
            if yahtzee == -1:  #  if the category hasn't already been scored for
                yahtzee = 0
                yahtzee_bonus = 0
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have taken a 0 for YAHTZEE and will not be able to score bonus YAHTZEEs")
            else:  #  if the category already has a score
                await message.channel.send("You have already scored for YAHTZEE")
        elif category == "chance":
            if chance == -1:  #  if the category hasn't already been scored for
                chance = 0
                d1_keep = 0
                d2_keep = 0
                d3_keep = 0
                d4_keep = 0
                d5_keep = 0
                roll = 1
                await message.channel.send("You have taken a 0 for chance")
            else:  #  if the category already has a score
                await message.channel.send("You have already scored for chance")
    elif message.content.startswith("!score"):  #  if the player wants to see their score - maybe will remove all totals for the time being
        print_str = '```'  # begins a code block
        print_str += 'Your score card is currently: \n\n'
        print_str += 'Upper Section: \n'
        if ones != -1:  #  if they haven't been scored, don't mark them as a 0
            print_str += ('Ones: ' + str(ones))
        else:
            print_str += ('Ones: ')
        if twos != -1:
            print_str += ('\nTwos: ' + str(twos))
        else:
            print_str += ('\nTwos: ')
        if threes != -1:
            print_str += ('\nThrees: ' + str(threes))
        else:
            print_str += ('\nThrees: ')
        if fours != -1:
            print_str += ('\nFours: ' + str(fours))
        else:
            print_str += ('\nFours: ')
        if fives != -1:
            print_str += ('\nFives: ' + str(fives))
        else:
            print_str += ('\nFives: ')
        if sixes != -1:
            print_str += ('\nSixes: ' + str(sixes))
        else:
            print_str += ('\nSixes: ')
        print_str += ('\nUpper Total (without bonus): ' + str(upper_1))  #  only listing the first total because the bonus does not need to be calculated until the end
        print_str += '\n\nLower Section: '
        if three_kind != -1:
            print_str += ('\n3 of a kind: ' + str(three_kind))
        else:
            print_str += ('\n3 of a kind: ')
        if four_kind != -1:
            print_str += ('\n4 of a kind: ' + str(four_kind))
        else: 
            print_str += ('\n4 of a kind: ')
        if full_house != -1:
            print_str += ('\nFull House: ' + str(full_house))
        else:
            print_str += ('\nFull House: ')
        if sm_straight != -1:
            print_str += ('\nSmall Straight: ' + str(sm_straight))
        else:
            print_str += ('\nSmall Straight: ')
        if lg_straight != -1:
            print_str += ('\nLarge Straight: ' + str(lg_straight))
        else:
            print_str += ('\nLarge Straight: ')
        if yahtzee != -1:
            print_str += ('\nYAHTZEE: ' + str(yahtzee))
        else:
            print_str += ('\nYAHTZEE: ')
        if chance != -1:
            print_str += ('\nChance: ' + str(chance))
        else:
            print_str += ('\nChance: ')
        if yahtzee_bonus != -1:
            print_str += ('\nYAHTZEE Bonus: ' + str(yahtzee_bonus))
        else:
            print_str += ('\nYAHTZEE Bonus: ')
        print_str += ('\nLower Total: ' + str(lower_total))
        print_str += '\n```'  # ends a code block
        await message.channel.send(print_str)
    elif message.content.startswith("!end"):  #  if the player wants to end the game
        #  need to calculate the upper bonus and total first and then the grand total
        if check_all() == 1:  # if the player has scored for every category
            if upper_1 >= 63:  #  if the player scored high enough to get a bonus
                upper_bonus = 35
                upper_total = upper_1 + upper_bonus
            else:  #  they did not get their bonus
                upper_total = upper_1
            grand_total = upper_total + lower_total
            # need to print everything out
            print_str = '```'  # begins a code block
            print_str += 'Your final score is: \n\n'
            print_str += 'Upper Section: \n'
            print_str += ('Ones: ' + str(ones))
            print_str += ('\nTwos: ' + str(twos))
            print_str += ('\nThrees: ' + str(threes))
            print_str += ('\nFours: ' + str(fours))
            print_str += ('\nFives: ' + str(fives))
            print_str += ('\nSixes: ' + str(sixes))
            print_str += ('\nUpper Total (without bonus): ' + str(upper_1))
            print_str += ('\nBonus for Upper Section: ' + str(upper_bonus))
            print_str += ('\nTotal for Upper Section: ' + str(upper_total))
            print_str += '\n\nLower Section: '
            print_str += ('\n3 of a kind:' + str(three_kind))
            print_str += ('\n4 of a kind: ' + str(four_kind))
            print_str += ('\nFull House: ' + str(full_house))
            print_str += ('\nSmall Straight: ' + str(sm_straight))
            print_str += ('\nLarge Straight: ' + str(lg_straight))
            print_str += ('\nYAHTZEE: ' + str(yahtzee))
            print_str += ('\nChance: ' + str(chance))
            print_str += ('\nYAHTZEE Bonus: ' + str(yahtzee_bonus))
            print_str += ('\nTotal for Lower Section: ' + str(lower_total))
            print_str += ('\n\nGrand Total for the game: ' + str(grand_total))
            print_str += '\n```'  # ends a code block
            await message.channel.send(print_str)
        else:
            await message.channel.send("You have not yet completed the game")

client.run(<your token here>)

#  potential features:
#       adding support for multiple people
