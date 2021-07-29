from select import poll, POLLIN
from inspect import getmembers
from pprint import pprint
import numpy as np
import xwiimote

NO_base, NE_base, SO_base, SE_base = 0,0,0,0
SENSOR_FACTOR_SEGURIDAD = 100
MEDIAN_FILTER_LENGTH = 10


class wiiBoard:
    def __init__(self):
        self.dev = None
        self.p = None

        self.NO_buffer = np.zeros(MEDIAN_FILTER_LENGTH)
        self.NE_buffer = np.zeros(MEDIAN_FILTER_LENGTH)
        self.SO_buffer = np.zeros(MEDIAN_FILTER_LENGTH)
        self.SE_buffer = np.zeros(MEDIAN_FILTER_LENGTH)


    def connect(self):
        # display a constant
        print ("=== " + xwiimote.NAME_CORE + " ===")

        # list wiimotes and remember the first one
        try:
            mon = xwiimote.monitor(True, True)
            print ("monitor file descriptor", mon.get_fd(False))
            ent = mon.poll()
            firstwiimote = ent
            while ent is not None:
                print ("Found device: " + ent)
                ent = mon.poll()
        except SystemError as e:
            print ("ooops, cannot create monitor (", e, ")")

        print ("===========================")


        # continue only if there is a wiimote
        if firstwiimote is None:
            print ("No wiimote to read")
            exit(0)

        # create a new iface
        try:
            self.dev = xwiimote.iface(firstwiimote)
        except IOError as e:
            print ("ooops,", e)
            exit(1)

        self.p = poll()
        self.p.register(self.dev.get_fd(), POLLIN)


    def print_info(self):
        # display some information and open the iface
        try:
            print ("syspath:" + self.dev.get_syspath())
            fd = self.dev.get_fd()
            print ("fd:", fd)
            print ("opened mask:", self.dev.opened())
            self.dev.open(self.dev.available() | xwiimote.IFACE_WRITABLE)
            print ("opened mask:", self.dev.opened())
            print ("capacity:",  self.dev.get_battery(), "%")
            print ("devtype:",   self.dev.get_devtype())
            print ("extension:", self.dev.get_extension())
        except SystemError as e:
            print ("ooops", e)
            exit(1)




    def read_events(self):
        # read some values
        evt = xwiimote.event()
        n = 0
        # while 1:
        self.p.poll(10)
        try:
            self.dev.dispatch(evt)
            if evt.type == xwiimote.EVENT_BALANCE_BOARD:
                # print("EVENT_BALANCE_BOARD", n)
                SE = evt.get_abs(1)[0]
                NE = evt.get_abs(0)[0]
                NO = evt.get_abs(2)[0]
                SO = evt.get_abs(3)[0]

                if NO < NO_base + SENSOR_FACTOR_SEGURIDAD:
                    NO = 0
                if NE < NE_base + SENSOR_FACTOR_SEGURIDAD:
                    NE = 0
                if SO < SO_base + SENSOR_FACTOR_SEGURIDAD:
                    NO = 0
                if SE < SE_base + SENSOR_FACTOR_SEGURIDAD:
                    SE = 0

                
                self.NO_buffer = np.roll(self.NO_buffer, -1)
                self.NO_buffer[-1] = NO

                self.NE_buffer = np.roll(self.NE_buffer, -1)
                self.NE_buffer[-1] = NE

                self.SO_buffer = np.roll(self.SO_buffer, -1)
                self.SO_buffer[-1] = SO

                self.SE_buffer = np.roll(self.SE_buffer, -1)
                self.SE_buffer[-1] = SE

                return np.median(self.NO_buffer), np.median(self.NE_buffer), np.median(self.SO_buffer), np.median(self.SE_buffer)
           

            else:
                # print("Evento que no es EVENT_BALANCE_BOARD")
                if evt.type != xwiimote.EVENT_ACCEL:
                    print ("type:", evt.type)
        except IOError as e:
            if e.errno != errno.EAGAIN:
                print ("Bad")

    def getBatteryLevel(self):
        return self.dev.get_battery()


    def getSensorStatus(self):
        NO, NE, SO, SE = self.read_events()
        
        # NO = NO - NO_base
        # NE = NE - NE_base
        # SO = SO - SO_base
        # SE = SE - SE_base

        total = (NE + SE + NO + SO)
        x = NE + SE - NO - SO
        y = NO + NE - SO - SE

        if(total != 0):
            return x/total, y/total
        else:
            return 0, 0


    def calibrar(self):
        try:
            NO_base, NE_base, SO_base, SE_base = self.read_events()
            print("Calibrado", NO_base, NE_base, SO_base, SE_base)
        except:
            print("Error de calibración")