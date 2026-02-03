import concurrent.futures
import threading
import serial
import time

class SerialReader():
    def __init__(self, port, baudrate=9600, timeout=3, execute_close=True):
        #super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        #self.readings = ''
        self.ser = None
        self.running = False
        self.execute_close = execute_close
        self.ser = serial.Serial(self.port, self.baudrate, parity=serial.PARITY_NONE, timeout=0.10, xonxoff=1, rtscts=1)
        print(f'SerialReader init. {self.port}')
        if not self.ser.is_open:
            print('Serial port not open')

    def serial_read(self, run_time=3):
        #print('SerialRead start')
        readings = ''
        self.running = True
        start_time = time.time()
        #while self.running and (time.time() - start_time) < 5.0:
        while ((time.time() - start_time) < run_time) and self.running:
            if self.ser.in_waiting > 0:
                #self.readings += self.ser.readline(self.ser.in_waiting).decode()
                readings += self.ser.readline(self.ser.in_waiting).decode()
            time.sleep(0.01)  # Brief sleep to prevent high CPU usage [web:17]
        if self.ser and self.execute_close:
            self.ser.close()
            print('SerialRead stop. Serial Close')
        return readings

    def settings(self, timeout, execute_close):
        print('Settings')
        self.timeout = timeout
        self.execute_close = execute_close

    def execute(self, task_func=None, *task_args, **task_kwargs):
        """
        Run task_func synchronously while reading serial concurrently.
        Returns (task_result, serial_data, serial_error).
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Submit serial read and task concurrently
            serial_future = executor.submit(self.serial_read, self.timeout)
            if task_func:
                task_future = executor.submit(task_func, *task_args, **task_kwargs)
                task_result = task_future.result()
            else:
                task_result = None

            serial_data = serial_future.result()

        print('execute complete')
        return task_result, serial_data


