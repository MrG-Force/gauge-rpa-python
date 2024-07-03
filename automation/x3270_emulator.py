from enum import Enum
import time
from Mainframe3270 import Emulator


class Direction(Enum):
    UP = b"PF(7)"
    DOWN = b"PF(8)"


class Robo3270Emulator:
    '''A class that wraps the Mainframe3270.Emulator class to perform operations on the ISPF interface.'''

    HEIGHT: int
    WIDTH: int

    def __init__(self, visible: bool = True, model: str = "4"):
        self.emulator = Emulator(visible=visible, model=model)
        self.HEIGHT = self.emulator.model_dimensions["rows"]
        self.WIDTH = self.emulator.model_dimensions["columns"]

    def connect_to_host(self, host: str, port: int = 23):
        self.emulator.connect('%s:%d' % (host, port))
        self.emulator.wait_for_field()

    def login(self, user: str, password: str):
        command = f'logon {user}'.encode("utf-8")
        self.emulator.send_string(command, 24, 1)
        self.send_enter()

        password = password.encode("utf-8")
        self.emulator.fill_field(8, 20, password, 8)
        self.send_enter()
        self.send_enter()
        self.send_enter()

    def send_option(self, option: str):
        self.emulator.send_string(option.encode("utf-8"))
        self.send_enter()
        if self.emulator.search_string("Invalid option"):
            raise ValueError(f"Invalid option: {option}")

    def send_enter(self):
        self.emulator.send_enter()
        self.emulator.wait_for_field()

    def find_field(self, field_name: str) -> tuple:
        '''Find the coordinates of the input field matching the field name.

        field_name
            The field name is the text that appears before the input field. For example
        the 'Dsname Level' field in the ISPF Data Set List Utility looks like this:

        `Dsname Level . . . ____________`

        It is assumed that all the input fields are preceded by a sequence of dots and spaces.
        '''

        # Find the coordinates of the strings matching the field name
        positions = self.emulator.get_string_positions(field_name)
        if not positions:
            raise ValueError(f"Field not found: {field_name}")

        # positions is a list of tuples (ypos, xpos)
        for pos in positions:
            ypos = pos[0]
            xpos = None
            string_starts = pos[1]
            string_ends = string_starts + len(field_name)
            for x in range(string_ends + 1, string_ends + 3):
                if self.emulator.string_get(ypos, x, 1) == ".":
                    # Found the field
                    # Skip one space and check if there is a dot
                    while x < 80:
                        x += 2
                        if self.emulator.string_get(ypos, x, 1) != ".":
                            # Found the start of the input field
                            xpos = x
                            break
                else:
                    continue
            if xpos:
                return ypos, xpos

        raise ValueError(f"Field not found: {field_name}")

    def set_field(self, field_name: str, value: str):
        ypos, xpos = self.find_field(field_name)
        self.emulator.move_to(ypos, xpos)
        self.emulator.delete_field()
        self.emulator.send_string(value.encode("utf-8"))
        self.send_enter()

    def get_data_sets(self) -> dict:
        """Get the list of datasets from the ISPF Data Set List Utility."""
        header: str = self.emulator.string_get(3, 2, 79)
        # The header contains size of list as 'Row 1 of <count>'
        row_count_index = header.index("Row")
        data_set_count = int(header[row_count_index + 8:].strip())
        # e.g ' DSLIST - Data Sets Matching <Dsname Level>
        list_title = header[0:row_count_index].strip()

        data_sets = {}
        data_sets["title"] = list_title
        data_sets["length"] = data_set_count
        data_sets["ds_list"] = []

        # the column containing the dataset names starts at
        col_starts = 11
        col_width = 45
        # Just before the line with 'Command ===> '
        bottom_limit = self.HEIGHT - 2
        # First dataset is at row
        i = 7
        # To scroll or not to scroll
        last_screen = self.emulator.search_string("* End ")
        while not last_screen:
            last_screen = self.emulator.search_string("* End ")
            for i in range(7, bottom_limit):
                if last_screen:
                    if self.emulator.string_get(i, 2, 1) == "*":
                        break
                ds_name = self.emulator.string_get(i, col_starts, col_width)
                data_sets["ds_list"].append(ds_name.strip())
            self.scroll(Direction.DOWN)

        return data_sets

    def view_data_set(self, dataset: str):
        pos = self.emulator.get_string_positions(dataset)
        if len(pos) == 0:
            raise ValueError(f"Dataset not found: {dataset}")

        ypos = pos[0][0]
        xpos = pos[0][1] - 2

        self.emulator.send_string("V".encode("utf-8"), ypos, xpos)
        self.send_enter()

    def search_record(self, record_name: str) -> tuple:
        positions = self.emulator.get_string_positions(record_name)
        found = len(positions) > 0
        is_last_screen = self.emulator.search_string("End")
        if not found and is_last_screen:
            return None
        elif not found:
            self.scroll(Direction.DOWN)
            return self.search_record(record_name)
        else:
            return positions[0]

    def open_record(self, record_name: str):
        pos = self.search_record(record_name)
        if not pos:
            raise ValueError(f"Record not found: {record_name}")
        ypos = pos[0]
        xpos = pos[1] - 2
        self.emulator.send_string("V".encode("utf-8"), ypos, xpos)
        self.send_enter()

    def get_record_contents_as_text(self) -> str:
        text = ""
        top_limit = self.emulator.get_string_positions("Top of Data")[0][0] + 1
        bottom_limit = self.HEIGHT - 2
        bottom_visible = False
        is_first_screen = True
        while not bottom_visible:
            bottom_visible = self.emulator.search_string("Bottom of Data")
            for i in range(top_limit, bottom_limit):
                if is_first_screen:
                    if self.emulator.string_get(i, 2, 6) == "==MSG>":
                        continue
                if bottom_visible and self.emulator.string_get(i, 2, 1) == "*":
                    break
                text += self.emulator.string_get(i, 9, 72)
                text += "\n"
            if bottom_visible:
                break
            self.scroll(Direction.DOWN)
            top_limit = 4
            is_first_screen = False

        return text

    def scroll(self, direction: Direction):
        self.emulator.exec_command(direction.value)
        self.emulator.wait_for_field()

    def go_to_main_menu(self):
        if self.emulator.search_string("ISPF Primary Option Menu"):
            return
        self.emulator.exec_command(b"PF(3)")
        self.emulator.wait_for_field()
        self.go_to_main_menu()

    def close(self):
        time.sleep(1)
        self.emulator.terminate()
        self.emulator = None