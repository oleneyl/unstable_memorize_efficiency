import random



"""
Datasets : 
{Skillname : {delay : Delay, prob : Probability}, ...}
"""

Mage_FB_Setting = {"Energy bolt" : {"delay" : 630, "prob" : 0.0044},
                    "Flame orb" : {"delay" : 720, "prob" : 0.0221},
                    "Poison breath" : {"delay" : 600, "prob" : 0.0221},
                    "Explosion" : {"delay" : 540, "prob" : 0.0442},
                    "poison mist" : {"delay" :1140, "prob" : 0.0442},
                    "Slime virus" : {"delay" :1260, "prob" : 0.0442},
                    "Paralyze" : {"delay" : 600, "prob" : 0.1106},
                    "mist eruption" : {"delay" : 780, "prob" : 0.1106},
                    "meteor" : {"delay" : 870, "prob" : 0.1106},
                    "flame heize" : {"delay" :1080, "prob" : 0.1106},
                    "infinity" : {"delay" : 600, "prob" : 0.1106},
                    "efrite" : {"delay" : 600, "prob" : 0.1106},
                    "megido flame" : {"delay" : 690, "prob" : 0.1106},
                    "epic adventure" : {"delay" : 0, "prob" : 0.0450}}

Mage_TC_Setting = {"Energy bolt" : {"delay" : 630, "prob" : 0.0054},
                    "Cold beam" : {"delay" : 810, "prob" : 0.0269},
                    "Thunder bolt" : {"delay" : 750, "prob" : 0.0269},
                    "Ice strike" : {"delay" : 960, "prob" : 0.0538},
                    "Glacial chain" : {"delay" :780, "prob" : 0.0538},
                    "Thunder storm" : {"delay" :1050, "prob" : 0.0538},
                    "Chain lightening" : {"delay" :600, "prob" : 0.1344},
                    "blizzard" : {"delay" : 870, "prob" : 0.1344},
                    "frozen orb" : {"delay" :1140, "prob" : 0.1344},
                    "flame heize" : {"delay" : 600, "prob" : 0.1344},
                    "infinity" : {"delay" : 600, "prob" : 0.1344},
                    "elquiness" : {"delay" : 600, "prob" : 0.1344},
                    "lightening spear" : {"delay" : 720, "prob" : 0.0538},
                    "epic adventure" : {"delay" :   0, "prob" : 0.0550}}

Bishop_Setting = {"Energy bolt" : {"delay" : 630, "prob" : 0.0041},
                    "Holy arrow" : {"delay" : 600, "prob" : 0.0407},
                    "heal" : {"delay" : 450, "prob" : 0.0407},
                    "Shining ray" : {"delay" : 690, "prob" : 0.0407},
                    "Holy fountain" : {"delay" :2760, "prob" : 0.0407},
                    "Dispel" : {"delay" : 900, "prob" : 0.1016},
                    "divine protection" : {"delay" :1290, "prob" : 0.0407},
                    "angel ray" : {"delay" : 630, "prob" : 0.1016},
                    "genesis" : {"delay" : 690, "prob" : 0.1016},
                    "big bang" : {"delay" : 570, "prob" : 0.1016},
                    "ressurection" : {"delay" :1710, "prob" : 0.1016},                    
                    "infinity" : {"delay" : 600, "prob" : 0.1016},
                    "bahamutte" : {"delay" : 600, "prob" : 0.1016},
                    "heavens door" : {"delay" : 270, "prob" : 0.0407},
                    "epic adventure" : {"delay" : 0, "prob" : 0.0417}}

UNS_COOLTIME = 8550
UNS_DELAY = 870
INFINITY_COOLTIME = 171000
INFINITY_REMAIN = 101000
MAGE_FB = 0
MAGE_TC = 1
BISHOP = 2

class Uns_mem():
    def __init__(self, _type, name = "Unstable"):
        self.name = name
        if _type == MAGE_FB:
            self.setting = Mage_FB_Setting
        elif _type == MAGE_TC:
            self.setting = Mage_TC_Setting
        elif _type == BISHOP:
            self.setting = Bishop_Setting
        else:
            raise TypeError
        
        self.left = 0
        self.init_skill()
        
    def init_skill(self):
        self.pick = {}
        prob = 0
        for skill in self.setting:
            self.pick[skill] = [prob , prob + self.setting[skill]["prob"]]
            prob += self.setting[skill]["prob"]
    
    def pass_time(self, time):
        self.left -= time
    
    def is_usable(self):
        if self.left <= 0:
            return True
        else:
            return False
    
    def use(self):
        tag = random.random()
        self.left = UNS_COOLTIME
        #print("Tag : %.2f" % (tag))
        for key in self.pick:
            #print("key:" + str(self.pick[key]))
            if tag >= self.pick[key][0] and tag <= self.pick[key][1]:
                is_inf = False
                if key == "infinity":
                    is_inf = True
                return self.setting[key]["delay"] * 0.5 + UNS_DELAY, is_inf
        
        print(tag)
        raise ValueError
                
    def print_status(self):
        print(self.name + "//"+ " left:" + str(self.left))                
                    
class Infinity():
    def __init__(self, name = "infinity"):
        self.name = name
        self.on = False
        self.left = 0
        self.cont = 0
        self.full_increment = self.calc_full_damage_factor()
        
    def calc_full_damage_factor(self):
        damage = 0
        for tick in range(0, INFINITY_REMAIN, 1000):
            damage += (1 + 0.65 + 0.03 * (tick //4000))
        return damage * 1000
        
    def get_increment(self):
        if self.on:
            return (1 + 0.65 + 0.03 * (self.cont // 4000))
        else:
            return 1.0
        
    def pass_time(self, time):
        self.left -= time
        self.cont += time
        if self.cont >= INFINITY_REMAIN:
            self.on = False
    
    def is_usable(self):
        if self.left <= 0:
            return True
        else:
            return False
    
    def use(self):
        if self.left > 0:
            raise TypeError
        self.on = True
        self.left = INFINITY_COOLTIME
        self.cont = 0

    def use_force(self):
        self.on = True
        self.left = INFINITY_COOLTIME
        self.cont = 0        

    def print_status(self):
        print(self.name + "//ON: "+str(self.on) +" left:" + str(self.left) + " cont:" + str(self.cont))

                
def simulate(_type, tot_time, term, logging = False):
    
    time = 0
    inf_real = Infinity()
    inf_virt = Infinity("infinity_virt")
    uns_mem = Uns_mem(_type)
    deal = 0
    garbage_time = 0
    
    def pass_time(t):
        inf_virt.pass_time(t)
        inf_real.pass_time(t)
        uns_mem.pass_time(t)

    def print_log():
        print("-------At time %d--------" % (time))
        inf_real.print_status()
        inf_virt.print_status()
        uns_mem.print_status()
        print("deal : %d, garbage_time : %d" % (deal, garbage_time))

    while time < tot_time:
        if logging : print_log()
        if inf_virt.on or inf_real.on:
            deal += inf_real.full_increment
            pass_time(INFINITY_REMAIN)
            time += INFINITY_REMAIN
            continue
        else:
            #No infinity is turned on, first check whether real infinity is usable
            if inf_real.is_usable():
                if logging : print("\n******infinity used******\n")
                inf_real.use()
            else:
                #If real infinity is not usable, use unstable memoruze if available
                inf_flag = False
                if uns_mem.is_usable():
                    delay, is_inf = uns_mem.use()
                    if logging : print("\nUns mem used, delay %d, is_inf : %r\n" % (delay, is_inf))
                    garbage_time += delay
                    if is_inf:
                        if logging : print("\n******unstable infinity used******\n")
                        inf_virt.use_force()
                        inf_flag = True
                if not inf_flag:
                    pass_time(term)
                    time += term
                    deal += max(inf_real.get_increment(), inf_virt.get_increment()) * term

    #print("Total time %d, deal : %d, garbage_time : %d" % (tot_time, deal, garbage_time))
    dps = (deal * (tot_time - garbage_time) / (tot_time) / (tot_time))
    #print("DPS : %.4f" % dps)
    return dps

def simulate_nouns(_type, tot_time, term, logging = False):
    time = 0
    inf_real = Infinity()
    deal = 0
    garbage_time = 0
    
    def pass_time(time):
        inf_real.pass_time(time)

    def print_log():
        print("-------At time %d--------" % (time))
        inf_real.print_status()
        print("deal : %d, garbage_time : %d" % (deal, garbage_time))

    for time in range(0, tot_time, term):
        if logging : print_log()
        if inf_real.on:
            deal += inf_real.get_increment() * term
            pass_time(term)
            continue
        else:
            if inf_real.is_usable():
                if logging : print("\n******infinity used******\n")
                inf_real.use()
            else:
                pass_time(term)
                deal += term

    #print("Total time %d, deal : %d, garbage_time : %d" % (tot_time, deal, garbage_time))
    dps = (deal * (tot_time - garbage_time) / (tot_time) / (tot_time))
    #print("DPS : %.4f" % dps)
    return dps
    
if __name__ == "__main__":
    for _type in range(3):
        dps_1 = 0
        dps_2 = 0
        for i in range(10):
            dps_1 += simulate(_type, 1000 * 720000, 50)
            dps_2 += simulate_nouns(_type, 1000 * 3600, 50)    
        if _type == 0:
            name = "MAGE_FB"
        elif _type == 1:
            name = "MAGE_TC"
        else:
            name = "BISHOP"
        print("%s :: Increment rate = %.4f" % (name, dps_1 / dps_2))

