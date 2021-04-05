# The final project for a course TIE-02100 Johdatus ohjelmointiin (Introduction to Programming)
# Programmed in the autumn 2017.
# Anriika Kauppi @anriikakauppi
# Tomi Jokkeenhaara @JokkeT
# Two-player Memory Game
# Status: Finished
#
# The purpose of this program is to act as a two-player memory game.
# To start the game, push the button "New Game" which will open a pop-up window.
# The players' names will be asked in the pop-up window. The window can be closed
# by clicking the "Done" button after the names have been given.
#
# Player 1 starts the game by choosing two cards which will turn from being clicked on.
# If the cards create a pair, they'll remain open and Player 1 may try again. Otherwise the
# cards will turn facing down and the turn is passed onto Player 2 by clicking the button "
# Next turn". For every found pair, a player gets a point.
#
# The game continues until all of the pairs are found and the game announces the winner.
# Players can start a new game whenever by clicking the button "New Game". The game closes
# by clicking the "Exit" button.


from tkinter import *
import random
import time

ROWS = 4
COLUMNS = 4
CARD_IMAGES = ["CoverImages/1.gif", "CoverImages/2.gif", "CoverImages/3.gif", "CoverImages/4.gif",
               "CoverImages/5.gif", "CoverImages/6.gif", "CoverImages/7.gif", "CoverImages/8.gif"]


class MemoryGame:
    def __init__(self):
        self.__mainwindow = Tk()
        self.__mainwindow.title("Finland100 Memory Game")
        self.__mainwindow.option_add("*Font", "fixedsys 16")
        self.__mainwindow.configure(background="LightSteelBlue1")

        self.__image_back = PhotoImage(file="CoverImages/backside.gif",
                                       width=86, height=86)

        self.__images_for_buttons = []
        for img_file in CARD_IMAGES:
            img = PhotoImage(file=img_file)
            self.__images_for_buttons.append(img)

        self.buttons = {}
        self.visible_sides = {}
        self.button_front_images = {}
        self.front_images_used = [0] * len(CARD_IMAGES)

        self.__turn_button = Button(self.__mainwindow, text="Next player",
                                    command=self.change_turn, state=DISABLED)
        self.__turn_button.grid(row=1, column=COLUMNS, sticky=W + E)

        self.refresh_game()

        for each in self.buttons:
            self.buttons[each].configure(state=DISABLED)

        self.__stop_button = Button(self.__mainwindow, text="Exit",
                                    command=self.shutdown)
        self.__stop_button.grid(row=ROWS +1, column=COLUMNS, sticky=W + E)

        self.__newgame_button =Button(self.__mainwindow, text="New game", command=self.when_clicked)
        self.__newgame_button.grid(row=0, column=COLUMNS, sticky=W+E+N)

        self.__turn = 0

        points1 = self.__player1_points = 0
        points2 = self.__player2_points = 0
        player1 = ""
        player2 = ""

        self.__points_label1 = Label(self.__mainwindow)
        self.__points_label1.grid(row=ROWS + 1, column=0, columnspan=2, sticky=W+E)
        self.__points_label2 = Label(self.__mainwindow)
        self.__points_label2.grid(row=ROWS + 1, column= 2, columnspan=2, sticky=W+E)

        self.__active_player_label = \
            Label(self.__mainwindow)
        self.__active_player_label.grid(row=2, column=COLUMNS,
                                        sticky=W + E)

    def start(self):
        """
        Starts the game window.
        :return:
        """
        self.__mainwindow.mainloop()

    def shutdown(self):
        """
        Closes the game window.
        :return:
        """
        self.__mainwindow.destroy()

    def flip_card(self, index):
        """
        Flips over a card with the given index. Checks if all cards for the
        turn have been flipped.
        :param index: str, index of the card
        :return:
        """
        if self.visible_sides[index] == "backside":
            self.buttons[index].configure(
                image=self.button_front_images[index])
            self.visible_sides[index] = "frontside"
            self.buttons[index].config(state=DISABLED)
        else:
            self.buttons[index].configure(image=self.__image_back)
            self.visible_sides[index] = "backside"
            self.buttons[index].config(state=ACTIVE)

        self.__cards_turned_this_turn.append(index)
        self.check_for_end_turn()

    def add_in_dict(self, button, index):
        """
        Adds the button to two dicts,
        which are used to manipulate the button.
        :param button: button, the object to be added
        :param index: str, index of the button
        :return:
        """
        self.buttons[index] = button
        self.visible_sides[index] = "backside"

    def check_for_end_turn(self):
        """
        Ends the turn when two cards are turned over. Enables the turn button
        for when the player is ready to pass the turn.
        :return:
        """
        if len(self.__cards_turned_this_turn) >= 2:
            self.enable_turn_button()
            self.disable_card_buttons()
            self.check_match()

    def disable_card_buttons(self):
        """
        Disables card buttons when the turn is ending.
        :return:
        """
        for button in self.buttons:
            self.buttons[button].config(state=DISABLED)

    def enable_card_buttons(self):
        """
        Enables card buttons for the next turn.
        :return:
        """
        for button in self.buttons:
            self.buttons[button].config(state=ACTIVE)

    def enable_turn_button(self):
        """
        Enables the button to start the next turn.
        :return:
        """
        self.__turn_button.config(state=ACTIVE)

    def change_turn(self):
        """
        Sets the game ready for the next turn. Changes the player in turn,
        turns flipped cards back over, resets the turned cards counter and
        disables the turn button.
        :return:
        """
        self.change_active_player()
        self.reset_cards()
        self.__cards_turned_this_turn = []
        self.__turn_button.config(state=DISABLED)

    def change_active_player(self):
        """
        Updates the information of the turn
        :return:
        """
        if self.__turn == 0:
            self.__turn = 1
            self.__active_player_label.config(text=(f"In turn:\n {player2}"))
        else:
            self.__turn = 0
            self.__active_player_label.config(text=(f"In turn:\n {player1}"))

    def reset_cards(self):
        """
        Flips all cards not yet paired so their backsides are visible.
        :return:
        """
        for button in self.buttons:
            side = self.visible_sides[button]
            if side == "frontside":
                self.flip_card(button)
            self.enable_card_buttons()

    def check_match(self):
        """
        Checks if the flipped cards are a pair.
        :return:
        """
        first_index = self.__cards_turned_this_turn[0]
        second_index = self.__cards_turned_this_turn[1]
        first_image = self.button_front_images[first_index]
        second_image = self.button_front_images[second_index]
        if first_image == second_image:
            self.remove_cards_from_game()
            self.extra_turn()
            self.add_points()
            self.update_points()
            self.check_game_status()

    def remove_cards_from_game(self):
        """
        Removes paired cards from the buttons dict.
        :return:
        """
        for card in self.__cards_turned_this_turn:
            del self.buttons[card]

    def extra_turn(self):
        """
        Awards an extra turn for pairing cards
        :return:
        """
        if self.__turn == 0:
            self.__turn = 1
        else:
            self.__turn = 0

    def generate_images_to_buttons(self):
        """
        Assigns images to represent the faces of the cards. Each image is added
        randomly to two different buttons.
        :return:
        """
        self.front_images_used = [0] * len(CARD_IMAGES)

        for button in self.buttons:
            image_index = random.randint(0, 7)
            while self.front_images_used[image_index] >= 2:
                image_index = random.randint(0, 7)
            self.button_front_images[button] = \
                self.__images_for_buttons[image_index]
            self.front_images_used[image_index] += 1

    def when_clicked(self):
        """
        Opens a pop-up screen which asks the names of the players
        :return:
        """
        inputPopup = Popup(self.__mainwindow, self)

    def start_game(self):
        """
        Changes the background of the mainwindow and actives the cards.
        :return:
        """
        self.__mainwindow.configure(background="LightSteelBlue1")
        for each in self.buttons:
            self.buttons[each].configure(state=ACTIVE)
            self.__active_player_label.config(text=(f"In turn:\n {player1}"))

    def refresh_game(self):
        """
        Resets the game to the starting state: creates new cards, disables and
        suffles them.
        :return:
        """
        for row in range(ROWS):
            for column in range(COLUMNS):
                index = str(row) + str(column)

                def turn_card(button_index=index):
                    self.flip_card(button_index)

                new_button = Button(self.__mainwindow, image=self.__image_back,
                                    command=turn_card)
                new_button.grid(row=row, column=column)
                self.add_in_dict(new_button, index)
        # Nämä rivit uusia, kopsattu initista. Peli alkaa nyt alusta "taydellisemmin".
        self.generate_images_to_buttons()
        self.__cards_turned_this_turn = []
        self.__turn_button.config(state=DISABLED)

    def update_points(self):
        """
        Updates the label which shows the current points of the players
        :return:
        """
        points = self.__player2_points
        self.__points_label2.configure(text=f"{player2}: {points} points")
        points = self.__player1_points
        self.__points_label1.config(text=f"{player1}: {points} points")

    def add_points(self):
        """
        Adds a point for a player.
        :return:
        """
        if self.__turn == 0:
            self.__player2_points += 1
        else:
            self.__player1_points += 1

    def check_game_status(self):
        """
        Checks if the game has ended and tells the winner or that it was a tie.
        Resets the points for the next game.
        :return:
        """
        if len(self.buttons) == 0:
            self.__active_player_label.config(text="")
            self.__turn_button.configure(state=DISABLED)
            if self.__player2_points != self.__player1_points:
                if self.__player2_points > self.__player1_points:
                    winner = player2
                else:
                    winner = player1

                self.__points_label1.configure(text=f"{winner} won!")
                self.__points_label2.configure(text="")
            else:
                self.__points_label1.configure(text=f"It's a tie!")
                self.__points_label2.configure(text="")
            self.__player1_points = 0
            self.__player2_points = 0

class Popup:
    """
    A pop-up window which asks the names of the players. If closed before the
    names are given, sets the names to "Player 1" and "Player 2".
    """

    def __init__(self, parent, MemoryGame):
        popup = self.__popup = Toplevel(parent)
        self.__popup.title("Enter the names of the players")
        self.__popup.grab_set()
        self.__popup.attributes("-topmost", "true")
        parent.configure(background="alice blue")

        self.__parent = parent
        self.__memorygame = MemoryGame

        self.__player1_infotext = Label(popup, text=" First player:")
        self.__player1_infotext.grid(row=0, column=0, sticky=W)
        self.__player1_entry = Entry(popup)
        self.__player1_entry.grid(row=0, column=1)

        self.__player2_infotext = Label(popup, text=" Second player:")
        self.__player2_infotext.grid(row=1, column=0, sticky=W)
        self.__player2_entry = Entry(popup)
        self.__player2_entry.grid(row=1, column=1)

        self.__done_button = Button(popup, text="Done",
                                    command=self.send)
        self.__done_button.grid(row=2, column=2)

        self.__popup.protocol("WM_DELETE_WINDOW", self.on_exit)

        MemoryGame.refresh_game()

    def send(self):
        """
        Provides the names of the players to the memory game window. If no
        names are given and "Done" is pressed, gives an error message.
        :return:
        """
        global player1
        global player2
        player1 = self.__player1_entry.get()
        player2 = self.__player2_entry.get()
        if player2 == "" or player1 == "":
            errorMessage = Label(self.__popup, text="Please enter the names")
            errorMessage.grid(row=3, column=1)
        else:
            self.__memorygame.start_game()
            self.__memorygame.update_points()
            self.__popup.destroy()

    def on_exit(self):
        """
        Defines the names of the players if none are given.
        :return:
        """
        global player1, player2
        try:
            player1
            player2
            self.__popup.destroy()
        except NameError:
            player1 = "Player 1"
            player2 = "Player 2"
            self.__memorygame.change_active_player()
            self.__popup.destroy()


def main():
    ui = MemoryGame()
    ui.start()


main()
