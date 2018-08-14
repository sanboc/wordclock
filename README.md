# wordclock
Python tkinter application which displays time using words. Allows for changing color and brightness.

FUNCTIONAL DESCRIPTION:
10x10 letter "word search" format clock face. Approximates time to 5-10 minutes:
--:00 - :04 : IT'S xx O'CLOCK yy
--:05 - :09 : IT'S FIVE PAST xx yy
--:10 - :14 : IT'S TEN PAST xx yy
--:15 - :19 : IT'S QUARTER PAST xx yy
--:20 - :29 : IT'S TWENTY PAST xx yy
--:30 - :39 : IT'S HALF PAST xx yy
--:40 - :44 : IT'S TWENTY TIL zz yy
--:45 - :49 : IT'S QUARTER TIL zz yy
--:50 - :54 : IT'S TEN TIL zz yy
--:55 - :59 : IT'S FIVE TIL zz yy

Where xx = current hour, yy = AM/PM, and zz = next hour. MIDNIGHT and NOON are used in place of TWELVE AM and TWELVE PM.

Clock face displays a black background with dark gray, capital letters at initialization. The current time then fades into view in bright white. When the time changes to require the next "word" time, the old words fade to dark gray, and the new words fade in to white. Any words which must be active for both the old time and the new time will stay active during the transition.

FEATURE DESCRIPTION:
Two buttons in the bottom right allow the user to toggle between seven colors (White, Green, Red, Violet, Indigo, Yellow, and Blue) and three brightness selections (fully bright, dimmed, and off).
