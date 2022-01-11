from helpers.data_helper import DataHelper

if __name__ == '__main__':
    # Initialize datagrabbing
    data_session = DataHelper("tree_cutting")
    data_session.start_recording()