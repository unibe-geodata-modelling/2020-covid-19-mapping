#Exercise 1 and 2 (Homework.)
name = input("Dear user, what is your name? ")
age = int(input ("Dear user, what is your age? "))
nextage = 0
#Inserting the +1 so that a 60 year old gets another ten years
while nextage < age+1:
    nextage = nextage + 10
yearsuntildecade=nextage-age
#Filter children out so they do not have to enter the gender
if age < 18:
    print("{}, in {} years you will be {} years old!".format(name, yearsuntildecade, nextage))
else:
    #Only allow valid (binary) genders
    gender = input ("Please specify your gender: Enter m for male and f for female: ")
    if gender == "f":
        print("Thank you for entering a valid gender input!")
    elif gender == "m":
        print("Thank you for entering a valid gender input!")
    else:
        #Exit code if invalid gender is entered
        print("I am sorry, you chose an invalid gender. You will exit the code immediately. Bye!")
        exit()
    #Filtering between men and women
    if gender == "f":
        print("Dear Mrs. {}, in {} years you will be {} years old!".format(name, yearsuntildecade, nextage))
    else:
        print("Dear Mr. {}, in {} years you will be {} years old!".format(name,yearsuntildecade,nextage))
#Question: How can I make just one line execute?


