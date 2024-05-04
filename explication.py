# Importing the tkinter module and aliasing it as tk
import tkinter as tk

# Creating the main application window
root = tk.Tk()

# Making the window not resizable
root.resizable(False, False) # Change the first parameter to True to make the window resizable in the x-direction

# Setting the title of the window
root.title("Tic Tac Toe for English")

# Creating a label widget with the title "Tic Tac Toe" and packing it into the root window
tk.Label(root, text="Tic Tac Toe", font=('Ariel', 25)).pack()

# Creating a label widget to display game status and packing it into the root window
status_label = tk.Label(root, text="X's turn", font=('Ariel', 15), bg='green', fg='snow')
status_label.pack(fill=tk.X)

# Function to reset the game
def play_again():
    global current_chr
    current_chr = 'X' # First player is always X
    # Resetting all points
    for point in XO_points: # XO_points is a list of all points in the game
        point.button.configure(state=tk.NORMAL) # Making the point clickable
        print("Here Im Again")
        point.reset()  
    status_label.configure(text="X's turn") # Setting the status label to show that it's X's turn
    play_again_button.pack_forget() # Hiding the play again button

# Creating a button widget to play again
play_again_button = tk.Button(root, text='Play again', font=('Ariel', 15), command=play_again)
play_with = "Computer"
# Function to set the game mode to play with a human
def play_with_human():
    global play_with 
    play_with = "Human" 
    play_with_button['text'] = "Play with computer"
    play_with_button['command'] = play_with_computer
    play_again()

# Function to set the game mode to play with a computer
def play_with_computer():
    global play_with
    play_with = "Computer"
    play_with_button['text'] = "Play with human"
    play_with_button['command'] = play_with_human
    play_again()

# Creating a button widget to choose to play with a human initially
play_with_button = tk.Button(root, text='Play with human', font=('Ariel', 15), command=play_with_human)
play_with_button.pack()

# Variable to keep track (watch) of the current player
current_chr = "X"

# Creating the play area frame
play_area = tk.Frame(root, width=300, height=300, bg='white')

# Lists to keep track of X and O points
XO_points = [] # List of all points
X_points = [] # List of all X points
O_points = [] # List of all O points

# Class to represent each point on the game grid
class XOPoint:
    def __init__(self, x, y): 
        self.x = x # x-coordinate of the point
        self.y = y # y-coordinate of the point
        self.value = None # Value of the point (X, O, or None)
        self.button = tk.Button(play_area, text="", width=10, height=5, command=self.set) # Button widget representing the point
        self.button.grid(row=x, column=y) # Packing the button into the play area

    # Function to set the value of the point
    def set(self):
        global current_chr
        if not self.value: # If the point is empty
            self.button.configure(text=current_chr, bg='snow', fg='black') # Setting the text and background color of the button
            self.value = current_chr # Setting the value of the point
            # Updating the player's turn
            if current_chr == "X": 
                X_points.append(self) # Adding the point to the list of X points
                current_chr = "O" # Changing the current player to O
                status_label.configure(text="O's turn") # Updating the status label
            elif current_chr == "O": 
                O_points.append(self) # Adding the point to the list of O points
                current_chr = "X" # Changing the current player to X
                status_label.configure(text="X's turn") # Updating the status label
        # Checking for a win or draw
        check_win()
        if play_with == "Computer" and status_label['text'] == "O's turn":
            auto_play()

    # Function to reset the point
    def reset(self):
        self.button.configure(text="", bg='lightgray')  
        if self.value == "X":
            X_points.remove(self) # Removing the point from the list of X points
        elif self.value == "O":
            O_points.remove(self) # Removing the point from the list of O points
        self.value = None

# Creating XOPoint objects for each cell in the grid
for x in range(1, 4):
    for y in range(1, 4):
        XO_points.append(XOPoint(x, y))

# Class to represent winning possibilities
class WinningPossibility:
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.x1 = x1 # x-coordinate of the first point 
        self.y1 = y1 # y-coordinate of the first point
        self.x2 = x2 # x-coordinate of the second point
        self.y2 = y2 # y-coordinate of the second point
        self.x3 = x3 # x-coordinate of the third point
        self.y3 = y3 # y-coordinate of the third point

    # Function to check if a winning possibility is satisfied
    def check(self, for_chr):
        self.p1_satisfied = False   
        self.p2_satisfied = False
        self.p3_satisfied = False
        if for_chr == 'X':
            for point in X_points:  # X_points is a list of all X points
                if point.x == self.x1 and point.y == self.y1: # If the first point is satisfied
                    self.p1_satisfied = True # Mark the first point as satisfied
                elif point.x == self.x2 and point.y == self.y2: 
                    self.p2_satisfied = True
                elif point.x == self.x3 and point.y == self.y3:
                    self.p3_satisfied = True
        elif for_chr == 'O':
            for point in O_points: # O_points is a list of all O points
                if point.x == self.x1 and point.y == self.y1: # If the first point is satisfied
                    self.p1_satisfied = True # Mark the first point as satisfied
                elif point.x == self.x2 and point.y == self.y2: 
                    self.p2_satisfied = True
                elif point.x == self.x3 and point.y == self.y3:
                    self.p3_satisfied = True
        return all([self.p1_satisfied, self.p2_satisfied, self.p3_satisfied]) # Return True if all points are satisfied

# List of winning possibilities
winning_possibilities = [ 
    WinningPossibility(1, 1, 1, 2, 1, 3), # Horizontal possibilities 
    WinningPossibility(2, 1, 2, 2, 2, 3), # Horizontal possibilities
    WinningPossibility(3, 1, 3, 2, 3, 3), # Horizontal possibilities
    WinningPossibility(1, 1, 2, 1, 3, 1), # Vertical possibilities
    WinningPossibility(1, 2, 2, 2, 3, 2), # Vertical possibilities
    WinningPossibility(1, 3, 2, 3, 3, 3), # Vertical possibilities
    WinningPossibility(1, 1, 2, 2, 3, 3), # Diagonal possibilities
    WinningPossibility(3, 1, 2, 2, 1, 3)  # Diagonal possibilities 
]

# Function to disable the game after it's finished
def disable_game():
    for point in XO_points: # XO_points is a list of all points
        point.button.configure(state=tk.DISABLED) # Disabling the button
    play_again_button.pack() # Packing the play again button

# Function to check if the game has been won or drawn
def check_win():
    for possibility in winning_possibilities: # For each winning possibility
        if possibility.check('X'): # If the possibility is satisfied by X
            status_label.configure(text="X won!") # Set the status label to show that X won
            disable_game() # Disable the game
            return # Exit the function
        elif possibility.check('O'): # If the possibility is satisfied by O
            status_label.configure(text="O won!") # Set the status label to show that O won
            disable_game() # Disable the game
            return # Exit the function
    if len(X_points) + len(O_points) == 9: # If all points are occupied
        status_label.configure(text="Draw!") # Set the status label to show that the game is a draw
        disable_game() # Disable the game

# Packing the play area into the root window
play_area.pack(pady=10, padx=50) 


def auto_play():
    # If winning is possible in the next move
    for winning_possibility in winning_possibilities: # For each winning possibility
        winning_possibility.check('O') # Check if the possibility is satisfied by O
        if winning_possibility.p1_satisfied and winning_possibility.p2_satisfied: # If the first two points are satisfied
            for point in XO_points: # For each point in the game
                if point.x == winning_possibility.x3 and point.y == winning_possibility.y3 and point not in X_points + O_points: # If the third point is empty
                    point.set() # Set the point
                    return # Exit the function
        elif winning_possibility.p2_satisfied and winning_possibility.p3_satisfied: # If the second and third points are satisfied
            for point in XO_points: # For each point in the game
                if point.x == winning_possibility.x1 and point.y == winning_possibility.y1 and point not in X_points + O_points: # If the first point is empty
                    point.set() # Set the point
                    return # Exit the function
        elif winning_possibility.p3_satisfied and winning_possibility.p1_satisfied: # If the third and first points are satisfied
            for point in XO_points: # For each point in the game
                if point.x == winning_possibility.x2 and point.y == winning_possibility.y2 and point not in X_points + O_points: # If the second point is empty
                    point.set() # Set the point
                    return # Exit the function

    # If the opponent can win in the next move
    for winning_possibility in winning_possibilities: # For each winning possibility
        winning_possibility.check('X') # Check if the possibility is satisfied by X 
        if winning_possibility.p1_satisfied and winning_possibility.p2_satisfied: # If the first two points are satisfied
            for point in XO_points: # For each point in the game
                if point.x == winning_possibility.x3 and point.y == winning_possibility.y3 and point not in X_points + O_points: # If the third point is empty
                    point.set() # Set the point
                    return
        elif winning_possibility.p2_satisfied and winning_possibility.p3_satisfied: # If the second and third points are satisfied
            for point in XO_points:
                if point.x == winning_possibility.x1 and point.y == winning_possibility.y1 and point not in X_points + O_points: # If the first point is empty
                    point.set() # Set the point
                    return
        elif winning_possibility.p3_satisfied and winning_possibility.p1_satisfied: # If the third and first points are satisfied
            for point in XO_points: # For each point in the game
                if point.x == winning_possibility.x2 and point.y == winning_possibility.y2 and point not in X_points + O_points: # If the second point is empty
                    point.set()
                    return

    # If the center is free...
    center_occupied = False # Variable to keep track of whether the center is occupied
    for point in X_points + O_points: # For each point occupied by X or O
        if point.x == 2 and point.y == 2: # If the point is the center
            center_occupied = True # Mark the center as occupied
            break # Exit the loop
    if not center_occupied: # If the center is not occupied
        for point in XO_points: # For each point in the game 
            if point.x == 2 and point.y == 2: # If the point is the center
                point.set() # Set the point
                return

    # Occupy corner or middle based on what opponent occupies
    corner_points = [(1, 1), (1, 3), (3, 1), (3, 3)] # List of corner points
    middle_points = [(1, 2), (2, 1), (2, 3), (3, 2)] # List of middle points
    num_of_corner_points_occupied_by_X = 0 # Variable to keep track of the number of corner points occupied by X
    for point in X_points: # For each point occupied by X
        if (point.x, point.y) in corner_points: # If the point is a corner point
            num_of_corner_points_occupied_by_X += 1 # Increment the number of corner points occupied by X
    if num_of_corner_points_occupied_by_X >= 2: # If X occupies at least two corner points
        for point in XO_points: # For each point in the game
            if (point.x, point.y) in middle_points and point not in X_points + O_points:  # If the point is a middle point and is not occupied
                point.set() # Set the point
                return # Exit the function
    elif num_of_corner_points_occupied_by_X < 2: # If X occupies less than two corner points
        for point in XO_points: # For each point in the game
            if (point.x, point.y) in corner_points and point not in X_points + O_points: # If the point is a corner point and is not occupied
                point.set() # Set the point
                return # Exit the function

root.mainloop() # Start the main event loop
