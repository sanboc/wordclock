from tkinter import *
from tkinter import ttk
import time
import datetime


# Letter class is used for each letter in the clock. When an instance is created, the letter defined is immediately
# added to the canvas object in the inactive color (#333333). The class has functions for setting and getting activity,
# where activity is defined as true depending on the time. In most cases #333333 is inactive,
# and all other colors are active, however this is not the case when brightness has been set to
# fully dimmed. When this is the case, the clock is still expected to keep track of time, so that
# when the brightness is turned back up, the time will automatically be correct. Active status is used in
# features such as change brightness and change color, so the function knows which letters to change colors and which
# to ignore. Active status is changed by the word class automatically when changing colors of member letters.
class Letter:
    def __init__(self, canvas, text, column, row):
        self.canvas = canvas
        self.text = text
        self.color = "#333333"
        self.active = False
        self.label = Label(self.canvas, text=self.text,
                           fg=self.color, bg="#000000",
                           padx=15, pady=5)
        self.label.grid(row=row, column=column)

    def setActive(self, active):
        self.active = active
        return

    def getActive(self):
        return self.active

    def setColor(self, newcolor):
        self.label["fg"] = newcolor
        return


# Word class groups individual letter instances into a known word. Minimum of two letters (AM, PM)) and maximum of
# eight letters (MIDNIGHT). When an instance is created, it is immediately assumed to be inactive. Activity here works
# the same as it does in the Letter class, with the primary exception being that the word class manages its own
# activity, whereas in the Letter class, the letter is told if it is active or not by external functions. Active
# is still defined as all colors other than #333333, except in cases where brightness is fully dimmed. If the
# fade_to_white function has been run, it is assumed that the word is active, even if the color is #333333.
class Word:
    def __init__(self, letter1, letter2, letter3=None, letter4=None, letter5=None, letter6=None, letter7=None,
                 letter8=None, master=None):
        self.letter1 = letter1
        self.letter2 = letter2
        self.letter3 = letter3
        self.letter4 = letter4
        self.letter5 = letter5
        self.letter6 = letter6
        self.letter7 = letter7
        self.letter8 = letter8
        self.master = master
        self.active = False

    def setActive(self, active):
        self.active = active

    def getActive(self):
        return self.active

    # The fade_to_white function fades the letters in the word from #333333 to the selected color. The minutes argument
    # is not used here, but is included to facilitate using instances of Word and instances of HStatement or MStatment
    # in the same context, which do require a minutes argument in their respective fade_to_white functions.
    #
    # fade_to_white works by treating the Red, Green, and Blue components of a hexadecimal color code as sliders. First,
    # the selected color is evaluated to see which of the three components are included in the selected color. For
    # example, if blue is a component, then the last two digits of the code will be either FF (for fully bright) or
    # AA (for fully dimmed). Once its determined that blue is a component, a multiple of the value "04" will be added to
    # the starting value of "33" for each iteration of the loop, to gradually "slide" the  blue component up to its
    # final value of "FF" or "AA". If blue is determined to NOT be a component of the selected color (the last two
    # digits of the code will be "00"), then a multiple of the value of "01" will be SUBTRACTED from the starting value
    # of "33" for each iteration of the loop, to gradually slide the blue component DOWN to its final value of "00".
    # These three components are added up to yield the current color code and the appropriate letters have their new
    # colors set.
    #
    # Because hexadecimal color codes require six digits, but an actual hexadecimal number could be truncated of its
    # leading digits if they are 0 and therefore not significant, the color code is checked for length and has these
    # leading digits added if necessary.
    #
    # The tkinter app is updated after each new color is set, and a delay is applied, to provide the visual fade.
    def fade_to_white(self, color, minutes=0):
        i = 1
        while not self.active:  # Only run if the word is off. If the word is already on, do not run again.
            if color[0] == "F":  # Red is a component
                red = (int("040000", 16) * i) + int("330000", 16)
            elif color[0] == "A":  # Red is a component, and dimming is active
                red = (int("020000", 16) * i) + int("330000", 16)
            else:
                red = int("330000", 16) - (int("010000", 16) * i)
            if color[2] == "F":  # Green is a component
                green = (int("000400", 16) * i) + int("003300", 16)
            elif color[2] == "A":  # Green is a component and dimming is active
                green = (int("000200", 16) * i) + int("003300", 16)
            else:
                green = int("003300", 16) - (int("000100", 16) * i)
            if color[4] == "F":  # Blue is a component
                blue = (int("000004", 16) * i) + int("000033", 16)
            elif color[4] == "A":  # Blue is a component, and dimming is active
                blue = (int("000002", 16) * i) + int("000033", 16)
            else:
                blue = int("000033", 16) - (int("000001", 16) * i)
            newcolorhex = hex(red+green+blue)  # Combine all newly calculated RBG values into new hex code.
            if len(newcolorhex) == 8:  # Concatenate string together, with appropriate leading zeros as needed.
                finalcolorhex = "#" + newcolorhex[2:8]
            elif len(newcolorhex) == 7:
                finalcolorhex = "#0" + newcolorhex[2:7]
            elif len(newcolorhex) == 6:
                finalcolorhex = "#00" + newcolorhex[2:6]
            else:
                finalcolorhex = "#FFFFFF"
            self.letter1.setColor(finalcolorhex)
            self.letter1.setActive(True)
            self.letter2.setColor(finalcolorhex)
            self.letter2.setActive(True)
            if self.letter3 is not None:
                self.letter3.setColor(finalcolorhex)
                self.letter3.setActive(True)
            if self.letter4 is not None:
                self.letter4.setColor(finalcolorhex)
                self.letter4.setActive(True)
            if self.letter5 is not None:
                self.letter5.setColor(finalcolorhex)
                self.letter5.setActive(True)
            if self.letter6 is not None:
                self.letter6.setColor(finalcolorhex)
                self.letter6.setActive(True)
            if self.letter7 is not None:
                self.letter7.setColor(finalcolorhex)
                self.letter7.setActive(True)
            if self.letter8 is not None:
                self.letter8.setColor(finalcolorhex)
                self.letter8.setActive(True)
            i = i + 1
            if i is 52:  # If done, set word active status.
                self.setActive(True)
            time.sleep(0.03)
            self.master.update_idletasks()
            self.master.update()
        return

    # fade_to_grey works very similar to fade_to_white, but in reverse. See fade_to_white for more details.
    def fade_to_grey(self, color, minutes=0):
        i = 1
        while self.active:  # Only run this if the word is on. If the word is already off, do not run again.
            if color[0] == "F":  # Red is a component
                red = int("FF0000", 16) - (int("040000", 16) * i)
            elif color[0] == "A":  # Red is a component and dimming is active
                red = int("AA0000", 16) - (int("020000", 16) * i)
            else:
                red = (int("010000", 16) * i) + int("000000", 16)
            if color[2] == "F":  # Green is a component
                green = int("00FF00", 16) - (int("000400", 16) * i)
            elif color[2] == "A":  # Green is a component and dimming is active
                green = int("00AA00", 16) - (int("000200", 16) * i)
            else:
                green = (int("000100", 16) * i) + int("000000", 16)
            if color[4] == "F":  # Blue is a component
                blue = int("0000FF", 16) - (int("000004", 16) * i)
            elif color[4] == "A":  # Blue is a component and dimming is active
                blue = int("0000AA", 16) - (int("000002", 16) * i)
            else:
                blue = (int("000001", 16) * i) + int("000000", 16)
            newcolorhex = hex(red+green+blue)  # Combine all newly calculated RBG values into new hex code.
            if len(newcolorhex) == 8:  # Concatenate string together, with appropriate leading zeros as needed.
                finalcolorhex = "#" + newcolorhex[2:8]
            elif len(newcolorhex) == 7:
                finalcolorhex = "#0" + newcolorhex[2:7]
            elif len(newcolorhex) == 6:
                finalcolorhex = "#00" + newcolorhex[2:6]
            else:
                finalcolorhex = "#333333"
            self.letter1.setColor(finalcolorhex)
            self.letter1.setActive(False)
            self.letter2.setColor(finalcolorhex)
            self.letter2.setActive(False)
            if self.letter3 is not None:
                self.letter3.setColor(finalcolorhex)
                self.letter3.setActive(False)
            if self.letter4 is not None:
                self.letter4.setColor(finalcolorhex)
                self.letter4.setActive(False)
            if self.letter5 is not None:
                self.letter5.setColor(finalcolorhex)
                self.letter5.setActive(False)
            if self.letter6 is not None:
                self.letter6.setColor(finalcolorhex)
                self.letter6.setActive(False)
            if self.letter7 is not None:
                self.letter7.setColor(finalcolorhex)
                self.letter7.setActive(False)
            if self.letter8 is not None:
                self.letter8.setColor(finalcolorhex)
                self.letter8.setActive(False)
            i = i + 1
            if i is 52:
                self.setActive(False)  # If done, set word active status.
            time.sleep(0.03)
            self.master.update_idletasks()
            self.master.update()
        return


# The HStatement class is a collection of words which together comprise an "Hour Statement", such as "ONE O'CLOCK PM".
# This class is very similar to but with notable differences from MStatement, which is defined as a collection of
# words to comprise a "Minute Statement". Activity works the same in the statement classes as it does in the Word
# class.
class HStatement:
    def __init__(self, word1, word2, word3):
        self.word1 = word1
        self.word2 = word2
        self.word3 = word3
        self.active = False

    def setActive(self, active):
        self.active = active

    def getActive(self):
        return self.active

    # fade_to_white is running the fade_to_white functions of the word class (see those functions for more details). The
    # minutes value is used to determine if "O'CLOCK" should be shown. O'CLOCK is always word2, and is only active when
    # minutes = 0, or when a digital clock is displaying :00 through :04.
    #
    # fade_to_white in the HStatement class is also setting its own active state. This active state is referenced by
    # the updatetime function to determine when to run fade_to_white or fade_to_grey.
    def fade_to_white(self, color, minutes=0):
        self.word1.fade_to_white(color)
        if minutes is 0:
            self.word2.fade_to_white(color)
        else:
            self.word2.fade_to_grey(color)
        self.word3.fade_to_white(color)
        self.setActive(True)

    # fade_to_grey is running the fade_to_grey functions of the word class (see those functions for more details). The
    # hour value is used to determine if PM or AM should be deactivated. AM or PM, which as always word3, should only
    # be deactivated if the time is NOON or MIDNIGHT. All other hours should leave AM or PM active, to prevent
    # unwanted blinking between hours.
    def fade_to_grey(self, color, hour):
        self.word1.fade_to_grey(color)
        self.word2.fade_to_grey(color)
        if hour is 24 or hour is 0:
            self.word3.fade_to_grey(color)
        self.setActive(False)


# The MStatement class is a collection of words which together comprise an "Minute Statement", such as "IT'S HALF PAST".
# This class is very similar to but with notable differences from HStatement, which is defined as a collection of
# words to comprise an "Hour Statement". Activity works the same in the statement classes as it does in the Word
# class.
class MStatement:
    def __init__(self, word1, word2, word3):
        self.word1 = word1
        self.word2 = word2
        self.word3 = word3
        self.active = False

    def setActive(self, active):
        self.active = active

    def getActive(self):
        return self.active

    # fade_to_white is running the fade_to_white functions of the word class (see those functions for more details).
    #
    # fade_to_white in the MStatement class is also setting its own active state. This active state is referenced by
    # the updatetime function to determine when to run fade_to_white or fade_to_grey.
    def fade_to_white(self, color):
        self.word1.fade_to_white(color)
        self.word2.fade_to_white(color)
        self.word3.fade_to_white(color)
        self.setActive(True)

    # fade_to_grey is running the fade_to_grey functions of the word class (see those functions for more details).
    #
    # fade_to_grey never greys out word1, as word1 is always IT'S, and IT'S is always active.
    # fade_to_grey only greys out word3 when minutes is either 8 or 0, or :40-:44, :00-:04 on the clock. These are the
    # only times that the clock changes from saying "PAST" to "TIL", or "TIL" to nothing. Otherwise, PAST/TIL are left
    # active to prevent unwanted blinking.
    def fade_to_grey(self, color, minutes):
        self.word2.fade_to_grey(color)
        if minutes is 8 or minutes is 0:
            self.word3.fade_to_grey(color)
        self.setActive(False)


class Application(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master = master
        self.CanvasBG = Canvas(self, width=1000, height=1000, bd=0, highlightthickness=0, relief='ridge')
        self.CanvasBG.configure(background='black')
        self.CanvasBG.pack(side="left", fill="both", expand=True)
        # Color options are as follows:
        #   #FFFFFF: WHITE, #AAAAAA: DIMMED WHITE, #333333: OFF
        #   #00FF00: GREEN, #00AA00: DIMMED GREEN, #333333: OFF
        #   #FF0000: RED, #AA0000: DIMMED RED, #333333: OFF
        #   #FF00FF: VIOLET, #AA00AA: DIMMED VIOLET, #333333: OFF
        #   #00FFFF: INDIGO, #00AAAA: DIMMED INDIGO, #333333: OFF
        #   #FFFF00: YELLOW, #AAAAAA: DIMMED YELLOW, #333333: OFF
        #   #0000FF: BLUE, #0000AA: DIMMED BLUE, #333333: OFF
        self.colorOptions = (("FFFFFF", "AAAAAA", "333333"), ("00FF00", "00AA00", "333333"),
                             ("FF0000", "AA0000", "333333"), ("FF00FF", "AA00AA", "333333"),
                             ("00FFFF", "00AAAA", "333333"), ("FFFF00", "AAAA00", "333333"),
                             ("0000FF", "0000AA", "333333"))
        self.colorSelection = 0  # Initialized at white
        self.brightnessSelection = 0  # Initialized at brightest
        self.color = self.colorOptions[self.colorSelection][self.brightnessSelection]

        # Letters is the array of letter instances. There are 100 letters. Two letter instances also include an
        # apostrophe.
        self.Letters = []
        self.Letters.append((Letter(self.CanvasBG, text="I", column=0, row=0),
                             Letter(self.CanvasBG, text="T'", column=1, row=0),
                             Letter(self.CanvasBG, text="S", column=2, row=0),
                             Letter(self.CanvasBG, text="Q", column=3, row=0),
                             Letter(self.CanvasBG, text="U", column=4, row=0),
                             Letter(self.CanvasBG, text="A", column=5, row=0),
                             Letter(self.CanvasBG, text="R", column=6, row=0),
                             Letter(self.CanvasBG, text="T", column=7, row=0),
                             Letter(self.CanvasBG, text="E", column=8, row=0),
                             Letter(self.CanvasBG, text="R", column=9, row=0)))
        self.Letters.append((Letter(self.CanvasBG, text="H", column=0, row=1),
                             Letter(self.CanvasBG, text="A", column=1, row=1),
                             Letter(self.CanvasBG, text="L", column=2, row=1),
                             Letter(self.CanvasBG, text="F", column=3, row=1),
                             Letter(self.CanvasBG, text="T", column=4, row=1),
                             Letter(self.CanvasBG, text="W", column=5, row=1),
                             Letter(self.CanvasBG, text="E", column=6, row=1),
                             Letter(self.CanvasBG, text="N", column=7, row=1),
                             Letter(self.CanvasBG, text="T", column=8, row=1),
                             Letter(self.CanvasBG, text="Y", column=9, row=1)))
        self.Letters.append((Letter(self.CanvasBG, text="F", column=0, row=2),
                             Letter(self.CanvasBG, text="I", column=1, row=2),
                             Letter(self.CanvasBG, text="V", column=2, row=2),
                             Letter(self.CanvasBG, text="E", column=3, row=2),
                             Letter(self.CanvasBG, text="T", column=4, row=2),
                             Letter(self.CanvasBG, text="E", column=5, row=2),
                             Letter(self.CanvasBG, text="N", column=6, row=2),
                             Letter(self.CanvasBG, text="T", column=7, row=2),
                             Letter(self.CanvasBG, text="I", column=8, row=2),
                             Letter(self.CanvasBG, text="L", column=9, row=2)))
        self.Letters.append((Letter(self.CanvasBG, text="P", column=0, row=3),
                             Letter(self.CanvasBG, text="A", column=1, row=3),
                             Letter(self.CanvasBG, text="S", column=2, row=3),
                             Letter(self.CanvasBG, text="T", column=3, row=3),
                             Letter(self.CanvasBG, text="T", column=4, row=3),
                             Letter(self.CanvasBG, text="W", column=5, row=3),
                             Letter(self.CanvasBG, text="E", column=6, row=3),
                             Letter(self.CanvasBG, text="L", column=7, row=3),
                             Letter(self.CanvasBG, text="V", column=8, row=3),
                             Letter(self.CanvasBG, text="E", column=9, row=3)))
        self.Letters.append((Letter(self.CanvasBG, text="T", column=0, row=4),
                             Letter(self.CanvasBG, text="W", column=1, row=4),
                             Letter(self.CanvasBG, text="O", column=2, row=4),
                             Letter(self.CanvasBG, text="S", column=3, row=4),
                             Letter(self.CanvasBG, text="I", column=4, row=4),
                             Letter(self.CanvasBG, text="X", column=5, row=4),
                             Letter(self.CanvasBG, text="F", column=6, row=4),
                             Letter(self.CanvasBG, text="O", column=7, row=4),
                             Letter(self.CanvasBG, text="U", column=8, row=4),
                             Letter(self.CanvasBG, text="R", column=9, row=4)))
        self.Letters.append((Letter(self.CanvasBG, text="T", column=0, row=5),
                             Letter(self.CanvasBG, text="H", column=1, row=5),
                             Letter(self.CanvasBG, text="R", column=2, row=5),
                             Letter(self.CanvasBG, text="E", column=3, row=5),
                             Letter(self.CanvasBG, text="E", column=4, row=5),
                             Letter(self.CanvasBG, text="E", column=5, row=5),
                             Letter(self.CanvasBG, text="I", column=6, row=5),
                             Letter(self.CanvasBG, text="G", column=7, row=5),
                             Letter(self.CanvasBG, text="H", column=8, row=5),
                             Letter(self.CanvasBG, text="T", column=9, row=5)))
        self.Letters.append((Letter(self.CanvasBG, text="E", column=0, row=6),
                             Letter(self.CanvasBG, text="L", column=1, row=6),
                             Letter(self.CanvasBG, text="E", column=2, row=6),
                             Letter(self.CanvasBG, text="V", column=3, row=6),
                             Letter(self.CanvasBG, text="E", column=4, row=6),
                             Letter(self.CanvasBG, text="N", column=5, row=6),
                             Letter(self.CanvasBG, text="O", column=6, row=6),
                             Letter(self.CanvasBG, text="O", column=7, row=6),
                             Letter(self.CanvasBG, text="N", column=8, row=6),
                             Letter(self.CanvasBG, text="E", column=9, row=6)))
        self.Letters.append((Letter(self.CanvasBG, text="F", column=0, row=7),
                             Letter(self.CanvasBG, text="I", column=1, row=7),
                             Letter(self.CanvasBG, text="V", column=2, row=7),
                             Letter(self.CanvasBG, text="E", column=3, row=7),
                             Letter(self.CanvasBG, text="N", column=4, row=7),
                             Letter(self.CanvasBG, text="I", column=5, row=7),
                             Letter(self.CanvasBG, text="N", column=6, row=7),
                             Letter(self.CanvasBG, text="E", column=7, row=7),
                             Letter(self.CanvasBG, text="Z", column=8, row=7),
                             Letter(self.CanvasBG, text="N", column=9, row=7)))
        self.Letters.append((Letter(self.CanvasBG, text="M", column=0, row=8),
                             Letter(self.CanvasBG, text="I", column=1, row=8),
                             Letter(self.CanvasBG, text="D", column=2, row=8),
                             Letter(self.CanvasBG, text="N", column=3, row=8),
                             Letter(self.CanvasBG, text="I", column=4, row=8),
                             Letter(self.CanvasBG, text="G", column=5, row=8),
                             Letter(self.CanvasBG, text="H", column=6, row=8),
                             Letter(self.CanvasBG, text="T", column=7, row=8),
                             Letter(self.CanvasBG, text="B", column=8, row=8),
                             Letter(self.CanvasBG, text="A", column=9, row=8)))
        self.Letters.append((Letter(self.CanvasBG, text="O'", column=0, row=9),
                             Letter(self.CanvasBG, text="C", column=1, row=9),
                             Letter(self.CanvasBG, text="L", column=2, row=9),
                             Letter(self.CanvasBG, text="O", column=3, row=9),
                             Letter(self.CanvasBG, text="C", column=4, row=9),
                             Letter(self.CanvasBG, text="K", column=5, row=9),
                             Letter(self.CanvasBG, text="D", column=6, row=9),
                             Letter(self.CanvasBG, text="J", column=7, row=9),
                             Letter(self.CanvasBG, text="P", column=8, row=9),
                             Letter(self.CanvasBG, text="M", column=9, row=9)))

        # There are two buttons, one for adjusting brightness, which runs the function changeBrightness (defined later)
        # and one for adjusting color, which runs the function changeColor (defined later)
        self.buttonColor = Button(self.master, text="color", command=self.changeColor, bg="#000000", fg="#333333",
                                  borderwidth=0, activeforeground="#FFFFFF", activebackground="#000000").pack(
            side=RIGHT)
        self.buttonBrightness = Button(self.master, text="brightness", command=self.changeBrightness, bg="#000000",
                                       fg="#333333", borderwidth=0, activeforeground="#FFFFFF",
                                       activebackground="#000000").pack(side=RIGHT)

        # The word instances here are individually defined. There are two "FIVE"'s, and two "TEN"'s. FIVE_1 and TEN_1
        # are each used in minute statements, FIVE_2 and TEN_2 are each used in hour statements. Two are necessary
        # for the cases of "IT'S FIVE TIL FIVE PM" for example. All other words are unique.
        #
        # There are 25 words, with several letter overlaps between them. For the letters which overlap, it's expected
        # for the letter to blink off and blink on during a transition, and not stay on.
        self.wordHALF = Word(self.Letters[1][0], self.Letters[1][1], self.Letters[1][2], self.Letters[1][3],
                             master=self.master)
        self.wordMIDNIGHT = Word(self.Letters[8][0], self.Letters[8][1], self.Letters[8][2], self.Letters[8][3],
                                 self.Letters[8][4], self.Letters[8][5], self.Letters[8][6], self.Letters[8][7],
                                 master=self.master)
        self.wordITS = Word(self.Letters[0][0], self.Letters[0][1], self.Letters[0][2], master=self.master)
        self.wordQUARTER = Word(self.Letters[0][3], self.Letters[0][4], self.Letters[0][5], self.Letters[0][6],
                                self.Letters[0][7], self.Letters[0][8], self.Letters[0][9], master=self.master)
        self.wordTWENTY = Word(self.Letters[1][4], self.Letters[1][5], self.Letters[1][6], self.Letters[1][7],
                               self.Letters[1][8], self.Letters[1][9], master=self.master)
        self.wordFIVE_1 = Word(self.Letters[2][0], self.Letters[2][1], self.Letters[2][2], self.Letters[2][3],
                               master=self.master)
        self.wordTEN_1 = Word(self.Letters[2][4], self.Letters[2][5], self.Letters[2][6], master=self.master)
        self.wordTIL = Word(self.Letters[2][7], self.Letters[2][8], self.Letters[2][9], master=self.master)
        self.wordPAST = Word(self.Letters[3][0], self.Letters[3][1], self.Letters[3][2], self.Letters[3][3],
                             master=self.master)
        self.wordTWELVE = Word(self.Letters[3][4], self.Letters[3][5], self.Letters[3][6], self.Letters[3][7],
                               self.Letters[3][8], self.Letters[3][9], master=self.master)
        self.wordTWO = Word(self.Letters[4][0], self.Letters[4][1], self.Letters[4][2], master=self.master)
        self.wordSIX = Word(self.Letters[4][3], self.Letters[4][4], self.Letters[4][5], master=self.master)
        self.wordFOUR = Word(self.Letters[4][6], self.Letters[4][7], self.Letters[4][8], self.Letters[4][9],
                             master=self.master)
        self.wordTHREE = Word(self.Letters[5][0], self.Letters[5][1], self.Letters[5][2], self.Letters[5][3],
                              self.Letters[5][4], master=self.master)
        self.wordEIGHT = Word(self.Letters[5][5], self.Letters[5][6], self.Letters[5][7], self.Letters[5][8],
                              self.Letters[5][9], master=self.master)
        self.wordELEVEN = Word(self.Letters[6][0], self.Letters[6][1], self.Letters[6][2], self.Letters[6][3],
                               self.Letters[6][4], self.Letters[6][5], master=self.master)
        self.wordNOON = Word(self.Letters[6][5], self.Letters[6][6], self.Letters[6][7], self.Letters[6][8],
                             master=self.master)
        self.wordONE = Word(self.Letters[6][7], self.Letters[6][8], self.Letters[6][9], master=self.master)
        self.wordFIVE_2 = Word(self.Letters[7][0], self.Letters[7][1], self.Letters[7][2], self.Letters[7][3],
                               master=self.master)
        self.wordTEN_2 = Word(self.Letters[5][9], self.Letters[6][9], self.Letters[7][9], master=self.master)
        self.wordSEVEN = Word(self.Letters[4][3], self.Letters[5][3], self.Letters[6][3], self.Letters[7][3],
                              self.Letters[8][3], master=self.master)
        self.wordNINE = Word(self.Letters[7][4], self.Letters[7][5], self.Letters[7][6], self.Letters[7][7],
                             master=self.master)
        self.wordOCLOCK = Word(self.Letters[9][0], self.Letters[9][1], self.Letters[9][2], self.Letters[9][3],
                               self.Letters[9][4], self.Letters[9][5], master=self.master)
        self.wordPM = Word(self.Letters[9][8], self.Letters[9][9], master=self.master)
        self.wordAM = Word(self.Letters[8][9], self.Letters[9][9], master=self.master)

        # Hours is the array of HStatement instances. There are two exceptions, MIDNIGHT and NOON, which were one word
        # each and as such did not require a full HStatement instance. These have been added to the array in a
        # specific order, so that the actual hour value can be used when calling the correct HStatement in the
        # updatetime function defined below.
        self.Hours = []
        self.Hours.append(self.wordMIDNIGHT)
        self.Hours.append(HStatement(self.wordONE, self.wordOCLOCK, self.wordAM))
        self.Hours.append(HStatement(self.wordTWO, self.wordOCLOCK, self.wordAM))
        self.Hours.append(HStatement(self.wordTHREE, self.wordOCLOCK, self.wordAM))
        self.Hours.append(HStatement(self.wordFOUR, self.wordOCLOCK, self.wordAM))
        self.Hours.append(HStatement(self.wordFIVE_2, self.wordOCLOCK, self.wordAM))
        self.Hours.append(HStatement(self.wordSIX, self.wordOCLOCK, self.wordAM))
        self.Hours.append(HStatement(self.wordSEVEN, self.wordOCLOCK, self.wordAM))
        self.Hours.append(HStatement(self.wordEIGHT, self.wordOCLOCK, self.wordAM))
        self.Hours.append(HStatement(self.wordNINE, self.wordOCLOCK, self.wordAM))
        self.Hours.append(HStatement(self.wordTEN_2, self.wordOCLOCK, self.wordAM))
        self.Hours.append(HStatement(self.wordELEVEN, self.wordOCLOCK, self.wordAM))
        self.Hours.append(self.wordNOON)
        self.Hours.append(HStatement(self.wordONE, self.wordOCLOCK, self.wordPM))
        self.Hours.append(HStatement(self.wordTWO, self.wordOCLOCK, self.wordPM))
        self.Hours.append(HStatement(self.wordTHREE, self.wordOCLOCK, self.wordPM))
        self.Hours.append(HStatement(self.wordFOUR, self.wordOCLOCK, self.wordPM))
        self.Hours.append(HStatement(self.wordFIVE_2, self.wordOCLOCK, self.wordPM))
        self.Hours.append(HStatement(self.wordSIX, self.wordOCLOCK, self.wordPM))
        self.Hours.append(HStatement(self.wordSEVEN, self.wordOCLOCK, self.wordPM))
        self.Hours.append(HStatement(self.wordEIGHT, self.wordOCLOCK, self.wordPM))
        self.Hours.append(HStatement(self.wordNINE, self.wordOCLOCK, self.wordPM))
        self.Hours.append(HStatement(self.wordTEN_2, self.wordOCLOCK, self.wordPM))
        self.Hours.append(HStatement(self.wordELEVEN, self.wordOCLOCK, self.wordPM))

        # Minutes is the array of MStatement instances. There is one exception, ITS, which is only one word, and did
        # not required a full MStatement instance. These have been added to the array in a specific order, so that the
        # actual minutes value can be used when calling the correct MStatement in the updatetime function defined
        # below. ITS TWENTY PAST and ITS HALF PAST were added twice, because the minute value increments in
        # five, but there is no TWENTY-FIVE PAST or THIRTY-FIVE PAST.
        self.Minutes = []
        self.Minutes.append(self.wordITS)
        self.Minutes.append(MStatement(self.wordITS, self.wordFIVE_1, self.wordPAST))
        self.Minutes.append(MStatement(self.wordITS, self.wordTEN_1, self.wordPAST))
        self.Minutes.append(MStatement(self.wordITS, self.wordQUARTER, self.wordPAST))
        self.Minutes.append(MStatement(self.wordITS, self.wordTWENTY, self.wordPAST))
        self.Minutes.append(MStatement(self.wordITS, self.wordTWENTY, self.wordPAST))
        self.Minutes.append(MStatement(self.wordITS, self.wordHALF, self.wordPAST))
        self.Minutes.append(MStatement(self.wordITS, self.wordHALF, self.wordPAST))
        self.Minutes.append(MStatement(self.wordITS, self.wordTWENTY, self.wordTIL))
        self.Minutes.append(MStatement(self.wordITS, self.wordQUARTER, self.wordTIL))
        self.Minutes.append(MStatement(self.wordITS, self.wordTEN_1, self.wordTIL))
        self.Minutes.append(MStatement(self.wordITS, self.wordFIVE_1, self.wordTIL))

    # adjustMinutes takes the actual minutes value, and modifies it to the correct index needed for the Minutes array.
    def adjustMinutes(self, minutes):
        return int(minutes / 5)

    # adjustHours takwes the actual hour and minutes value, and modifies it to the correct index needed for the Hours
    # array. The next hour is called when the clock read :40 or higher, because at that point the minute statement will
    # be reading "ITS TWENTY TIL" or less.
    def adjustHours(self, hour, minutes):
        if minutes < 8:
            return hour
        else:
            return hour + 1

    # changeColor uses loopAdd (see loopAdd function definition for more details) to shift the color selection to the
    # next color in the array, and then updates all active letters to the newly selected color. Active letters are
    # added to a temporary array, which is looped through, so that there is no delay between updated letters, other
    # than the configured delay for visual effect.
    def changeColor(self):
        activeLetters = []
        self.colorSelection = self.loopAdd(len(self.colorOptions), self.colorSelection)
        self.color = self.colorOptions[self.colorSelection][self.brightnessSelection]
        for i in range(0, 10):
            for j in range(0, 10):
                if self.Letters[i][j].getActive() is True:
                    activeLetters.append(self.Letters[i][j])
        for i in range(0, len(activeLetters)):
            activeLetters[i].setColor("#" + str(self.colorOptions[self.colorSelection][self.brightnessSelection]))
            self.master.update_idletasks()
            self.master.update()
            time.sleep(0.12)

    # changeBrightness uses loopAdd (see loopAdd function definition for more details) to shift the brightness selection
    # to the next (dim) color in the array, and then updates all active letters to the newly selected color. Active
    # letters are added to a temporary array, which is looped through, so that there is no delay between updated
    # letters, other than the configured delay for visual effect.
    def changeBrightness(self):
        activeLetters = []
        self.brightnessSelection = self.loopAdd(len(self.colorOptions[self.colorSelection]), self.brightnessSelection)
        self.color = self.colorOptions[self.colorSelection][self.brightnessSelection]
        for i in range(0, 10):
            for j in range(0, 10):
                if self.Letters[i][j].getActive() is True:
                    activeLetters.append(self.Letters[i][j])
        for i in range(0, len(activeLetters)):
            activeLetters[i].setColor("#" + str(self.colorOptions[self.colorSelection][self.brightnessSelection]))
            self.master.update_idletasks()
            self.master.update()
            time.sleep(0.12)

    # loopAdd takes the length of an array (maxloop) and the current index of the array being used (currentvalue) and
    # increments UP to the next value. If the currentvalue is the max value of the array, then loopAdd returns 0 to go
    # back to the beginning of the array. loopAdd is used in changeBrightness and changeColor in order to loop through
    # the options of the colors and brightness.
    def loopAdd(self, maxloop, currentvalue):
        if currentvalue < maxloop - 1:
            return currentvalue + 1
        else:
            return 0

    # loopSub takes the length of an array (maxloop) and the current index of the array being used (currentvalue) and
    # increments DOWN to the next value. If the currentvalue is 0, then loopSub retrns the max value of the array to go
    # back to the beginning. loopSub is used in updatetime to calculate the last hour and minute value, which is then
    # used to run fade_to_grey on the last HStatement and MStatement.
    def loopSub(self, maxloop, currentvalue):
        if currentvalue is 0:
            return maxloop - 1
        else:
            return currentvalue - 1

    # updatetime is the "bread and butter" of the program. This is where the time is evaluated, and the correct
    # HStatement and MStatement are faded to grey and color as appropriate.
    #
    # First, the minutes and hour are adjusted to correspond to the correct index in the Hours and Minutes arrays. This
    # is done by adjustMinutes and adjustHours. Because the minute statement is updated roughly every 5 minutes, the
    # minutes value is divided by 5. Because the hour statement changes the hour word at the :40 minute mark rather
    # than the :00 minute mark, the hour statement has to be bumped up at :40 minutes.
    #
    # Next, the last minute and last hour have to be calculated. For most cases, this will just be the adjusted minutes
    # and the adjusted hours - 1, but for cases where the current hour and/or minutes are 0, loopSub is ran to return
    # the max value in those cases, if appropriate.
    #
    # Finally, fade_to_grey is ran on the last minute and hour to turn them off, before turning on the current minute
    # and hour statement. fade_to_grey is only ran if the statement is currently active, so it should only be ran at
    # the time of change and not again. This prevents "blinking" behavior every time the clock re-checks the time, but
    # the time has not actually changed.
    #
    # fade_to_white is run every time, because once the statement is active, running fade_to_white again will not cause
    # any undesired behavior. The fade_to_white function in the word class is smart enough to only run if the word is
    # inactive, so as long as fade_to_grey was not run mistakenly, then fade_to_white can be run without any harm.
    #
    # updatetime is scheduled to run every 30 seconds. It does not actually run every 30 seconds. If a change in time
    # has occurred, updatetime will actually take quite awhile to run, accounting for all the delay times in fading
    # for every individual word. The 30 second time starts counting at the end of the last execution of updatetime, so
    # including run time for the execution, this can mean a delay of up to 50 seconds. This is why the function is
    # scheduled for every 30, this ensures that that the longest time the app will take to update on a change in time is
    # 29 seconds.
    def updatetime(self):
        minutes = self.adjustMinutes(int(time.strftime('%M', time.localtime())))
        hour = self.adjustHours(int(time.strftime('%H', time.localtime())), minutes)
        lastminute = self.loopSub(len(self.Minutes), minutes)
        if self.Minutes[lastminute].getActive() is True:
            self.Minutes[lastminute].fade_to_grey(self.color, minutes)
        self.Minutes[minutes].fade_to_white(self.color)
        lasthour = self.loopSub(len(self.Hours), hour)
        if self.Hours[lasthour].getActive() is True:
            self.Hours[lasthour].fade_to_grey(self.color, hour)
        self.Hours[hour].fade_to_white(self.color, minutes)
        self.master.after(30000, self.updatetime)


# main function creates an instance of Tk, and the application class defined above. Then it runs updatetime on the
# instance of Application.
def main():
    root = Tk()
    root.title("Word Clock")
    root.configure(background='black')
    app = Application(master=root)
    app.updatetime()
    root.mainloop()

# run it!
main()
