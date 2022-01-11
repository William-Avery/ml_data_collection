from threading import Thread
from helpers.data_helper import DataHelper

if __name__ == '__main__':
    # Initialize datagrabbing
    data_session = DataHelper()
    t2 = Thread(target=data_session.init_datarecorder)

    #t1.start()
    t2.start()
    #t1.join()
    t2.join()