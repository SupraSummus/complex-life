import math
import os
import sys
from struct import pack

from nbt.world import WorldFolder
from PIL import Image

# List of blocks to ignore
# Uncomment all the lines to show underground structures
# TODO: move this list into a separate config file
block_ignore = [
    'minecraft:air',  # At least this one
    #    'cave_air', 'water', 'lava', 'snow', 'ice',
    #    'grass', 'tall_grass', 'dead_bush',
    #    'seagrass', 'tall_seagrass', 'kelp', 'kelp_plant',
    #    'dandelion', 'poppy', 'oxeye_daisy', 'white_tulip',
    #    'azure_bluet', 'lilac', 'rose_bush', 'peony', 'blue_orchid',
    #    'lily_pad', 'sugar_cane', 'vine', 'pumpkin', 'cactus',
    #    'wheat', 'potatoes', 'beetroots', 'carrots',
    #    'oak_leaves', 'dark_oak_leaves', 'birch_leaves',
    #    'acacia_leaves', 'spruce_leaves',
    #    'oak_log', 'dark_oak_log', 'birch_log',
    #    'acacia_log', 'spruce_log',
    #    'brown_mushroom', 'red_mushroom',
    #    'brown_mushroom_block', 'red_mushroom_block', 'mushroom_stem',
    #    'grass_block', 'grass_path', 'farmland', 'dirt',
    #    'stone', 'sand', 'gravel', 'clay',
    #    'sandstone', 'diorite', 'andesite', 'granite', 'obsidian',
    #    'coal_ore', 'iron_ore', 'gold_ore', 'diamond_ore',
    #    'redstone_ore', 'lapis_ore', 'emerald_ore',
    #    'cobweb',
]


# Map of block colors from names
# Legacy block numeric identifiers are now hidden by Block class
# and mapped to alpha identifiers in best effort
# TODO: move this map into a separate config file
block_colors = {
    'acacia_leaves': {'h': 114, 's': 64, 'l': 22},
    'acacia_log': {'h': 35, 's': 93, 'l': 30},
    'air': {'h': 0, 's': 0, 'l': 0},
    'andesite': {'h': 0, 's': 0, 'l': 32},
    'azure_bluet': {'h': 0, 's': 0, 'l': 100},
    'bedrock': {'h': 0, 's': 0, 'l': 10},
    'birch_leaves': {'h': 114, 's': 64, 'l': 22},
    'birch_log': {'h': 35, 's': 93, 'l': 30},
    'blue_orchid': {'h': 0, 's': 0, 'l': 100},
    'bookshelf': {'h': 0, 's': 0, 'l': 100},
    'brown_mushroom': {'h': 0, 's': 0, 'l': 100},
    'brown_mushroom_block': {'h': 0, 's': 0, 'l': 100},
    'cactus': {'h': 126, 's': 61, 'l': 20},
    'cave_air': {'h': 0, 's': 0, 'l': 0},
    'chest': {'h': 0, 's': 100, 'l': 50},
    'clay': {'h': 7, 's': 62, 'l': 23},
    'coal_ore': {'h': 0, 's': 0, 'l': 10},
    'cobblestone': {'h': 0, 's': 0, 'l': 25},
    'cobblestone_stairs': {'h': 0, 's': 0, 'l': 25},
    'crafting_table': {'h': 0, 's': 0, 'l': 100},
    'dandelion': {'h': 60, 's': 100, 'l': 60},
    'dark_oak_leaves': {'h': 114, 's': 64, 'l': 22},
    'dark_oak_log': {'h': 35, 's': 93, 'l': 30},
    'dark_oak_planks': {'h': 35, 's': 93, 'l': 30},
    'dead_bush': {'h': 0, 's': 0, 'l': 100},
    'diorite': {'h': 0, 's': 0, 'l': 32},
    'dirt': {'h': 27, 's': 51, 'l': 15},
    'end_portal_frame': {'h': 0, 's': 100, 'l': 50},
    'farmland': {'h': 35, 's': 93, 'l': 15},
    'fire': {'h': 55, 's': 100, 'l': 50},
    'flowing_lava': {'h': 16, 's': 100, 'l': 48},
    'flowing_water': {'h': 228, 's': 50, 'l': 23},
    'glass_pane': {'h': 0, 's': 0, 'l': 100},
    'granite': {'h': 0, 's': 0, 'l': 32},
    'grass': {'h': 94, 's': 42, 'l': 25},
    'grass_block': {'h': 94, 's': 42, 'l': 32},
    'gravel': {'h': 21, 's': 18, 'l': 20},
    'ice': {'h': 240, 's': 10, 'l': 95},
    'infested_stone': {'h': 320, 's': 100, 'l': 50},
    'iron_ore': {'h': 22, 's': 65, 'l': 61},
    'iron_bars': {'h': 22, 's': 65, 'l': 61},
    'ladder': {'h': 35, 's': 93, 'l': 30},
    'lava': {'h': 16, 's': 100, 'l': 48},
    'lilac': {'h': 0, 's': 0, 'l': 100},
    'lily_pad': {'h': 114, 's': 64, 'l': 18},
    'lit_pumpkin': {'h': 24, 's': 100, 'l': 45},
    'mossy_cobblestone': {'h': 115, 's': 30, 'l': 50},
    'mushroom_stem': {'h': 0, 's': 0, 'l': 100},
    'oak_door': {'h': 35, 's': 93, 'l': 30},
    'oak_fence': {'h': 35, 's': 93, 'l': 30},
    'oak_fence_gate': {'h': 35, 's': 93, 'l': 30},
    'oak_leaves': {'h': 114, 's': 64, 'l': 22},
    'oak_log': {'h': 35, 's': 93, 'l': 30},
    'oak_planks': {'h': 35, 's': 93, 'l': 30},
    'oak_pressure_plate': {'h': 35, 's': 93, 'l': 30},
    'oak_stairs': {'h': 114, 's': 64, 'l': 22},
    'packed_ice': {'h': 240, 's': 10, 'l': 95},
    'peony': {'h': 0, 's': 0, 'l': 100},
    'pink_tulip': {'h': 0, 's': 0, 'l': 0},
    'poppy': {'h': 0, 's': 100, 'l': 50},
    'pumpkin': {'h': 24, 's': 100, 'l': 45},
    'rail': {'h': 33, 's': 81, 'l': 50},
    'red_mushroom': {'h': 0, 's': 50, 'l': 20},
    'red_mushroom_block': {'h': 0, 's': 50, 'l': 20},
    'rose_bush': {'h': 0, 's': 0, 'l': 100},
    'sugar_cane': {'h': 123, 's': 70, 'l': 50},
    'sand': {'h': 53, 's': 22, 'l': 58},
    'sandstone': {'h': 48, 's': 31, 'l': 40},
    'seagrass': {'h': 94, 's': 42, 'l': 25},
    'sign': {'h': 114, 's': 64, 'l': 22},
    'spruce_leaves': {'h': 114, 's': 64, 'l': 22},
    'spruce_log': {'h': 35, 's': 93, 'l': 30},
    'stone': {'h': 0, 's': 0, 'l': 32},
    'stone_slab': {'h': 0, 's': 0, 'l': 32},
    'tall_grass': {'h': 94, 's': 42, 'l': 25},
    'tall_seagrass': {'h': 94, 's': 42, 'l': 25},
    'torch': {'h': 60, 's': 100, 'l': 50},
    'snow': {'h': 240, 's': 10, 'l': 85},
    'snow_block': {'h': 240, 's': 10, 'l': 95},
    'spawner': {'h': 180, 's': 100, 'l': 50},
    'vine': {'h': 114, 's': 64, 'l': 18},
    'wall_torch': {'h': 60, 's': 100, 'l': 50},
    'water': {'h': 228, 's': 50, 'l': 23},
    'wheat': {'h': 123, 's': 60, 'l': 50},
    'white_wool': {'h': 0, 's': 0, 'l': 100},
}
block_colors = {
    f'minecraft:{name}': color
    for name, color in block_colors.items()
}


unknown_colors = {}


def get_map(chunk):
    # Show an image of the chunk from above
    pixels = b''

    for z in range(16):
        for x in range(16):
            # Find the highest block in this column
            max_height = chunk.get_max_height()
            for y in range(max_height, -1, -1):
                block_id = chunk.get_block(x, y, z)
                if block_id is not None and block_id not in block_ignore:
                    break

            if block_id is not None:
                if block_id in block_colors:
                    color = block_colors[block_id]
                else:
                    color = {'h': 0, 's': 0, 'l': 100}
                    if block_id not in unknown_colors:
                        unknown_colors[block_id] = 0
                    unknown_colors[block_id] += 1
            else:
                color = {'h': 0, 's': 0, 'l': 0}

            rgb = hsl2rgb(color['h'], color['s'], color['l'])

            pixels += pack('BBB', rgb[0], rgb[1], rgb[2])

    im = Image.frombytes('RGB', (16, 16), pixels)
    return im


def report_unknown_colors():
    if unknown_colors:
        print("Unknown block colors:")
        for block_id, count in unknown_colors.items():
            print(f"{block_id}: {count}")
    unknown_colors.clear()


# From http://www.easyrgb.com/index.php?X=MATH&H=19#text19
def hsl2rgb(H, S, L):
    H = H / 360.0
    S = S / 100.0  # Turn into a percentage
    L = L / 100.0
    if S == 0:
        return (int(L * 255), int(L * 255), int(L * 255))
    var_2 = L * (1 + S) if (L < 0.5) else (L + S) - (S * L)
    var_1 = 2 * L - var_2

    def hue2rgb(v1, v2, vH):
        if vH < 0:
            vH += 1
        if vH > 1:
            vH -= 1
        if (6 * vH) < 1:
            return v1 + (v2 - v1) * 6 * vH
        if (2 * vH) < 1:
            return v2
        if (3 * vH) < 2:
            return v1 + (v2 - v1) * (2 / 3.0 - vH) * 6
        return v1

    R = int(255 * hue2rgb(var_1, var_2, H + (1.0 / 3)))
    G = int(255 * hue2rgb(var_1, var_2, H))
    B = int(255 * hue2rgb(var_1, var_2, H - (1.0 / 3)))
    return (R, G, B)


def main(world_folder):
    world = WorldFolder(world_folder)
    bb = world.get_boundingbox()
    world_map = Image.new('RGB', (16 * bb.lenx(), 16 * bb.lenz()))
    t = world.chunk_count()
    try:
        i = 0.0
        for chunk in world.iter_chunks():
            if i % 50 == 0:
                sys.stdout.write('Rendering image')
            elif i % 2 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()
            elif i % 50 == 49:
                sys.stdout.write('%5.1f%%\n' % (100 * i / t))
                report_unknown_colors()
            i += 1
            chunkmap = get_map(chunk)
            x, z = chunk.get_coords()
            world_map.paste(chunkmap, (16 * (x - bb.minx), 16 * (z - bb.minz)))
        print(' done\n')
        filename = os.path.basename(world_folder) + '.png'
        world_map.save(filename, 'PNG')
        print('Saved map as %s' % filename)
    except KeyboardInterrupt:
        print(' aborted\n')
        filename = os.path.basename(world_folder) + '.partial.png'
        world_map.save(filename, 'PNG')
        print('Saved map as %s' % filename)
        return 75  # EX_TEMPFAIL

    return 0  # NOERR


if __name__ == '__main__':
    world_folder = '~/.minecraft/saves/New World'
    world_folder = os.path.expanduser(world_folder)
    # clean path name, eliminate trailing slashes. required for os.path.basename()
    world_folder = os.path.normpath(world_folder)
    if not os.path.exists(world_folder):
        print('No such folder as ' + world_folder)
        sys.exit(72)  # EX_IOERR

    main(world_folder)
