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

starboi_md5 = None
with open("Manifests/starboi.manifest", 'r') as content_file:
    starboi_md5 = content_file.read()

vurt_md5 = None
with open("Manifests/vurt.manifest", 'r') as content_file:
    vurt_md5 = content_file.read()

jarvik_md5 = None
with open("Manifests/jarvik.manifest", 'r') as content_file:
    jarvik_md5 = content_file.read()

glory_md5 = None
with open("Manifests/glory.manifest", 'r') as content_file:
    glory_md5 = content_file.read()

ules_md5 = None
with open("Manifests/ules.manifest", 'r') as content_file:
    ules_md5 = content_file.read()


def validate(md5_list):
    print("\nComparing md5sum of UIX:R to the other files.")
    beth_counter = starboi_counter = vurt_counter = jarvik_counter = glory_counter = ules_counter = 0
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
            if md5 in starboi_md5:
                starboi_counter += 1
                print("{0},{1},Found in StarBoi's work".format(md5, rest))
            if md5 in vurt_md5:
                vurt_counter += 1
                print("{0},{1},Found in Vurt's work".format(md5, rest))
            if md5 in jarvik_md5:
                jarvik_counter += 1
                print("{0},{1},Found in Jarvik bsa".format(md5, rest))
            if md5 in glory_md5:
                glory_counter += 1
                print("{0},{1},Found in TheGloryRoad".format(md5, rest))
            if md5 in ules_md5:
                ules_counter += 1
                print("{0},{1},Found in Ules' Farm".format(md5, rest))

    total = beth_counter + starboi_counter + vurt_counter + jarvik_counter + glory_counter + \
        ules_counter

    print("""\
Out of {0} files, found: {1}
  {2} bethesda files
  {3} starboi files
  {4} vurt files
  {5} jarvik files
  {6} glory files
  {7} ules files""".format(
        len(md5_list.split('\n'))-1, total, beth_counter, starboi_counter, vurt_counter,
        jarvik_counter, glory_counter, ules_counter))

    
# uixr files
uixr_md5 = None
with open("Manifests/UIXR.manifest", 'r') as content_file:
    uix_md5 = content_file.read()
    validate(uix_md5)

