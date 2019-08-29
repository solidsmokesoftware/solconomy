import source.common.world as world

w = world.World()
w.set_world(1001, 250, 250)

i = 0
height_sum = 0
water_sum = 0
temp_sum = 0
veg_sum = 0
mana_sum = 0

height_max = -100
water_max = -100
temp_max = -1000
veg_max = -100
mana_max = -100

height_min = 100
water_min = 100
temp_min = 1000
veg_min = 100
mana_min = 100

height_dict = {}
water_dict = {}
temp_dict = {}
veg_dict = {}
mana_dict = {}

for x in range(-250,250):
        for y in range(-250,250):
                t = world.Tile()
                tile = w.gen_tile(x, y, t)
                i += 1
                height_sum += tile.height
                water_sum += tile.water
                temp_sum += tile.temp
                veg_sum += tile.veg
                mana_sum += tile.mana

                if tile.height > height_max:
                        height_max = tile.height
                elif tile.height < height_min:
                        height_min = tile.height

                if tile.water > water_max:
                        water_max = tile.water
                elif tile.water < water_min:
                        water_min = tile.water

                if tile.temp > temp_max:
                        temp_max = tile.temp
                elif tile.temp < temp_min:
                        temp_min = tile.temp

                if tile.veg > veg_max:
                        veg_max = tile.veg
                elif tile.veg < veg_min:
                        veg_min = tile.veg

                if tile.mana > mana_max:
                        mana_max = tile.mana
                elif tile.mana < mana_min:
                        mana_min = tile.mana



                height_str = str(tile.height)[0:3]
                water_str = str(tile.water)[0:3]
                temp_str = str(tile.temp)[0:3]
                veg_str = str(tile.veg)[0:3]
                mana_str = str(tile.mana)[0:3]

                if height_str in height_dict:
                        height_dict[height_str] += 1
                else:
                        height_dict[height_str] = 1

                if water_str in water_dict:
                        water_dict[water_str] += 1
                else:
                        water_dict[water_str] = 1

                if temp_str in temp_dict:
                        temp_dict[temp_str] += 1
                else:
                        temp_dict[temp_str] = 1

                if veg_str in veg_dict:
                        veg_dict[veg_str] += 1
                else:
                        veg_dict[veg_str] = 1

                if mana_str in mana_dict:
                        mana_dict[mana_str] += 1
                else:
                        mana_dict[mana_str] = 1

p = 100.0 / i

print ('Height')
print ('Max: %s' % height_max)
print ('Min: %s' % height_min)
print ('Avg: %s' % (height_sum / i))
print ('Distribtuion')
d = []
for v in height_dict:
        d.append(v)
d.sort()
for v in d:
        print('%s: %s (%s percent)' % (v, height_dict[v], height_dict[v] * p))

print ('Water')
print ('Max: %s' % water_max)
print ('Min: %s' % water_min)
print ('Avg: %s' % (water_sum / i))
print ('Distribtuion')
d = []
for v in water_dict:
        d.append(v)
d.sort()
for v in d:
        print('%s: %s (%s percent)' % (v, water_dict[v], water_dict[v] * p))

print ('Temp')
print ('Max: %s' % temp_max)
print ('Min: %s' % temp_min)
print ('Avg: %s' % (temp_sum / i))
print ('Distribtuion')
d = []
for v in temp_dict:
        d.append(v)
d.sort()
for v in d:
        print('%s: %s (%s percent)' % (v, temp_dict[v], temp_dict[v] * p))

print ('Veg')
print ('Max: %s' % veg_max)
print ('Min: %s' % veg_min)
print ('Avg: %s' % (veg_sum / i))
print ('Distribtuion')
d = []
for v in veg_dict:
        d.append(v)
d.sort()
for v in d:
        print('%s: %s (%s percent)' % (v, veg_dict[v], veg_dict[v] * p))

print ('Mana')
print ('Max: %s' % mana_max)
print ('Min: %s' % mana_min)
print ('Avg: %s' % (mana_sum / i))
print ('Distribtuion')
d = []
for v in mana_dict:
        d.append(v)
d.sort()
for v in d:
        print('%s: %s (%s percent)' % (v, mana_dict[v], mana_dict[v] * p))


'''
i = 0
total = 0
dist = {}
max_v = -100
min_v = 100

for x in range(500):
        for y in range(500):
                v =w.height_table.smooth_noise2(x, y, 1, 10.0, 2, 1.2)
                i += 1
                total += v
                veg_sum = str(v)[0:3]
                if veg_sum in dist: dist[veg_sum] += 1
                else: dist[_sum] = 1
                if v > max_v: max_v = v
                elif v < min_v: min_v = v

d = []
for v in dist:
    d.append(v)

d.sort()

p = 100.0 / i
for v in d:
    print(v, dist[v], dist[v] * p)
'''
