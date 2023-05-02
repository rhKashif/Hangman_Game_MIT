# Problem Set 2, hangman.py
# Name: Hassan Kashif
# Collaborators: N/A
# Time spent: Unknown

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
# wordlist = load_words()


def is_word_guessed(secret_word_list, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    guess = [] 
    secret_word_list_comp = []
    for i in letters_guessed:
        for j in secret_word_list:
            if i == j and i not in guess:
                guess.append(i)
            if j not in secret_word_list_comp:
                secret_word_list_comp.append(j)
    return (sorted(guess) == sorted(secret_word_list_comp))        #set(secret_word_list).intersection(set(letters_guessed))


# secret_word_list = 'apple'
# letters_guessed = ['a', 'l', 'k', 'p', 'e', 's']
# print(is_word_guessed(secret_word, letters_guessed))


def get_guessed_word(secret_word_list, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guess = []
    flag = False
    for i in secret_word_list:
        for j in letters_guessed:
            if i == j:
                guess.append(i)
                flag = True
                break
            else:
                flag = False
        if flag == False:
            guess.append("_ ")
    print("Guessed Word Progress:", ''.join(guess))
    return guess

# secret_word_list = 'hello'
# letters_guessed = ['e', 'i', 'k', 'p', 'r', 's']
# get_guessed_word(secret_word, letters_guessed)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    all_letters = string.ascii_lowercase
    all_letters_list = list(all_letters)
    not_in_letters_guessed = []
    for i in all_letters_list:
        if i not in letters_guessed:
            not_in_letters_guessed.append(i)
    return print("Available letters: ", ' '.join(not_in_letters_guessed))
        
    
# letters_guessed = ['e', 'i', 'k', 'p', 'r', 's'] 
# get_available_letters(letters_guessed)

def guess_letters(warnings, guesses, letters_guessed, secret_word_list, guess):
    '''
    checks the user input to ensure a letter has been entered
    if a non-letter is entered (number of symbol), the user is loses a warning
    '''
    while warnings > 0 or guesses > 0:
        guessed_letter = input("Please guess a letter: ")
        if guessed_letter in string.ascii_letters:
            if guessed_letter not in letters_guessed:
                letters_guessed.append(guessed_letter.lower())
                break
            elif guessed_letter in letters_guessed:
                print("You have already entered this letter!\n")
        elif guessed_letter.lower() == 'help':
            get_help()
        elif guessed_letter.lower() == 'hint':
            show_possible_matches(guess, guesses, letters_guessed)
        elif guessed_letter.lower() == 'status':
            get_guessed_word(secret_word_list, letters_guessed)
        elif guessed_letter.lower() == 'give up':
            guesses = 0
            break
        else:
            print("You must enter a letter!")
            if warnings != 0:
                warnings -= 1
                print("You have", warnings, "warnings remaining.")
            else:
                guesses -= 1
                print("You have", guesses, "guesses remaining.")
    return guessed_letter, warnings, guesses, letters_guessed

# print(guess_letters(3, 6, [])[3])


def guess_verdict(user_guess, secret_word, guesses, letters_guessed):
    '''
    checks whether the user inputted letter is contained within the secret word
    if not, user loses a guess
    '''
    vowels = ['a', 'e', 'i', 'o', 'u']
    if user_guess not in secret_word:
        print("Oops! That letter is not in my word.")
        if user_guess in vowels:
            guesses -= 2
        else:
            guesses -= 1
    else: 
        print("You guessed correctly!")
    return guesses

def hangman_status(guesses):
    '''
    visual representation of how close the user is to losing
    '''
    if guesses == 5:
        print(" ...... \n .   ..\n O   ..  H\n     ..\n     ..")
    elif guesses == 4:
        print(" ...... \n .   ..\n\O   ..  HA\n     ..\n     ..")
    elif guesses == 3:
        print(" ...... \n .   ..\n\O/  ..  HAN\n     ..\n     ..")
    elif guesses == 2:
        print(" ...... \n .   ..\n\O/  ..  HANG\n |   ..\n     ..")
    elif guesses == 1:
        print(" ...... \n .   ..\n\O/  ..  HANGE\n |   ..\n/    ..")
    elif guesses == 0:
        print(" ...... \n .   ..\n\O/  ..  HANGED\n |   ..\n/ \  ..")
        
def hangman_intro(secret_word, guesses, warnings, wordlist):
    print("Loading word list from file...", 
          len(wordlist), "words loaded.\n\
          \nWelcome to the game Hangman!\
          \nYou have", guesses, " guesses and", warnings, "warnings at the start of the game.\
          \nFollow the instructions on screen or you will be penalised.\
          \nIf you have no warnings remaining and break the rules of the game you will lose a guess.\
          \nYou will lose 1 guess for each incorrect consonant you guess.\
          \nYou will lose 2 guesses for each incorrect vowel you guess.\
          \nType 'help' to view special commands.\
          \nI am thinking of a word that is", len(secret_word), "letters long:", "_ "*len(secret_word), "\n")

def guess_warning_status(guesses, warnings):
    print("You have", guesses, " guesses and", warnings, "warnings remaining.")

def get_help():
    print("Enter the following for information:\
          \n'hint' - provide a list of remaining words that fit your guesses\n'status'   - provide game status")
    
def match_with_gaps(secret_word_list, guess, letters_guessed):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    j = 0
    n = 0
    if len(guess) != len(secret_word_list):
        return False
    for i in guess:
        if i != secret_word_list[j] and i != "_ ":
            n += 1
        if i == "_ ":
            if secret_word_list[j] in guess:
                return False
            if secret_word_list[j] in letters_guessed:
                return False
        j += 1 
    if n == 0:
        return True
    else: 
        return False

def show_possible_matches(guess, guesses, letters_guessed):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
              Keep in mind that in hangman when a letter is guessed, all the positions
              at which that letter occurs in the secret word are revealed.
              Therefore, the hidden letter(_ ) cannot be one of the letters in the word
              that has already been revealed.
    '''
    wordlist = load_words()
    j = 0
    potential_answers = []
    for i in wordlist:
        if match_with_gaps(wordlist[j], guess, letters_guessed) == True:
            potential_answers.append(wordlist[j])
        j += 1
    if len(potential_answers)>50 and guesses > 3:
        return print("There are currently", len(potential_answers), "possible answers.\
                     \nIt is recommented to use this command once you have guessed a few letters or used atleast 3 guesses")
    if len(potential_answers) == 1:
        return print("There is only 1 potential answer.\
                     \nEnter 'give up' if wish to quit and see the word I am thinking of.")
    return print("Here is a list of the return words:", ", ".join(potential_answers)) 
                
def hangman():
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.
    
    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''    
    wordlist = load_words()
    secret_word = choose_word(wordlist)
    secret_word_list = list(secret_word)
    guesses = 6
    warnings = 3
    letters_guessed = []
    
    hangman_intro(secret_word, guesses, warnings, wordlist)    
    while guesses > 0:
        guess_warning_status(guesses, warnings)
        get_available_letters(letters_guessed)
        guess = get_guessed_word(secret_word_list, letters_guessed)
        guess_letter_output = guess_letters(warnings, guesses, letters_guessed, secret_word_list, guess)
        user_guess = guess_letter_output[0]
        warnings = guess_letter_output[1]
        guesses = guess_letter_output[2]
        letters_guessed = guess_letter_output[3]
        if guesses <= 0:
            break
        # letters_guessed.append(user_guess) #adds guessed letter to the guessed letter list
        
        guesses = guess_verdict(user_guess, secret_word, guesses, letters_guessed)
        hangman_status(guesses)
        if is_word_guessed(secret_word_list, letters_guessed) == True:
            break
        print("_ " * 20, "\n")
    if guesses > 0:
        score = guesses*len(secret_word)
        print("\nCongratulations, you won!\nYour score: ", score)
    else:
        score = 0
        print("\nYou lost!\nThe word I was thinking of was:", secret_word)
    print("Program shutting down...")
    return score

def continue_function():
    while True:
        a = input("\nWould you like to run the program again? [Yes or No]: ")
        if a.lower() == "yes":
            print("\n", "-"*25,"-"*25)
            return 1
        elif a.lower() == "no": 
            print("\nProgram shutting down...\n", "-"*25,"-"*25)
            return 0
        else: 
            print("Enter a valid response!")


if __name__ == "__main__":
    i = 1
    while i == 1:
        hangman()
        i = continue_function()



