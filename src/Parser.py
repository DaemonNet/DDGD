class Expr:
    def __init__(self):
        self.predicates=[]
        self.implicant = None

    def __str__(self):
        return(str(self.predicates) +  str(self.implicant))

def parseISCAS(file):
    f = open(file, mode="r", encoding="utf8", errors='ignore')
    alllines = f.readlines()
    outstr = []
    for line in alllines:
        #print(line)
        line = line.replace("\x00", "")
        
        line = line.replace("!","")
        line = line.replace("(","")
        line = line.replace(")","")
        line = line.replace("&&","AND")

        line = line.replace("||","AND")
        line = line.replace("\n","")
        index = line.find(":")
        if line == "":
            continue
        line = line[index+1:] #remove first part
        index = line.find("==")
        pre = line[:index].strip()
        post = line[index+3:]
        line = post + " IMPLIES " + pre
        outstr.append(line + "\n")
    f.close()

    return outstr

def readSDfromFile(path):
    f = open(path, mode="r", encoding="utf8", errors='ignore')
    return f.readlines()


def parseSD(in_str):
    SD = []

    for line in in_str:
        exp = Expr()
        line_split = line.split(" ")
        for elem in line_split:
            elem = elem.strip()
            if elem == "AND":
                continue
            if elem == "IMPLIES":
                break
            elem = replacer(elem)
            exp.predicates.append(elem)
        exp.implicant = line_split[-1].strip()
        exp.implicant = replacer(exp.implicant)
        SD.append(exp)

    return SD
        
            
        
def replacer(line):
    line = line.replace(".","_")
    line = line.replace("der(","")
    line = line.replace(")","")
    line = line.replace("[","")
    line = line.replace("]","")
    line = line.replace("$","")
    line = line.replace("+","")
    return line