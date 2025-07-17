#this is a programme that makes a palindrome of a word.

# a=str(input("Enter a word "))
# def backward(a):
#     if a ==a[::-1]:
#         print("Yes it is the palindrome")
#     else:
#         print("Try again")
#   Request input of  a word from user
#  Create a function and pass in the input as a parameter
#  create a variable and assign it to the reversed form of input using slicing
#   Palindrome will be formed when the variable is equal to our input.
# Display output.

def backword(a):
    a=str(input("Enter a word")) 
    pal=a[::-1]
    if a==pal:
        print("Yayy!you have found the palindrome")
    else:
        print("Try another word")
   
                                     #yes it wil display a word but in its pl form but not all words are palindromes
#create a function and pass in a paramter
#Request for user to enter a number three times 
#Append the three times to an empty list
#create another empty list and assign it the reverse of the first list 
#if the two lists are the same,it is the palindrome
#end function.

def palnumb(z):
    p=int(input("Enter a number "))
    z=int(input("Enter another number "))
    y=int(input("Enter another number "))
    new=[]
    new=[new.append(p),new.append(z),new.append(y)]
    people=new.reverse()
    if people==new:
        print("Yay you have got the palindrome")
    else:
        print("Try again")


