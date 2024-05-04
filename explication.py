# Importing the tkinter module and aliasing it as tk
import tkinter as tk

# Creating the main application window
root = tk.Tk()

# Making the window not resizable
root.resizable(True, False) # Change the first parameter to True to make the window resizable in the x-direction

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

# Variable to keep track of the current player
current_chr = "X"

# Creating the play area frame
play_area = tk.Frame(root, width=300, height=300, bg='white')

# Lists to keep track of X and O points
XO_points = []
X_points = []
O_points = []

# Class to represent each point on the game grid
class XOPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = None
        self.button = tk.Button(play_area, text="", width=10, height=5, command=self.set)
        self.button.grid(row=x, column=y)

    # Function to set the value of the point
    def set(self):
        global current_chr
        if not self.value:
            self.button.configure(text=current_chr, bg='snow', fg='black')
            self.value = current_chr
            # Updating the player's turn
            if current_chr == "X":
                X_points.append(self)
                current_chr = "O"
                status_label.configure(text="O's turn")
            elif current_chr == "O":
                O_points.append(self)
                current_chr = "X"
                status_label.configure(text="X's turn")
        # Checking for a win or draw
        check_win()
        if play_with == "Computer" and status_label['text'] == "O's turn":
            auto_play()

    # Function to reset the point
    def reset(self):
        self.button.configure(text="", bg='lightgray')
        if self.value == "X":
            X_points.remove(self)
        elif self.value == "O":
            O_points.remove(self)
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
            for point in X_points:
                if point.x == self.x1 and point.y == self.y1:
                    self.p1_satisfied = True
                elif point.x == self.x2 and point.y == self.y2:
                    self.p2_satisfied = True
                elif point.x == self.x3 and point.y == self.y3:
                    self.p3_satisfied = True
        elif for_chr == 'O':
            for point in O_points:
                if point.x == self.x1 and point.y == self.y1:
                    self.p1_satisfied = True
                elif point.x == self.x2 and point.y == self.y2:
                    self.p2_satisfied = True
                elif point.x == self.x3 and point.y == self.y3:
                    self.p3_satisfied = True
        return all([self.p1_satisfied, self.p2_satisfied, self.p3_satisfied])

# List of winning possibilities
winning_possibilities = [
    WinningPossibility(1, 1, 1, 2, 1, 3),
    WinningPossibility(2, 1, 2, 2, 2, 3),
    WinningPossibility(3, 1, 3, 2, 3, 3),
    WinningPossibility(1, 1, 2, 1, 3, 1),
    WinningPossibility(1, 2, 2, 2, 3, 2),
    WinningPossibility(1, 3, 2, 3, 3, 3),
    WinningPossibility(1, 1, 2, 2, 3, 3),
    WinningPossibility(3, 1, 2, 2, 1, 3)
]

# Function to disable the game after it's finished
def disable_game():
    for point in XO_points:
        point.button.configure(state=tk.DISABLED)
    play_again_button.pack()

# Function to check if the game has been won or drawn
def check_win():
    for possibility in winning_possibilities:
        if possibility.check('X'):
            status_label.configure(text="X won!")
            disable_game()
            return
        elif possibility.check('O'):
            status_label.configure(text="O won!")
            disable_game()
            return
    if len(X_points) + len(O_points) == 9:
        status_label.configure(text="Draw!")
        disable_game()

# Packing the play area into the root window
play_area.pack(pady=10, padx=10)


def auto_play():


    # If winning is possible in the next move
    for winning_possibility in winning_possibilities:
        winning_possibility.check('O')
        if winning_possibility.p1_satisfied and winning_possibility.p2_satisfied:
            for point in XO_points:
                if point.x == winning_possibility.x3 and point.y == winning_possibility.y3 and point not in X_points + O_points:
                    point.set()
                    return
        elif winning_possibility.p2_satisfied and winning_possibility.p3_satisfied:
            for point in XO_points:
                if point.x == winning_possibility.x1 and point.y == winning_possibility.y1 and point not in X_points + O_points:
                    point.set()
                    return
        elif winning_possibility.p3_satisfied and winning_possibility.p1_satisfied:
            for point in XO_points:
                if point.x == winning_possibility.x2 and point.y == winning_possibility.y2 and point not in X_points + O_points:
                    point.set()
                    return

    # If the opponent can win in the next move
    for winning_possibility in winning_possibilities:
        winning_possibility.check('X')
        if winning_possibility.p1_satisfied and winning_possibility.p2_satisfied:
            for point in XO_points:
                if point.x == winning_possibility.x3 and point.y == winning_possibility.y3 and point not in X_points + O_points:
                    point.set()
                    return
        elif winning_possibility.p2_satisfied and winning_possibility.p3_satisfied:
            for point in XO_points:
                if point.x == winning_possibility.x1 and point.y == winning_possibility.y1 and point not in X_points + O_points:
                    point.set()
                    return
        elif winning_possibility.p3_satisfied and winning_possibility.p1_satisfied:
            for point in XO_points:
                if point.x == winning_possibility.x2 and point.y == winning_possibility.y2 and point not in X_points + O_points:
                    point.set()
                    return

    # If the center is free...
    center_occupied = False
    for point in X_points + O_points:
        if point.x == 2 and point.y == 2:
            center_occupied = True
            break
    if not center_occupied:
        for point in XO_points:
            if point.x == 2 and point.y == 2:
                point.set()
                return

    # Occupy corner or middle based on what opponent occupies
    corner_points = [(1, 1), (1, 3), (3, 1), (3, 3)]
    middle_points = [(1, 2), (2, 1), (2, 3), (3, 2)]
    num_of_corner_points_occupied_by_X = 0
    for point in X_points:
        if (point.x, point.y) in corner_points:
            num_of_corner_points_occupied_by_X += 1
    if num_of_corner_points_occupied_by_X >= 2:
        for point in XO_points:
            if (point.x, point.y) in middle_points and point not in X_points + O_points:
                point.set()
                return
    elif num_of_corner_points_occupied_by_X < 2:
        for point in XO_points:
            if (point.x, point.y) in corner_points and point not in X_points + O_points:
                point.set()
                return

root.mainloop()