import hashlib
import os
import angr

from collections import defaultdict




def gethashcode(path):

    md5 = hashlib.md5()
    if not path.endswith(".bin"):
        return
    proj=angr.Project(path,auto_load_libs=False)

    obj=proj.loader.main_object

    for sec in obj.sections:
            md5.update(str(sec).encode(encoding="utf-8"))
    return md5.hexdigest()

def get_flitered_files(filedir):
    dict_one_to_more = defaultdict(list)
    for r, d, f in os.walk(filedir):
        for file in f:
            try:
                hash = gethashcode(os.path.join(r, file))
                if not hash == None:
                    print(hash)
                    print(os.path.join(r, file))
                    dict_one_to_more[hash].append(os.path.join(r, file))
            except:
                continue
    return dict_one_to_more








