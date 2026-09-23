# simple while loop with user input

answer = input("Type y for yes, or n for no")

while (answer == 'y'):
  print("Yay, you're in the loop!")
  answer = input("Do you want to continue in the loop? y for yes, or n for no")

print("You're officially out of the loop.")