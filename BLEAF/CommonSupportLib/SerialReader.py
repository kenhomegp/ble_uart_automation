import concurrent.futures
import threading
import serial
import time
import re

class SerialReader():
    def __init__(self, port1, port2='', baudrate=9600, timeout=3, execute_close=True, dut_only=False):
        #super().__init__()
        self.port = port1
        self.baudrate = baudrate
        self.timeout = timeout
        #self.readings = ''
        self.ser = None
        self.running = False
        self.execute_close = execute_close
        if not dut_only:
            self.ser = serial.Serial(self.port, self.baudrate, parity=serial.PARITY_NONE, timeout=0.10, xonxoff=1, rtscts=1)
            print(f'SerialReader init. {self.port}')
            if not self.ser.is_open:
                print(f'Serial port not open.{self.port}')
        else:
            self.timeout = 10
            self.ser1 = serial.Serial(port1, self.baudrate, parity=serial.PARITY_NONE, timeout=0.10, xonxoff=1,
                                     rtscts=1)
            print(f'SerialReader init.{port1}')
            if not self.ser1.is_open:
                print(f'Serial port not open:{port1}')
            self.ser2 = serial.Serial(port2, self.baudrate, parity=serial.PARITY_NONE, timeout=0.10, xonxoff=1,
                                      rtscts=1)
            print(f'SerialReader init.{port2}')
            if not self.ser2.is_open:
                print(f'Serial port not open:{port2}')

    def serial_read(self, run_time=3):
        print(f'SerialRead start, run time = {run_time}')
        debug = False
        readings = ''
        serial_data = []
        self.running = True
        start_time = time.time()
        while ((time.time() - start_time) < run_time) and self.running:
            if self.ser.in_waiting > 0:
                try:
                    serial_data.append(self.ser.readline(self.ser.in_waiting).decode())
                except UnicodeDecodeError as e:
                    print(f"Decode error: {e}")
            time.sleep(0.001)
        if self.ser and self.execute_close:
            self.ser.close()
            print('SerialRead stop. Serial Close')
            if debug:
                print(f'serial_data = {readings}')
        #return readings
        return serial_data

    def dut_serial_read(self, run_time=10):
        print('dut_serial_read start')
        debug = True
        dbg_data1 = ''
        dbg_data2 = ''
        serial_data1 = []
        serial_data2 = []
        self.running = True
        start_time = time.time()
        while ((time.time() - start_time) < run_time) and self.running:
            try:
                if self.ser1.in_waiting > 0:
                    if debug:
                        dbg_data1 += self.ser1.readline(self.ser1.in_waiting).decode()
                        serial_data1.append(self.ser1.readline(self.ser1.in_waiting).decode())
                if self.ser2.in_waiting > 0:
                    if debug:
                        dbg_data2 += self.ser2.readline(self.ser2.in_waiting).decode()
                        serial_data2.append(self.ser2.readline(self.ser2.in_waiting).decode())
            except UnicodeDecodeError as e:
                print(f"Decode error: {e}")
            time.sleep(0.001)
        if self.execute_close:
            self.ser1.close()
            self.ser2.close()
            print('SerialRead stop. Serial Close')
            if debug:
                print(f'serial_data1 = {dbg_data1}')
                print(f'serial_data2 = {dbg_data2}')
        return serial_data1, serial_data2

    def settings(self, timeout, execute_close=True):
        print(f'Settings. timeout = {timeout}')
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

    def dut_execute(self, task_func=None, *task_args, **task_kwargs):
        """
        Run task_func synchronously while reading serial concurrently.
        Returns (task_result, serial_data, serial_error).
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Submit serial read and task concurrently
            serial_future = executor.submit(self.dut_serial_read, self.timeout)
            if task_func:
                task_future = executor.submit(task_func, *task_args, **task_kwargs)
                task_result = task_future.result()
            else:
                task_result = None

            serial_data = serial_future.result()

        print('dut_serial_read.execute complete')
        return task_result, serial_data

    def search_test_pattern_with_keyword(self, data_lines, test_pattern, keyword=[]):
        print('search_test_pattern_with_keyword')
        match_count = 0
        result = []
        for line_idx in range(len(data_lines)):
            words = data_lines[line_idx]
            if re.search(test_pattern, words, re.IGNORECASE):
                match_count += 1
                result.append(words)
                print(f'match result = {words}')
        return result

    def search_test_pattern(self, data_lines, test_pattern, count=1, fullmatch=True):
        print('search_test_pattern')
        match_count = 0
        result = []
        for line_idx in range(len(data_lines)):
            words = data_lines[line_idx]
            if fullmatch:
                if re.fullmatch(test_pattern, words, re.IGNORECASE):
                    match_count += 1
                    result.append(words)
                    print(f'match result = {words}')
            else:
                if re.match(test_pattern, words, re.IGNORECASE):
                    match_count += 1
                    result.append(words)
                    print(f'match result = {words}')

            if match_count == count:
                break
        return result

    def search_keyword_sets_ordered(self, data_lines, keywords):
        print('search_keyword_sets_ordered')
        result = []
        next_start_line = 0
        kw_idx = 0
        while kw_idx < len(keywords):
            for line_idx in range(next_start_line, len(data_lines)):
                words = data_lines[line_idx]
                if keywords[kw_idx] in words:
                    #if keywords[kw_idx] == 'Starting Observer Demo':
                    #    print('Debug start')
                    print(f'kw found: {keywords[kw_idx]} in line {line_idx}')
                    print(f'idx = {kw_idx}')
                    if (kw_idx + 1) < len(keywords):
                        kw_idx_temp = kw_idx
                        for next_kw_idx in range((kw_idx + 1), len(keywords)):
                            #print(f'check next kw index = {next_kw_idx}')
                            if keywords[next_kw_idx] in words:
                                kw_idx = next_kw_idx
                                print(f'next kw found: {keywords[next_kw_idx]} in line{line_idx}')
                        next_start_line = line_idx + 1
                        result.append(words)
                        if kw_idx_temp != kw_idx:
                            print('Multiple keyword in one line:True')
                            if (kw_idx + 1) < len(keywords):
                                kw_idx = kw_idx + 1
                        else:
                            print('Multiple keyword in one line:False')
                            kw_idx = kw_idx + 1
                            #if kw_idx == (len(keywords) - 1):
                            #    print('Find all keywords')
                            #    break
                        print(f'next_start_line = {next_start_line}, kw_idx = {kw_idx}')
                        break
                    else:
                        print('Find all keywords')
                        kw_idx = kw_idx + 1
                        break
            if next_start_line == 0:
                print('First keyword not found')
                break

        '''
        for idx in range(kw_idx, len(keywords)):
            for line_idx in range(next_start_line, len(data_lines)):
                words = data_lines[line_idx]
                if keywords[idx] in words:
                    print(f'kw found: {keywords[idx]} in line {line_idx}')
                    print(f'idx = {idx}')
                    if (kw_idx + 1) <= len(keywords):
                        kw_idx_temp = kw_idx
                        for next_kw_idx in range((kw_idx + 1), len(keywords)):
                            #print(f'check next kw index = {next_kw_idx}')
                            if keywords[next_kw_idx] in words:
                                kw_idx = next_kw_idx
                                print(f'next kw found: {keywords[next_kw_idx]} in line{line_idx}')
                        if kw_idx_temp != kw_idx:
                            print('Multiple keyword in one line')
                            if (kw_idx + 1 ) <= len(keywords):
                                kw_idx = kw_idx + 1
                    next_start_line = line_idx + 1
                    result.append(words)
                    print(f'next_start_line = {next_start_line}, kw_idx = {kw_idx}')
                    break
            if next_start_line == 0:
                print('First keyword not found')
                break
        '''
        '''
        for kw in keywords:
            for line_idx in range(next_start_line, len(data_lines)):
                #words = data_lines[line_idx].lower()
                words = data_lines[line_idx]
                #print(f'{line_idx}:Compare words:{words}')
                if kw in words:
                    print(f'Found: {kw} in line{line_idx}')
                    next_start_line = line_idx + 1
                    result.append(words)
                    break
            if next_start_line == 0:
                print('First keyword not found')
                break
        '''
        return result







