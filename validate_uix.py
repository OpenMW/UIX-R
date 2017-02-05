#!/usr/bin/python


# bethesda files
morrowind_md5 = None
with open("Manifests/morrowind.manifest", 'r') as content_file:
    morrowind_md5 = content_file.read()
    
tribunal_md5 = None
with open("Manifests/tribunal.manifest", 'r') as content_file:
    tribunal_md5 = content_file.read()
    
bloodmoon_md5 = None
with open("Manifests/bloodmoon.manifest", 'r') as content_file:
    bloodmoon_md5 = content_file.read()
    

def validate(md5_list):
    print("\nComparing md5sum of UIX:R to the contents Bethesda's BSA files.")
    beth_counter = 0
    for line in md5_list.split('\n'):
        if len(line) > 0:
            md5, rest = line.split(",", 1)
            if md5 in morrowind_md5:
                beth_counter += 1
                print("{0},{1},Found in Morrowind.bsa".format(md5, rest))
            if md5 in tribunal_md5:
                beth_counter += 1
                print("{0},{1},Found in Tribunal.bsa".format(md5, rest))
            if md5 in bloodmoon_md5:
                beth_counter += 1
                print("{0},{1},Found in Bloodmoon.bsa".format(md5, rest))
                
    print("Out of {0} files, found {1} bethesda files.\n".format(
        len(md5_list.split('\n'))-1, beth_counter))

    
# uixr files
uixr_md5 = None
with open("Manifests/UIXR.manifest", 'r') as content_file:
    uix_md5 = content_file.read()
    validate(uix_md5)

