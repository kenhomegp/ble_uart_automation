"""
Dependencies: pyserial
 install cmd:  pip install pyserial
"""

import sys
import time
import serial

SERIAL_TIMEOUT_RESP = "TIMEOUT: NO RESPONSE "

class SerialAccess():
    """
    Concrete implementation of DutAccessAbstractBaseClass which provides a generic serial access interface
    """
    
    def __init__(self, com_port, baud_rate):
        """

        :param serial_config: Serial dictionary as returned by SerialKeyDefines.create_serial_access_dict
        :return: if the serial_config can't be verified, a KeyError will be thrown.
        caller MUST catch the exceptions!
        """
        
        self.__port_number = com_port
        self.__com_port = None
        
        self.term_char = None
        self.device_type = None
        self.cmd_prompt = None
        self.char_send_delay = None
        
        self.__com_port = serial.Serial(port=self.__port_number,
                                        baudrate=baud_rate,
                                        parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        timeout=0)
        time.sleep(1)  # Todo move this to RasPi implementation
    
    def cleanup_for_exit(self):
        """
        additional cleanup required - other than closing ports' Some communications may need to close files
        :return:
        """
        if self.__com_port is not None:
            self.close_port()
    
   
    def close_port(self):
        """
        do not use soon to be replaced
        :return:
        """
        # acquire semaphore to allow thread safe access to the serail port resource
        try:
            if self.__com_port is not None:
                print(("Connection closed for device: {} on serial port: {}".format(self.device_type,
                                                                                    self.__port_number)))
                self.__com_port.close()
                self.__com_port = None
        except Exception as e:
            print("Error close_port: {}, reported exception: {}".format(self.__port_number, str(e)))
    
    def open_port(self):
        """
        open the  serial port
        :return: n/a
        """
        try:
            if not self.__com_port.isOpen():
                self.__com_port.open()
                print(
                    "Connection opened for device: {} on serial port: {}".format(self.device_type, self.__port_number))
        except Exception as e:
            print("Error open_port: {}, exception: {}".format(self.__port_number, str(e)))
    
    def verify_connection(self):
        print("TBD")
    
    def __del__(self):
        """

        :return:
        """
        self.cleanup_for_exit()
    
    def send_cmd_wait_for_resp(self, command, timeout_s=3, wait_resp=None, remove_cmd_echo=False):
        """

        :param command:
        :param timeout_s: timeout in seconds to terminate waiting for a response
        :param wait_resp: response expected in string
        :param remove_cmd_echo: many products will echo the command in the response, in some cases, this could
        be a problem
        :return:
        """
        
        if wait_resp is None:
            wait_resp = self.cmd_prompt
        
        self.send_cmd(command)
        resp_str = self.wait_for_resp(wait_resp, timeout_s)
        
        if remove_cmd_echo:
            resp_str = self.remove_cmd_echo_from_resp_str(command, resp_str)
        
        return resp_str
    
    def remove_cmd_echo_from_resp_str(self, command, resp_str):
        """
        This method removes the command string from the response if it is found in the first line
        of the response. This is needed since mfg mode returns an echo of the command string and that can cause issues
        when parsing an expected response.
        :param command: The command str that was sent to the console
        :param resp_str: response string from a serial command
        :return:
        """
        cmd_removed = False
        if resp_str:
            # remove leading whitespace
            resp = resp_str.lstrip()
            
            if self.term_char in resp:
                # split the string to separate the first line
                echo_str, resp = resp.split(self.term_char, 1)
                
                # remove trailing whitespace from the echo string
                echo_str = echo_str.rstrip()
                
                # if this is the command echo then the command string will equal the echo string.
                # if this is not the command echo string then return the original string
                if command == echo_str:
                    cmd_removed = True
        
        # return the original response string if no cmd string is found to remove.
        if not cmd_removed:
            resp = resp_str
        
        return resp
    
    def wait_for_resp(self, exp_resp=None, timeout_s=3, print_each_char_to_console=False, write_each_char_to_file=True):
        """
        method only reads from serial for until timeout_s or exp_resp is found

        print_each_char_to_console is very useful debug tool for commands such as software 'up all'
          which can take upwards of 3-5 min to return the prompt.  This allows the output to be printed
          to the screen while waiting for the exp_resp

        :param exp_resp: expected response to read until it is found
        :param timeout_s: seconds to continue search
        :param print_each_char_to_console: prints each character to the console as it is read.
        :param write_each_char_to_file: controls if the serial response should be written to the log file.
        :return: returns the string found in serial or error message Todo - generic may be able to  return a boolean+string

        """
        
        timeout = time.time() + timeout_s  # timeout in seconds from now
        
        if exp_resp is None:
            exp_resp = self.cmd_prompt
        
        output_chars = []
        response_string = ""
        
        while True:
            if time.time() < timeout:
                read = self.read_line(timeout_seconds=.5, return_repr_str=False)
                if print_each_char_to_console and write_each_char_to_file:
                    sys.stdout.write(read)
                output_chars += read
                response_string = ''.join(output_chars)
                if exp_resp in response_string:
                    if not print_each_char_to_console and write_each_char_to_file:
                        print("serial response: ({}) ".format(response_string))
                    break
            else:
                timeout_str = ("{} - Did not find response: {} in Serial response: {}"
                               .format(SERIAL_TIMEOUT_RESP, exp_resp, response_string))
                response_string = timeout_str
                print(timeout_str)
                break
        
        return response_string
    
    def send_cmd(self, command):
        """
        Write to the serial bus.
        :param command: what you would like to send -> term_char added.
        :return: None
        """
        cmd = command + self.term_char
        print("On device: {} Command is: {}".format(self.device_type, cmd))
        
        try:
            # clear any excess garbage off the input/output buffer for a clean start
            self.__com_port.flushOutput()
            self.__com_port.flushInput()
            if self.char_send_delay == 0:
                self.__com_port.write(cmd.encode())  # Send command!
            else:
                self.char_send_delay *= .001  # convert to sec
                for ch in cmd:
                    self.__com_port.write(ch.encode())  # Send command!
                    time.sleep(self.char_send_delay)
        except Exception as e:
            print("Error write_with_char_delay port: {}, exception: {}".format(self.__port_number, str(e)))
    
    def com_write(self, bytes):
        """
        write bytes
        :param bytes:
        :return: length of the data it writes.
        """
        return self.__com_port.write(bytes)
    
    def com_read(self, size=1):
        """
        Read size bytes from the serial port.
        :param size: byte size
        :return: bytes read
        """
        return self.__com_port.read()
    
    def com_in_waiting(self):
        """

        :return:
        """
        return self.__com_port.inWaiting()
    
    def read_line(self, line_terminator="\n", timeout_seconds=1, return_repr_str=False):
        """
        Read a single line from the serial connection. There are two types of date that ca be returned from
        this method.
        :param line_terminator: end of line terminator or terminators
        :param timeout_seconds: seconds to continue search
        :param return_repr_str: set to True to use repr() to format the response string

        :return: a single line
        """
        output_chars = []
        
        timeout = time.time() + timeout_seconds
        
        resp_str = ""
        while True:
            # Avoid breaking in the middle of reading a line due to a timeout.
            # If data is available wait for line_terminator or cmd_prompt to break,
            # else break on timeout if no data is available.
            if self.__com_port.inWaiting():
                read = (self.__com_port.read().decode(encoding='utf-8', errors="replace")).replace('\0',
                                                                                                   '')  # some response  contain nulls which chop the string
                output_chars += read
                resp_str = ''.join(output_chars)
                if line_terminator in resp_str:
                    break
            elif time.time() > timeout:
                break
        
        if return_repr_str:
            resp_str = repr(resp_str)
        
        return resp_str
    
    def read_all(self):
        """
        Read all bytes currently available from the serial connection.
        :return: String
        """
        
        response_string = ""
        try:
            response_string = self.__com_port.read_all()
            print("Response: {}".format(response_string))
        
        except Exception as e:
            print("Error read_all port: {}, exception: {}".format(self.__port_number, str(e)))
        
        return response_string



