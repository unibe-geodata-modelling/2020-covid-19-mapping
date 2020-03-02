#Exercise 3
#import random
import random
#create random number r
r=random.randint(0,100)
print("A random number between 0 and 100 has been generated!")
u=int(input("Choose a random number between 0 and 100: "))
guesses=1
while u != r:
    if u < r:
        u=int(input("The number is actually higher, make another guess: "))
        print(u)
        guesses=guesses+1
    else:
        u = int(input("The number is actually lower, make another guess: "))
        print(u)
        guesses=guesses+1
print("Congratulations, the number was {} and it only took you {} guesses to figure it out!".format(r,guesses))

