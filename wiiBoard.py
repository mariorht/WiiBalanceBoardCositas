from select import poll, POLLIN
from inspect import getmembers
from pprint import pprint
import xwiimote


class wiiBoard:
    def __init__(self):
        self.dev = None
        self.p = None
    
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

                return NO, NE, SO, SE
                # print(NO,NE)
                # print(SO,SE)            

            else:
                # print("Evento que no es EVENT_BALANCE_BOARD")
                if evt.type != xwiimote.EVENT_ACCEL:
                    print ("type:", evt.type)
        except IOError as e:
            if e.errno != errno.EAGAIN:
                print ("Bad")
