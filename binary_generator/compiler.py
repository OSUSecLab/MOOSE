import os
import ntpath
import subprocess

leftflag="./resourcefiles/validflags"
flagfile="./resourcefiles/validflags"
testflag="./resourcefiles/validflags"
finalflags= "./resourcefiles/validflags"
validflags=  "./resourcefiles/validflags"

YES_CASE="YES"
NO_CASE="NO"

def test_complie(filepath):
    f = open(testflag, "r")
    fpath, fname = ntpath.split(filepath)
    for line in f:
        testcmd = line.rstrip()
        finalcmd = "gcc " + testcmd + " " + filepath + " -o " + fpath + "/out" + line.strip().replace(" ","") + "-" + fname.replace(
            ".c", ".bin")
        print(finalcmd)

        os.system(finalcmd)


def load_flag_and_complie(filepath):
    f = open(flagfile, "r")
    fpath, fname = ntpath.split(filepath)
    for line in f:
        testcmd = line.strip()
        finalcmd = "gcc " + testcmd + " " + filepath + " -o " + fpath + "/out" + line.strip() + "-" + fname.replace(
            ".c", ".bin")

        os.system(finalcmd)

def clear(path):
    for r, d, f in os.walk(path):
        for file in f:
            if not (file.endswith("c") or file.endswith("res")):
                os.remove(os.path.join(r, file))

def default_comple(filepath):
    cmd = "gcc  -nostartfiles " + filepath + " -o " + filepath.replace(
        ".c", ".bin")
    os.system(cmd)


def complie(filepath,currentcase,level,flag):
    fpath, fname = ntpath.split(filepath)

    turnoncase= flag
    turnoffcase= flag[:2] + 'no-' + flag[2:]
    allflags=loadallvalidflags()
    cmds=""


    for f in allflags:
        if not (f == flag):

                if currentcase == YES_CASE:
                    cmds = cmds + f + " "
                else:
                    cmds = cmds + f[:2] + 'no-' + f[2:] + " "


    turnonfinalcmd = "gcc " + level+" " +cmds + turnoncase + " " + filepath + " -o " + fpath + "/out" + level+ turnoncase.replace(" ","+") + "+" + fname.replace(
        ".c", ".bin")
    turnofffinalcmd = "gcc " + level+" "+cmds + turnoffcase + " " + filepath + " -o " + fpath + "/out" + level+ turnoffcase.replace(" ","+") + "+" + fname.replace(
        ".c", ".bin")

    os.system(turnonfinalcmd)
    os.system(turnofffinalcmd)


def complie_with_pflags(filepath,currentcase,level,parentflags,flag):
    fpath, fname = ntpath.split(filepath)
    turnoncase= flag
    turnoffcase= flag[:2] + 'no-' + flag[2:]
    allflags=loadallvalidflags()

    cmds=""


    for f in allflags:
        if not (f == flag):
            if not f in parentflags:
                if currentcase == YES_CASE:
                    cmds = cmds + f + " "
                else:
                    cmds = cmds + f[:2] + 'no-' + f[2:] + " "

    if not len(parentflags) == 0:
        for cf in parentflags:
            cmds = cmds + cf + " "


    turnonfinalcmd = "gcc " + level+" " +cmds + turnoncase + " " + filepath + " -o " + fpath + "/out" + level+turnoncase.replace(" ","+") + "+" + fname.replace(
        ".c", ".bin")
    turnofffinalcmd = "gcc " + level+" "+cmds + turnoffcase + " " + filepath + " -o " + fpath + "/out" + level+ turnoffcase.replace(" ","+") + "+" + fname.replace(
        ".c", ".bin")

    os.system(turnonfinalcmd)
    os.system(turnofffinalcmd)

def OYFlagcomplie(filepath,testcmd,flag):
    fpath, fname = ntpath.split(filepath)
    turnoncase=testcmd+" "+flag
    turnoffcase=testcmd+" "+(flag[:2] + 'no-' + flag[2:])
    flags=loadallvalidflags()
    nocmds=""
    for f in flags:
        if not f ==flag:
            nocmds = nocmds+ f+" "

    turnonfinalcmd = "gcc " + nocmds + turnoncase + " " + filepath + " -o " + fpath + "/out" + turnoncase.replace(" ","+") + "+" + fname.replace(
        ".c", ".bin")
    turnofffinalcmd = "gcc " + nocmds + turnoffcase + " " + filepath + " -o " + fpath + "/out" + turnoffcase.replace(" ","+") + "+" + fname.replace(
        ".c", ".bin")
    os.system(turnonfinalcmd)
    os.system(turnofffinalcmd)


def ONFlagcomplie(filepath,testcmd,flag):
    fpath, fname = ntpath.split(filepath)
    turnoncase=testcmd+" "+flag
    turnoffcase=testcmd+" "+(flag[:2] + 'no-' + flag[2:])
    flags=loadallvalidflags()
    nocmds=""
    for f in flags:
        if not f ==flag:
            nocmds = nocmds+ f[:2] + 'no-' + f[2:] +" "

    turnonfinalcmd = "gcc " + turnoncase + " " +nocmds+ filepath + " -o " + fpath + "/out" + turnoncase.replace(" ","+") + "+" + fname.replace(
        ".c", ".bin")
    turnofffinalcmd = "gcc " + turnoffcase + " " +nocmds + filepath + " -o " + fpath + "/out" + turnoffcase.replace(" ","+") + "+" + fname.replace(
        ".c", ".bin")
    os.system(turnonfinalcmd)
    os.system(turnofffinalcmd)

def OFlagcomplie(filepath,testcmd,flag):
    fpath, fname = ntpath.split(filepath)
    turnoncase=testcmd+" "+flag
    turnoffcase=testcmd+" "+(flag[:2] + 'no-' + flag[2:])
    turnonfinalcmd = "gcc " + turnoncase + " " + filepath + " -o " + fpath + "/out" + turnoncase.replace(" ","+") + "+" + fname.replace(
        ".c", ".bin")
    turnofffinalcmd = "gcc " + turnoffcase + " " + filepath + " -o " + fpath + "/out" + turnoffcase.replace(" ","+") + "+" + fname.replace(
        ".c", ".bin")
    os.system(turnonfinalcmd)
    os.system(turnofffinalcmd)


def Ocomplie(filepath,testcmd):
    fpath, fname = ntpath.split(filepath)
    finalcmd = "gcc " + testcmd + " " + filepath + " -o " + fpath + "/out" + testcmd + "-" + fname.replace(
        ".c", ".bin")
    os.system(finalcmd)

def load_noflag_and_complie(filepath):
    f = open(flagfile, "r")
    fpath, fname = ntpath.split(filepath)
    for line in f:
        testcmd = line.strip()
        if('no' not in testcmd[2:4]):
            testcmd =  (testcmd[:2] + 'no-' + testcmd[2:])
            finalcmd = "gcc " + testcmd + " " + filepath + " -o " + fpath + "/out" + line.strip() + "-" + fname.replace(
                ".c", ".bin")

            os.system(finalcmd)

def compleflie_with_yes_flag(filepath,levels,flags):
    for level in levels:
        OYFlagcomplie(filepath, level, flags)




def compleflie_with_yes_flag(filepath,flag):
    OYFlagcomplie(filepath, "-O3",flag)
    OYFlagcomplie(filepath, "-O2",flag)
    OYFlagcomplie(filepath, "-O1",flag)
    OYFlagcomplie(filepath, "-O0",flag)
    OYFlagcomplie(filepath, "-Og",flag)
    OYFlagcomplie(filepath, "-Os",flag)

def compleflie_with_no_flag(filepath,flag):
    ONFlagcomplie(filepath, "-O3",flag)
    ONFlagcomplie(filepath, "-O2",flag)
    ONFlagcomplie(filepath, "-O1",flag)
    ONFlagcomplie(filepath, "-O0",flag)
    ONFlagcomplie(filepath, "-Og",flag)
    ONFlagcomplie(filepath, "-Os",flag)

def compleflie_with_singleflag(filepath,flag):
    OFlagcomplie(filepath, "-O3",flag)
    OFlagcomplie(filepath, "-O2",flag)
    OFlagcomplie(filepath, "-O1",flag)
    OFlagcomplie(filepath, "-O0",flag)
    OFlagcomplie(filepath, "-Og",flag)
    OFlagcomplie(filepath, "-Os",flag)

def loadallvalidflags():
    flags=[]
    f = open(validflags, "r")

    for line in f:
        testcmd = line.strip()
        flags.append(testcmd)

    return flags

def loadallflags():
    flags=[]
    f = open(finalflags, "r")

    for line in f:
        testcmd = line.strip()
        flags.append(testcmd)

    return flags


#pflags=["-fipa-icf","-fipa-cp","-ftree-builtin-call-dce","-fipa-bit-cp","-ftree-bit-ccp","-fgnu89-inline"]

#complie("/home/yue/Flie.c",NO_CASE,"-O1", pflags,"-fcrossjumping")
