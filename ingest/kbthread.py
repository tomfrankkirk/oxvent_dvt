import threading

class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.daemon = True
        self.start()

    def run(self):

        self.input_cbk(input()) #waits to get input + Return
            