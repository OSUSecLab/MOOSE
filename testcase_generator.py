import os
import signal

import angr

import compiler
regex='\s*(static)*(signed)*(unsigned)*\s*int [a-zA-Z_]+[0-9]*(\[[0-9]*\])*(\s*=\s*(-)*[0-9a-zA-Z]+)*;|\s*(static)*(signed)*(unsigned)*\s*short [a-zA-Z_]+[0-9]*(\[[0-9]*\])*(\s*=\s*(-)*[0-9a-zA-Z]+)*;|\s*(static)*(signed)*(unsigned)*\s*char [a-zA-Z_]+[0-9]*(\[[0-9]*\])*(\s*=\s*(-)*[0-9a-zA-Z]+)*;|\s*(static)*(signed)*(unsigned)*\s*long [a-zA-Z_]+[0-9]*(\[[0-9]*\])*(\s*=\s*(-)*[0-9a-zA-Z]+)*;'
regex2="\s*[a-zA-Z_]+[0-9]*(\[[0-9]*\])*(\s*=\s*(-)*[0-9a-zA-Z]+);"
fpath="./input/"
output="./output/"
counter=0
import re



class variable:
    assigned=False
    variablename=""
    variablevalue =""
    variablelocation=0
    isstatic=False
    basename=""
    variabletype=""
    type=0
    arraytype=False
    starts=0
    ends=0
    assignednumber=0


    def __init__(self, variabletype,variablename,variablelocation,variablevalue,isarray,isstatic):
        self.variabletype=variabletype
        self.variablename=variablename
        self.variablelocation=variablelocation
        self.variablevalue=variablevalue
        self.arraytype=isarray
        self.isstatic=isstatic



    def tostring(self):
         return ("variabletype={},variablename={},variableloaction={},variablevalue={},type={},assigned={},".format(self.variabletype,self.variablename,self.variablelocation,self.variablevalue,self.type,self.assignednumber))


def getvariable(line,linenumber):
    m = re.match(regex, line)
    readystr=m.group().strip()
    isstatic=False
    if "static" in readystr:
        readystr=readystr.replace("static ","")
        isstatic=True
    if "signed" in readystr:
        readystr=readystr.replace("signed ","")
        isstatic=True
    if "unsigned" in readystr:
        readystr=readystr.replace("unsigned ","")
        isstatic=True

    readystr.strip()

    vt=readystr.split(" ")[0]

    isarray=False

    value= ""

    vn=((readystr.split(";")[0]).split(" ")[1]);
    if "=" in vn:
        vnlist=((vn.split("=")))
        value=vnlist[1]
        vn=vnlist[0]
    else:
        value="0"

    if "[" in vn:
        vn=((vn.split("[")[0]))
        isarray=True
    return variable(vt,vn,linenumber,value,isarray,isstatic)
    


def hasvariable(line):
    m = re.match(regex, line)
    if not m == None:
        return True
    else:
        return False


def updatingvariables(variables, function_entrance_number,function_exit_number, main_linenumber):
    updatedvariables=[]
    mainexit=0
    for fx in function_exit_number:
        if fx> main_linenumber:
            mainexit=fx
            break



    for v in variables:
        index = 0
        v.type=1

        while (index < len(function_exit_number)):

            if v.variablelocation>= function_entrance_number[index] and v.variablelocation<= function_exit_number[index]:
                #print(v.variablename,v.variablelocation,function_entrance_number[index],v.variablelocation<= function_exit_number[index])

                v.type=2
                v.starts=function_entrance_number[index]
                v.ends=function_exit_number[index]
            index = index + 1
        if v.variablelocation >=main_linenumber and v.variablelocation<=mainexit:
            v.type=3 # v in main
        updatedvariables.append(v)
    return updatedvariables




def has_assign_variable(line):

    m = re.match(regex2, line)
    if not m == None:

        return True
    else:
        return False


def getname(line):
    m = re.match(regex2, line)
    str=m.group().strip()

    name=str.split("=")[0]
    name=name.strip()
    if "[" in name:
        name=name.split("[")[0].strip()


    return name


def updating_and_assgin(code,variables,function_entrance_number,function_exit_number):
    updatedvariables = []

    linenumber=0
    for v in variables:

        for line in code:
            linenumber = linenumber + 1
            if has_assign_variable(line):
                vname=getname(line)
                print(v.variablename,"=",vname,vname == v.variablename,len(vname),len(v.variablename))
                if v.variablename==vname:
                    v.assigned=True
                    print(linenumber)

                    if linenumber > v.variablelocation:

                            v.assignednumber=linenumber
                            print(v.tostring())
        updatedvariables.append(v)
    return updatedvariables





class sourcefile:
    mainline=0
    code=[]
    outputcode=[]
    path=""
    outputpath=""
    main_linenumber=0
    line_number=0
    entrance_number=0
    function_entrance_number=[]
    function_exit_number=[]
    variables=[]
    comment_starts = 0
    comment_ends = 0

    def make_it_symbolic(self,variable):

        self.outputcode.clear()
        for line in self.code:
            self.outputcode.append(line)
        if not variable.assigned:
            if variable.type == 1:
                if variable.arraytype:
                    insertcode = "read(0," + variable.variablename +",sizeof("+variable.variablename+"));\n"
                    self.outputcode.insert(self.entrance_number, insertcode)
                else:
                    insertcode = ""
                    if variable.variabletype == "int" or variable.variabletype == "long":
                        insertcode = "read(0," + variable.variablename +",sizeof("+variable.variablename+"));\n"
                    if variable.variabletype == "char":
                        insertcode = "read(0," + variable.variablename +",sizeof("+variable.variablename+"));\n"
                    self.outputcode.insert(self.entrance_number, insertcode)

            if variable.type == 3 or variable.type == 2:
                if variable.arraytype:
                    insertcode = "read(0," + variable.variablename +",sizeof("+variable.variablename+"));\n"
                    self.outputcode.insert(variable.variablelocation, insertcode)

                else:
                    insertcode = ""
                    if variable.variabletype == "int" or variable.variabletype == "long":
                        insertcode = "read(0," + variable.variablename +",sizeof("+variable.variablename+"));\n"
                    if variable.variabletype == "char":
                        insertcode = "read(0," + variable.variablename +",sizeof("+variable.variablename+"));\n"
                    self.outputcode.insert(variable.variablelocation, insertcode)
        else:

            if variable.type == 1:
                if variable.arraytype:
                    insertcode = "read(0," + variable.variablename +",sizeof("+variable.variablename+"));\n"


                    self.outputcode.insert(variable.assignednumber, insertcode)
                else:

                    insertcode = ""
                    if variable.variabletype == "int" or variable.variabletype == "long":
                        insertcode = "read(0," + variable.variablename +",sizeof("+variable.variablename+"));\n"
                    if variable.variabletype == "char":
                        insertcode = "read(0," + variable.variablename +",sizeof("+variable.variablename+"));\n"
                    self.outputcode.insert(variable.assignednumber, insertcode)

            if variable.type == 3 or variable.type == 2:

                if variable.arraytype:
                    insertcode = "read(0," + variable.variablename + ",sizeof("+variable.variablename+"));\n"
                    self.outputcode.insert(variable.assignednumber, insertcode)

                else:
                    insertcode = ""
                    if variable.variabletype == "int" or variable.variabletype == "long":
                        insertcode = "read(0," + variable.variablename +",sizeof("+variable.variablename+"));\n"
                    if variable.variabletype == "char":
                        insertcode = "read(0," + variable.variablename +",sizeof("+variable.variablename+"));\n"
                    self.outputcode.insert(variable.assignednumber, insertcode)



    def __init__(self,path):
        self.path=path
        self.outputpath=path.replace(".c","-sym.c")
        self.code=[]
        self.outputcode=[]
        self.mainline = 0

        self.main_linenumber = 0
        self.line_number = 0
        self.entrance_number = 0
        self.function_entrance_number = []
        self.function_exit_number = []
        self.variables = []
        self.assign_variables = []
        f=open(self.path,"r")
        self.comment_starts=0
        self.comment_ends=10000

        for line in f:


            self.line_number=self.line_number+1


            if("main" in line):
                self.main_linenumber=self.line_number
            if("{" in line):
                self.function_entrance_number.append(self.line_number)
            if("}" in line):
                self.function_exit_number.append(self.line_number)
            if(hasvariable(line)):

                self.variables.append(getvariable(line,self.line_number))



            self.code.append(line)
        f.close()
        for ln in self.function_entrance_number:
            if ln>=self.main_linenumber:
                self.entrance_number=ln
                break;

        self.variables=updatingvariables(self.variables,self.function_entrance_number,self.function_exit_number,self.main_linenumber)
        self.variables = updating_and_assgin(self.code,self.variables,self.function_entrance_number,self.function_exit_number)
        for v in self.variables:
            (v.tostring())





    def output(self,path):
        symflie = open(path, "w")
        for line in self.outputcode:

            symflie.write(line)

        symflie.close()
        self.outputcode.clear()



def handler(signum, stack):
    print("Time out")
    raise Exception

def hasSym(path):
    proj = angr.Project(path, auto_load_libs=False, use_sim_procedures=True,
                        default_analysis_mode='symbolic')

    init_state = proj.factory.entry_state()
    cfg = proj.analyses.CFGFast(normalize=True)

    sm = proj.factory.simgr(init_state)
    while len(sm.active) > 0:
        sm.step()
        states = sm.active
        for state in states:
            if len(state.solver.constraints) > 0:
                return True
    return False

def has_symbolic(path):
    compiler.default_comple(path)

    proj = angr.Project(path, auto_load_libs=False, use_sim_procedures=True,
                        default_analysis_mode='symbolic')

    state = proj.factory.entry_state()

    sm = proj.factory.simgr(state)
    cfg = proj.analyses.CFGFast(normalize=True)
    # sm.use_technique(angr.exploration_techniques.LoopSeer(cfg=cfg, bound=10))
    # sm.use_technique(angr.exploration_techniques.DFS())
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(5)
    try:
        sm.run()
    except:
        pass
    signal.alarm(0)

    if len(sm.active) == 0:

        if not len(sm.deadended) == 0:
            for state in sm.deadended:
                if len(state.solver.constraints) != 0:
                    return True
                else:
                    return False


    else:

        for state in sm.active:
            if len(state.solver.constraints) != 0:
                return True
            else:
                return False


 

    return False
def findvalues(path):
    f = open(path, "r")
    for line in f:

        m = re.match(regex2, line)
        if not m==None:
            print(line, end="")

  
def convertcfile(path):
    # ";"
    codes = []
    f = open(path, "r")
    for line in f:
        if "for(" in line:
            continue
        readystr = line.split(";")
        index=0

        for code in readystr:
            index = index + 1
            if index < len(readystr):
                codes.append(code + ";\n")
            else:
                codes.append(code)

    f.close()
    f = open(path, "w")

    for code in codes:
        f.write(code)
    f.close()


    #deal with { and }
    codes=[]
    f = open(path, "r")

    for line in f:
        readystr=line.split("{")
        index=0
        for code in readystr:
            index=index+1
            codes.append(code)
            if index< len(readystr):
                codes.append("{")
    f.close()
    f = open(path, "w")

    for code in codes:
        if "{" in code:
            f.write(code+"\n")
        else:
            f.write(code)
    f.close()
    #"}"
    codes = []
    f = open(path, "r")
    for line in f:
        readystr = line.split("}")
        index = 0
        for code in readystr:
            index = index + 1
            codes.append(code)
            if index < len(readystr):
                codes.append("}")
    f.close()
    f = open(path, "w")

    for code in codes:
        if "}" in code:
            f.write(code + "\n")
        else:
            f.write(code)
    f.close()


  

def testcasegeneration():
    index=0
    for r, d, f in os.walk(fpath):
        for file in f:

            if "sym" in file:
                continue


            if file.endswith(".c"):
                index = index + 1
                print("Scanning file#",index,":-----",file)


                try:
 

                    convertcfile(os.path.join(r, file))
                    source = sourcefile(os.path.join(r, file))
                    for v in source.variables:
                        print(v.tostring())
                        source.make_it_symbolic(v)

                        newpath = source.outputpath
                        newpath = newpath.replace(".c", "-" + v.variablename + ".c")

                        source.output(newpath)
                        compiler.default_comple(newpath)

                        if os.path.exists(newpath.replace("c", "bin")):

                            try:
   
                                print(newpath, output)
                                print("mv " + newpath + " " + output)
                                os.system("mv " + newpath + " " + output)
   

                            except:
                                print("mv " + newpath + " " + output)
                                os.system("mv " + newpath + " " + output)
                                pass

 


                except:
                    continue

  
                 
                    os.system("rm "+fpath+"*sym*.c")
                    os.system("rm "+fpath+file+".c")

testcasegeneration()
 

