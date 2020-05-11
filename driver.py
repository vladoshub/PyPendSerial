import serial.tools.list_ports;
import measurement
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
    ser.baudrate = 500000
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
        arg=str(arg1)+'$'+str(arg2)+'$'
        ser.write(bytes(arg + '\n', 'UTF-8'))
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

        ser.write(bytes('W', 'UTF-8'))
        ser.flush()
        status = ser.readline().strip().decode()
        return status



def getStatus():  # get status driver(получает текущий режим работы драйвера)
    try:
        ser.write(bytes('T', 'UTF-8'))
        ser.flush()
        statusWork = ser.readline().strip().decode()
        statusLastWork = ser.readline().strip().decode()
        return statusWork, statusLastWork
    except:
        raise Exception('error')


def getDataCoordinate():  # current position(возвращает текущее положение маятника)
    try:
        ser.write(bytes('N', 'UTF-8'))
        ser.flush()
        l = (ser.readline().strip().decode())
        return l
    except:
        raise Exception('error')


def getDataArray():  # get received data-time and coordinate(возвращает собранные данные в виде 2х массивов-время и коррдинату)
    try:
        ser.write(bytes('M', 'UTF-8'))
        ser.flush()
        status = ser.readline().strip().decode()
        meas = measurement.measurement()
        meas.set_Status(status)
        k = int(ser.readline().strip().decode())
        meas.set_Count(k)
        if(status=='I' and k>0):
            meas.set_Count(k)
            time = []
            coordinate = []
            while k > 0:
                time.append(float(ser.readline().strip().decode()))
                coordinate.append(int(ser.readline().strip().decode()))
                k = k - 1
            meas.set_Time(time)
            meas.set_Coordinate(coordinate)
            return meas
        else:
            return meas
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
