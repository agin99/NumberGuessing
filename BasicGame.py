import random

while True:
    user_input = input("Choose a difficulty level:\n1. Easy (10)\n2. Medium (100)\n3. Hard (1000)\n\n")
    try:
        difficulty_choice = int(user_input)
        if difficulty_choice < 1 or difficulty_choice > 3:
            raise ValueError("Must choose a value corresponding to the difficulty level.")
        break
    except ValueError:
        print(f"Must input an integer, your input {user_input}.")
random_number = int(random.random() * 10**(difficulty_choice) // 1)
print(random_number)
max_turns = 10
player_guess = 0
turns = 0
distance = 0
while player_guess != random_number:
    if turns > 1:
        if distance > abs(random_number - player_guess):
            print("Warmer")
        else:
            print("Colder")
    distance = abs(random_number - player_guess)
    
    while True:
        user_input = input("Guess a number: ")
        try:
            player_guess = int(user_input)
            break
        except ValueError:
            print(f"Must input an integer, your input {user_input}.")
    turns += 1
    if turns == 10:
        break
    if(player_guess > random_number):
        print("Too high!")
    elif(player_guess < random_number):
        print("Too low!")

if player_guess == random_number:
    print(f"You win. You guessed {player_guess} in {turns} turns.")
else:
    print(f"You lose. You exceeded the maximum of {max_turns} turns.\nThe correct number was {random_number}.")