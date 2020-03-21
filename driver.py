import serial.tools.list_ports;

ID="1A86:7523"
ser = serial.Serial()

Ops = {  # protol(протокол для общения с датчиком)
    'N': 'N',  # current coordinate
    'W': 'W',  # start Measurement
    'M': 'M',  # start Measurement
    'C': 'C',  # claer all safe data
    'S': 'S',  # overwrite sensitivity threshold
    'E': 'E',  # stop driver
    'T': 'T'  # get status driver
}


def ports():
    for port in serial.tools.list_ports.comports():
        if ID in port.hwid:
            return port.device
def init():
    ser.baudrate = 9600
    ser.port = ports()
    ser.open()
    if ser.is_open:
        return True
    else:
        return False




def doChangeSensor(arg1, arg2):  # overwrite sensitivity threshold(перезаписывает порог чувствительности)
    try:
        ser.write(bytes('S', 'UTF-8'))
        ser.flush()
        ser.write(bytes(arg1 + '\n', 'UTF-8'))
        ser.flush()
        ser.write(bytes(arg2 + '\n', 'UTF-8'))
        ser.flush()
    except:
        raise Exception('error')


def doClear():  # claer all safe data(очищает все измерения сделанные датчиким)
    try:
        ser.write(bytes('C', 'UTF-8'))
        ser.flush()
    except:
        raise Exception('error')


def doMeasurement():  # start Measurement(Запустить режим ожидания старта маятника и записи маха)
    try:
        ser.write(bytes('W', 'UTF-8'))
        ser.flush()
    except:
        raise Exception('error')


def getStatus():  # get status driver(получает текущий режим работы драйвера)
    try:
        ser.write(bytes('T', 'UTF-8'))
        ser.flush()
        statusWork = ser.readline().decode()
        statusLastWork = ser.readline().decode()
        return statusWork, statusLastWork
    except:
        raise Exception('error')


def getDataCoordinate():  # current position(возвращает текущее положение маятника)
    try:
        ser.write(bytes('N', 'UTF-8'))
        ser.flush()
        l = (ser.readline().decode())
        return l
    except:
        raise Exception('error')


def getDataArray():  # get received data-time and coordinate(возвращает собранные данные в виде 2х массивов-время и коррдинату)
    try:
        ser.write(bytes('M', 'UTF-8'))
        ser.flush()
        k = int(ser.readline().decode())
        m=k
        time = []
        coordinate = []
        while k > 0:
            time.append(float(ser.readline().decode()))
            coordinate.append(int(ser.readline().decode()))
            k = k - 1
        return coordinate, time,m
    except:
        raise Exception('error')


def checkSyntax(arg):
    if not (arg in Ops):
        raise Exception('not found operation')


def stop():  # stop driver(останавливает драйвер)
    try:
        ser.write(bytes('E', 'UTF-8'))
        ser.flush()
    except:
        raise Exception('error')
