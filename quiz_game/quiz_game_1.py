print("welcome to quiz")
print("do you want to play the game? answer in 'Yes' or 'No' ")

play_game = input()

def game():
    print("what does CPU stands for?")
    ans = input()
    if ans.lower() == 'central processing unit':
        print("Congratulations that is a correct answer")
    else:
        print("Unfortunately that is a wrong answer")
        print("the correct answer is Central Processing Unit")


if play_game.lower() == 'yes':
    print("Awesome let's Start the game")
    game()
else :
    print("Sorry to hear that.. see you soon")


