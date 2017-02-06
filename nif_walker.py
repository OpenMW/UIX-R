from pyffi.formats.nif import NifFormat
from os import path
from sys import argv, exit, stdout

# UIX_PATH = "../../../Private/UIX/UIX FILES/Data Files/"
# UIX_PATH = "../../../Private/UIX/UIX FILES/Data Files/Meshes/TOE/RedMoonGa01.NIF"


def find_external_assets(data, assets):
    """ recursively find any external assets linked into a nif"""

    if isinstance(data, list):
        for node in data:
            if node.__class__.__name__ == 'NiNode':
                find_external_assets(node.children, assets)
            elif node.__class__.__name__ == 'NiTriShape':
                find_external_assets(node.properties, assets)
            else:
                find_external_assets(node, assets)

    if data.__class__.__name__ == 'NiSourceTexture':
        assets.append(data.file_name)
    elif data.__class__.__name__ == 'NiTexturingProperty':
        if data.has_base_texture:
            find_external_assets(data.base_texture.source, assets)
        if data.has_bump_map_texture:
            find_external_assets(data.bump_map_texture.source, assets)
        if data.has_dark_texture:
            find_external_assets(data.dark_texture.source, assets)
        if data.has_gloss_texture:
            find_external_assets(data.gloss_texture.source, assets)
        if data.has_glow_texture:
            find_external_assets(data.glow_texture.source, assets)
        if data.has_normal_texture:
            find_external_assets(data.normal_texture.source, assets)
        if data.has_detail_texture:
            find_external_assets(data.detail_texture.source, assets)
        if data.has_unknown_2_texture:
            find_external_assets(data.unknown_2_texture.source, assets)
        if data.has_decal_0_texture:
            find_external_assets(data.decal_0_texture.source, assets)
        if data.has_decal_1_texture:
            find_external_assets(data.decal_1_texture.source, assets)
        if data.has_decal_2_texture:
            find_external_assets(data.decal_2_texture.source, assets)
        if data.has_decal_3_texture:
            find_external_assets(data.decal_3_texture.source, assets)


def walk_nif(nif_path, use_stdout=True):
    if not path.exists(nif_path):
        exit("Path `{0}` not found.".format(nif_path))

    all_assets = []
    for stream, data in NifFormat.walkData(nif_path):
        try:
            if use_stdout:
                print(stream.name, sep='', end=', ', file=stdout, flush=True)
            data.read(stream)
            assets = []
            find_external_assets(data.roots, assets)
            assets = set(assets)  # remove duplicates
            assets_string = "{0}".format(b', '.join(assets).decode(encoding="ISO-8859-1"))
            all_assets.append(assets_string)
            if use_stdout:
                print(assets_string, sep=', ', end='\n', file=stdout, flush=True)
        except ValueError as ex:
            print(" Error with {0}: {1}".format(stream.name, str(ex.args)), sep='', end='\n', file=stdout, flush=True)
        except Exception as ex:
            print(ex)
            raise
    return all_assets


if __name__ == "__main__":
    if len(argv) == 2:
        walk_nif(argv[1])
    else:
        exit("No path given.")
