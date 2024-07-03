import json
import os
from dotenv import load_dotenv

from getgauge.python import step, data_store, Table, Messages

from automation.x3270_emulator import Robo3270Emulator as ISPFEmulator


@step("Setup environment")
def setup_environment():
    load_dotenv()


@step("Open wc3270 emulator")
def open_wc3270_emulator():
    em = ISPFEmulator(visible=True)
    data_store.scenario["emulator"] = em


@step("Connect to the host")
def connect_to_host():
    em = data_store.scenario["emulator"]
    HOST = os.getenv("MAINFRAME_HOST")
    PORT = int(os.getenv("MAINFRAME_PORT"))
    em.connect_to_host(HOST, PORT)


@step("Login to IBM Z Xplore learning platform")
def login_to_ibm_z_xplore_learning_platform():
    em = data_store.scenario["emulator"]
    username = os.getenv("MAINFRAME_USER")
    pswd = os.getenv("MAINFRAME_PASS")
    em.login(username, pswd)
    data_store.scenario["username"] = username


@step("Go to the Utilities menu")
def go_to_the_utilities_menu():
    em = data_store.scenario["emulator"]
    em.send_option("3")


@step("Go to Data Set List Utility")
def go_to_data_set_list_utility():
    em = data_store.scenario["emulator"]
    em.send_option("4")


@step("Set Dsname Level to <name> and press Enter")
def set_dsname_level_and_press_enter(name: str):
    em = data_store.scenario["emulator"]
    em.set_field("Dsname Level", name)


@step("Capture the list of datasets")
def capture_the_list_of_datasets():
    em = data_store.scenario["emulator"]
    data_store.scenario["data_sets"] = em.get_data_sets()


@step("Dump data sets to <filepath>")
def dump_data_sets_to_file(file_path: str):
    ds = data_store.scenario["data_sets"]
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w") as file:
        json.dump(ds, file, indent=2)


@step("The list should contain the following datasets: <table>")
def the_list_should_contain_the_following_datasets(table: Table):
    values = table.get_column_values_with_name("Dataset Name")
    ds_list = data_store.scenario["data_sets"]["ds_list"]
    for v in values:
        assert v in ds_list, f"Dataset {v} not found in the list"


@step("View <dataset_name> dataset")
def view_the_dataset(dataset: str):
    em = data_store.scenario["emulator"]
    em.view_data_set(dataset)


@step("Find and open the record named <name>")
def find_and_open_the_record_named(name: str):
    em = data_store.scenario["emulator"]
    em.open_record(name)


@step("Capture the text from the record")
def capture_the_text_from_the_dataset():
    em = data_store.scenario["emulator"]
    data_store.scenario["dataset_text"] = em.get_record_contents_as_text()

@step("Dump record content to <file>")
def dump_record_content_to(file: str):
    text = data_store.scenario["dataset_text"]
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file), exist_ok=True)

    with open(file, "w") as f:
        f.write(text)

@step("The text should start with <text>")
def the_text_should_start_with(text):
    text = data_store.scenario["dataset_text"]
    assert text.startswith(text), f"Expected text: {text} not found in the dataset"


@step("Go back to the main ISPF menu")
def go_back_to_the_main_ispf_menu():
    em = data_store.scenario["emulator"]
    em.go_to_main_menu()


@step("Log off from the mainframe")
def log_off_from_the_mainframe():
    em = data_store.scenario["emulator"]
    em.go_to_main_menu()
    try:
        em.send_option("X")
    except ConnectionResetError as e:
        Messages.write_message(f"Connection error: {e.strerror}. ")
    finally:
        em.close()
