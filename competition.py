#!/usr/bin/env python3

# 'annotations' are imported here so that
# methods within a class can reference the parent class.
#
# 'Enum' is imported here to... well, construct an Enum.
from __future__ import annotations
from enum import Enum

"""
  ==========================================
 |             General Utility              |
  ==========================================
"""
class ANSI_SEQ(Enum):
    """ An enum storing ANSI escape sequences for this project. """

    RED = "\033[95m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END_FMT = "\033[0m"

class Util:
    """ An abstract class holding all auxiliary, general utility functionality. """

    def __init__(self):
        raise RuntimeError("[UTIL]: 'Util' class should never be insantiated as it is abstract!")

    def format_text(
        text: str = "",
        color: str = "",
        fmt: str = ""
    ) -> str:
        """
        Formats the given text, with the given colour and/or format.

        Viable values for 'color':
            * red
            * green
            * yellow

        Viable values for 'fmt':
            * bold
            * underline
            * bold+underline

        Returns an empty string if something went wrong.
        """

        # If there is no text, or,
        # if there is no colour and format value,
        # return the original text/empty string.
        if (
            not text or
            (not color and not fmt)
        ):
            return text

        if (
            color and
            # Only apply colour patches if
            # the colour value is valid.
            (
                "red" == color.lower() or
                "green" == color.lower() or
                "yellow" == color.lower()
            )
        ):
            text = f"{ANSI_SEQ[color.upper()].value}{text}{ANSI_SEQ.END_FMT.value}"

        if fmt:
            # Only apply formats if they're
            # valid format values.bin(number)
            if "bold" in fmt.lower():
                text = f"{ANSI_SEQ.BOLD.value}{text}"
            
            if "underline" in fmt.lower():
                text = f"{ANSI_SEQ.UNDERLINE.value}{text}"

            # Necessary END_FMT escape seq.
            text += ANSI_SEQ.END_FMT.value
        
        return text

"""
  ==========================================
 |       Second Largest Int in List         |
  ==========================================
"""
class SNDL:
    """
    An instance holding all the auxiliary methods 
    for extracting the 2nd largest integer from
    an ambiguous list.
    """

    def __init__(self):
        pass

    def second_largest(
        self,
        data: list,
        ext_method: str = "manual"
    ) -> int | None:
        """
        Extracts the second largest number from a given list.

        Method allows for 2 "types" of extraction:
            - `manual` — uses a custom method, defined in the parent class.
            - `built-in` — uses `sorted()`, which is built into Python.
        """

        # Small check to ensure
        # we're dealing with a list
        # that contains at least a singular
        # integer value in it.
        try:
            self.check_int_list(data)
        except RuntimeError:
            return None

        data = self.filter_int_ambiguous_list(data)

        if ext_method.lower() == "manual":

            # Returns a new list - contains all the integers inside
            # of the 'data' list.
            #
            # Sorted from highest -> lowest.
            return self.sort_int_list(data)[1]

        elif ext_method.lower() == "built-in":
            # Here, we first use 'sorted()' to sort
            # the list of integers in ascending order.
            #
            # We could use the 'reversed()' method to
            # yield an iterator, which corresponds to the
            # ordered list, but this time in reverse order.
            #
            # With that iterator, we can convert it to a pythonic
            # list by using the `list()` constructor to instantiate it as one.
            #
            # However, that shouldn't be necessary since the built-in `sorted()`
            # method already has a parameter which will sort the 
            # list in descending order.
            #
            # An alternative approach to this would be:
            #       * data.sort(reverse=True); data[1]
            #
            # Benefit over the current method:
            #   * Not any that I know of.
            # 
            # Drawback over the current method:
            #   * Mutates the original list during runtime.
            return sorted(data, reverse=True)[1]

    def sort_int_list(
        self,
        target: list[int],
    ) -> list[int]:
        """ Sorts a list of integers in descending order. """

        if not target:
            return []

        return self.merge_sort(target)

    def merge_sort(self, target: list) -> list:
        """
        Uses the 'merge sort' algorithm to sort a
        list of integers in descending order.

        Time complexity:
            - Best-case: `O(n log n)`
            - Worst-case: `O(n log n)`
        
        Space complexity: `O(n)`
        """

        # If the list is empty, or doesn't exist,
        # return an empty list.
        if not target:
            return []
            
        length = len(target)

        if length == 1:
            return target

        # The integer division operator (`//`) allows
        # for us to round the value to an integer,
        # instead of it remaining as a float.
        #
        # `mid_pt` is the index of the middle
        # of the list provided.
        mid_pt = length // 2

        # Left partition of the list.
        left = self.merge_sort(target[:mid_pt])

        # Right partition of the list.
        right = self.merge_sort(target[mid_pt:])

        # The actual part where we define
        # which value will be the head,
        # and which one will the tail.
        #
        # In this case:
        #   - `tail` — the lower integer
        #   - `head` — the higher integer
        merged = []
        i = k = 0

        while i < len(left) and k < len(right):
            # If the left partition's value
            # is greater than the right one's,
            # we'll want to append the left part's value
            # because we're doing it in descending order.
            #
            # For ascending order, the condition would be:
            #       left[i] < right[k]
            if left[i] > right[k]:
                merged.append(left[i])
                i += 1
            
            else:
                merged.append(right[k])
                k += 1

        # This will alter the `merged` value
        # in a way where it'll retain its previous
        # values, while also adding the new ones.
        #
        # Alternative:
        #   `merged.extend(left[i:])`   along with:
        #   `merged.extend(right[k:])`
        merged = [
            *merged,
            *left[i:],
            *right[k:]
        ]
        
        return merged

    def filter_int_ambiguous_list(self, target: list) -> list[int]:
        """ Filters out non-integer values from an ambiguous-typed list. """

        # If the list is empty, or not a list
        # return an empty list.
        if not target:
            return []

        # In case the first element isn't
        # an integer; skip over it.
        if type(target[0]) != int:
            return self.filter_int_ambiguous_list(target[1:])

        # What this part does is it
        # adds the first element of 'target'
        # to its return value—a list—and
        # calls itself until 'target' is essentially empty.
        #
        # It expands the return value (a list)
        # into the parent return value (again, a list)
        return [
            target[0],
            *self.filter_int_ambiguous_list(target[1:])
        ]

    def check_int_list(self, target: list) -> None | RuntimeError:
        """ Verifies that a list contains at least a singular integer value. """

        if (
            # In Python, empty lists are
            # treated as falsy values.
            #
            # Which is why we can use the 'not'
            # operator to convert it into its
            # opposite boolean value.
            not target or
            type(target) != list or
            not any(type(x) == int for x in target)
        ):
            raise RuntimeError(
                "[2ND-L]: 'target' value is incomplete or doesn't contain an integer value!")

        # This explicit return statement
        # isn't necessary; since returning
        # no value in a function implicitly
        # returns 'None'; but it's done here
        # for the sake of clarity anyway.
        return None

"""
  ==========================================
 |            Grading Exam papers           |
  ==========================================
"""
class Questions:
    """
    An instance to hold marks for each question.

    There can only be 5 questions; no more, no less.
    """

    def __init__(
        self,
        first: int = 0,
        second: int = 0,
        third: int = 0,
        fourth: int = 0,
        fifth: int = 0
    ):
        if (
            type(first) != int or
            type(second) != int or
            type(third) != int or
            type(fourth) != int or
            type(fifth) != int
        ):
            raise RuntimeError("[EXAMS]: All values for a 'Questions' instance must be an integer!")
        
        if (
            self.check_condition(first) or
            self.check_condition(second) or
            self.check_condition(third) or
            self.check_condition(fourth) or
            self.check_condition(fifth)
        ):
            raise RuntimeError("[EXAMS]: Value for any question's mark mustn't be below 0, or above 100!")

        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth
        self.fifth = fifth

    def check_condition(self, question: int) -> bool:
        """ Ensures that the question's marks are in proper bounds. """

        return question > 100 or question < 0

    def get_marks_list(self) -> list[tuple]:
        """ Packs the marks into a defined list of tuples. """
        
        return [
            ("first",   self.first),
            ("second",  self.second),
            ("third",   self.third),
            ("fourth",  self.fourth),
            ("fifth",   self.fifth)
        ]

class GRADE_RANGE(Enum):
    """
    All grade ranges; sorted from min->max.
    
    To be quite frank, this could've been
    achieved using a tuple, nested list,
    a dictionary, etc. - instead of its own Enum.
    
    But I feel as if an Enum has the most sense to use here.
    """

    GRADE_A = (90, 100)
    GRADE_B = (80, 89)
    GRADE_C = (70, 79)
    GRADE_D = (60, 69)
    GRADE_F = (0, 60)

class Exam:
    """ An instance for grading and validating exam papers. """

    def __init__(
        self,
        marks: list[tuple] = []
    ):
        if marks:
            validated = self.__validate_marks(marks)

            if validated.get("questions", -1) != 5:
                raise RuntimeError("[EXAMS]: Incomplete marks provided; only marks for 5 questions necessary!")
            
            elif validated.get("highest_mark", -1) > 100:
                raise RuntimeError("[EXAMS]: Highest mark for a question can be 100, not greater than that!")

            elif validated.get("lowest_mark", -1) < 0:
                raise RuntimeError("[EXAMS]: Lowest mark for a question can be 0, not lower than that!")

        # Assign marks value to this instance
        # if there is such a parameter provided.
        #
        # This property does not have higher priority
        # for its instance's `grade_paper()` method.
        self.marks = [] if not marks else marks

        self.indexed = [
            "first",
            "second",
            "third",
            "fourth",
            "fifth"
        ]

    def get_marks(self, question_index: int = 0) -> Exam:
        """ Interactively obtains marks for each question from the user. """

        if question_index > 4:
            return self

        amount = input(f"Marks for question #{question_index + 1}: ")

        if not self.__validate_mark_range(int(amount)):
            print(
                Util.format_text(
                    "ERR: Invalid amount! Mark are only between 0-100 (both valeus inclusive); try again!",
                    "red",
                    "underline"
                )
            )
            return self.get_marks(question_index)

        self.marks.append(
            (self.indexed[question_index], int(amount))
        )

        return self.get_marks(question_index + 1)

    def grade_paper(
        self, 
        marks: list[tuple] = [], 
        inclusive: bool = False
    ) -> str | None:
        """
        Grades an exam paper based on the total of every question's marks. 

        Returns None if no marks are provided.

        Additional information:
            - `inclusive` parameter allows for grade ranges to include
                          max and min range to be accepted as the upper grade.
                          Will always target higher grade this way.
                          Set to 'False' by default.
        """
        from math import ceil

        if self.marks:
            # Use class's assigned marks
            # in the very case that this method
            # isn't being used to deal with arbitrary data.
            if not marks:
                marks = self.marks
        else:
            # No marks at all? No grade that can be provided.
            return None

        # Rounds in favour of a higher mark, if such be a case.
        #
        #   89.2 -> 90
        #   89.6 -> 90
        #   89.1 -> 90
        total = ceil(sum([x[1] for x in marks]) / len(marks))
        grade = ""

        # A little work-around.
        if (
            total % 10 == 0 or
            total == 0 or
            "9" in str(total)
        ):
            inclusive = True
        
        for RANGE in GRADE_RANGE:
            if inclusive:
                if self.__grade_condition(total, RANGE.value, inclusive):
                    if (
                        not grade or 
                        GRADE_RANGE[grade].value[0] < RANGE.value[0]
                    ):
                        grade = RANGE.name

            elif self.__grade_condition(total, RANGE.value):
                grade = RANGE.name
            
            # This should never be reached.
            else:
                continue

        return grade.replace("GRADE_", "")

    def __validate_marks(self, marks: list[tuple]) -> dict:
        """ Private method to ensure that the marks are properly constructed. """

        present = 0
        highest = 0
        lowest = 0

        for mark in marks:
            if (
                "first" == mark[0].lower() or
                "second" == mark[0].lower() or
                "third" == mark[0].lower() or
                "fourth" == mark[0].lower() or
                "fifth" == mark[0].lower()
            ):
                present += 1

            if mark[1] > 100:
                highest = mark[1]
            
            if mark[1] < 0:
                lowest = mark[1]

        return {
            "questions": present,
            "highest_mark": highest,
            "lowest_mark": lowest
        }

    def __validate_mark_range(self, mark: int) -> bool:
        """ Checks to see if the marks for a question is in proper bounds. """
        return mark <= 100 and mark >= 0
    
    def __grade_condition(
        self, 
        mark,
        mark_range: tuple = (-1, -1),
        inclusive: bool = False
    ) -> bool:
        """ Validates if the mark falls under the given range. """
        if mark_range == (-1, -1):
            return False

        return (
            (mark >= mark_range[0] and
            mark <= mark_range[1])
            if inclusive
            else (
                mark > mark_range[0] and
                mark < mark_range[1]
            )
        )

"""
  ==========================================
 |              Puzzle Word game            |
  ==========================================
"""
class PZWGame:
    """
    A Puzzle Word game handler.

    Principle of the PZW Game:
        User is provided a randomly generated set of letters
        by the program; they must guess a word which contains
        said letters.
        After a specific threshold (how many letters they guessed),
        it determines whether or not the user has won.

    Drawbacks:
        * No real word validation (words can be non-existent.)
        * Ambiguity as to whether or not a 100% threshold is an illegal case
    """
    def __init__(self):
        self.letters = []

        import random
        import string

        i = 0
        while i != 5:
            letter = random.choice(string.ascii_lowercase)
            if letter in self.letters:
                continue

            self.letters.append(letter)
            i += 1

    def run_game(
        self, 
        affirm_order: bool = False
    ) -> None:
        """
        Runs the Puzzle Word game.

        Additional info:
            * `affirm_order` — requires the user to come up with a word
                               where the sequence of the randomly generated
                               letters must remain absolute.
                               Example: 
                               Letters are: ['a', 'b', 'c', 'd', 'e']
                               User must come up with a word to respect the sequence.
                               Valid: [ 'game', 'fame' ]
                               Invalid: [ 'great', 'each' ]
        """

        letters = self.letters

        print(
            "The following letters are provided: " +
            Util.format_text(
                " - ".join(letters),
                "yellow",
                "bold"
            ) +
            "\n"
        )
        answer = input(
            "Try to guess a word (1-6 letters) which contains the aforementioned letters: "
        )

        if (
            len(answer.strip()) < 1 or
            len(answer.strip()) > 6
        ):
            print(
                Util.format_text(
                    "ERR! Invalid answer! Word can only contain 1-6 letters. Try again.\n",
                    "red",
                    "underline"
                )
            )
            return self.run_game(letters)

        return self.__validate_answer(answer.strip(), letters, affirm_order)

    def __validate_answer(
        self, 
        ans: str, 
        letters: list[str],
        affirm_order: bool = False
    ) -> None:
        """ Ensures that the answer provided by the user is valid; if not, prompt them again. """
        matches = []

        for letter in letters:
            if letter.lower() in ans.lower():
                matches.append(letter)

        if not matches:
            print(
                Util.format_text(
                    f"'{ans}' contains no matching letters!",
                    "red",
                    "bold+underline"
                )
            )

            ans = input("Please try to guess again: ")
            return self.__validate_answer(ans, letters)

        if len(matches) > 1:
            if affirm_order:
                indices = [
                    ans.lower().index(letter.lower())
                    for letter in matches
                ]

                for i in range(len(indices)):
                    if (i + 1) == len(indices):
                        break
                        
                    if indices[i] > indices[i + 1]:
                        print(
                            Util.format_text(
                                f"'{ans}' does not respect the letter order!\n",
                                "red",
                                "bold+underline"
                            ) +
                            f"Example letters: {Util.format_text('a - b - c - d - e', 'yellow')}\n"
                            f"Valid outputs: {Util.format_text('[ game, fame, date ]', 'yellow')}\n"
                            f"Invalid outputs: {Util.format_text('[ great, feat ]', 'yellow')}\n"
                        )

                        ans = input("Please try to guess again: ")
                        return self.__validate_answer(ans, letters)
                    
            print(
                f"'{ans}' contains a sufficient amount of letters: {', '.join(matches)}!\n" +
                Util.format_text(
                    "Congratulations, you won!", 
                    "green", 
                    "bold+underline"
                )
            )
            return
        else:
            print(
                Util.format_text(
                    f"'{ans}' does not contain a sufficient amount of letters (ONLY {len(matches)})!\n",
                    "red",
                    "underline"
                )
            )

            ans = input("Please try to guess again: ")
            return self.__validate_answer(ans, letters)

"""
///===============================================
///                 UNIT TESTS
///===============================================
"""          

"""
  ==========================================
 |       Second Largest Int in List         |
  ==========================================
"""

#
#   Proper cases:
#
print(
    "Data: [\"xd\", 12, 5, 34, 75, 8, None, 11]\n" +
    "Additional arguments: None\n" +
    "Result:", SNDL().second_largest(["xd", 12, 5, 34, 75, 8, None, 11]), "\n" +
    "Expected:", sorted([12, 5, 34, 75, 8,11])[-2], "\n" +
    "Details: None\n"
)
print(
    "Data: [\"xd\", 12, 5, 34, 75, 8, None, 11]\n" +
    "Additional arguments: ext_format='built-in'\n" +
    "Result:", SNDL().second_largest(["xd", 12, 5, 34, 75, 8, None, 11], "built-in"), "\n" +
    "Expected:", sorted([12, 5, 34, 75, 8,11])[-2], "\n" +
    "Details: None\n"
)

#
#   Edge cases:
#
print(
    "Data: [\"xd\", None, SNDL(), SNDL, \"test!\"]\n" +
    "Additional arguments: None\n" +
    "Result:", SNDL().second_largest(["xd", None, SNDL(), SNDL, "test!"]), "\n" +
    "Expected: None\n" +
    "Details: Provided a list with no integers\n"
)


"""
  ==========================================
 |            Grading Exam papers           |
  ==========================================
"""
questions = Questions(
    67,
    78,
    30,
    90,
    89
)

#
#   Proper cases:
#
print(
    "Data: Questions(67, 78, 30, 90, 89)\n" +
    "Additional arguments: None\n" +
    "Result:", Exam(questions.get_marks_list()).grade_paper(), "\n" +
    "Expected: C\n" +
    "Details: None\n"
)
print(
    'Data: [ ("first", 100), ("second", 100), ("third", 100), ("fourth", 100), ("fifth", 100) ]\n' +
    "Additional arguments: None\n" +
    "Result:", Exam([ ("first", 100), ("second", 100), ("third", 100), ("fourth", 100), ("fifth", 100) ]).grade_paper(), "\n" +
    "Expected: A\n" +
    "Details: None\n"  
)

#
#   Edge cases:
#
try:
    Exam([ ("first", 100) ])
except RuntimeError:
    print("[EXAMS]: Edge case #1 works as expected.")

try:
    Exam([ ("first", 100), ("second", 105), ("third", 100), ("fourth", 100), ("fifth", 100) ])
except RuntimeError:
    print("[EXAMS]: Edge case #2 works as expected.")

try:
    Exam([ ("first", 100), ("second", -2), ("third", 100), ("fourth", 100), ("fifth", 100) ])
except RuntimeError:
    print("[EXAMS]: Edge case #3 works as expected.")

#
#   Assigned cases (user input):
#
print(
    Exam().get_marks().grade_paper(),
    "\n"
)

"""
  ==========================================
 |              Puzzle Word game            |
  ==========================================
"""
#
#   Assigned cases (user input):
#
print("RUNNING PZW GAME...")
print("Run #1: 'affirm_order' is None.\n")
pzw_first = PZWGame()
pzw_first.run_game()
print("\n")

print("RUNNING PZW GAME AGAIN...")
print("Run #2: 'affirm_order' is turned on.")
pzw_second = PZWGame()
pzw_second.run_game(affirm_order=True)