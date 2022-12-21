import zlib

# Use offsets.py to create this list.
HOTKEY_OFFSETS=[12, 24, 36, 72, 84, 96, 108, 120, 132, 144, 156, 168, 180, 192, 204, 216, 228, 240, 256, 268, 280, 292, 304, 316, 328, 340, 352, 376, 388, 400, 412, 424, 436, 448, 484, 496, 508, 520, 532, 544, 556, 568, 580, 592, 604, 616, 628, 640, 652, 664, 676, 688, 700, 712, 724, 736, 748, 760, 772, 784, 796, 808, 820, 832, 848, 860, 872, 884, 896, 908, 920, 932, 944, 956, 968, 980, 992, 1004, 1016, 1028, 1040, 1052, 1064, 1076, 1088, 1100, 1112, 1124, 1136, 1152, 1164, 1176, 1188, 1200, 1212, 1224, 1236, 1248, 1260, 1272, 1284, 1296, 1308, 1320, 1332, 1344, 1356, 1368, 1380, 1392, 1404, 1416, 1428, 1440, 1452, 1464, 1476, 1488, 1500, 1512, 1524, 1536, 1548, 1560, 1572, 1584, 1596, 1608, 1620, 1632, 1644, 1656, 1668, 1680, 1692, 1704, 1716, 1728, 1740, 1752, 1764, 1776, 1788, 1800, 1812, 1824, 1836, 1848, 1860, 1872, 1884, 1896, 1908, 1920, 1932, 1944, 1956, 1968, 1980, 1992, 2004, 2016, 2028, 2040, 2052, 2064, 2076, 2088, 2100, 2112, 2128, 2140, 2152, 2164, 2320, 2336, 2348, 2360, 2372, 2384, 2396, 2408, 2420, 2432, 2444, 2456, 2468, 2480, 2492, 2504, 2580, 2592, 2604, 2616, 2628, 2640, 2652, 2664, 2676, 2688, 2712, 2724, 2736, 2748, 2764, 2776, 2788, 2800, 2812, 2824, 2836, 2848, 2860, 2872, 2884, 2908, 2920, 2932, 2944, 2956, 2968, 2980, 2992, 3004, 3040, 3052, 3064, 3076, 3088, 3100, 3112, 3124, 3136, 3148, 3160, 3176, 3236, 3248, 3260, 3272, 3284, 3296, 3308, 3324, 3336, 3348, 3360, 3372, 3384, 3408, 3420, 3432, 3444, 3456, 3468, 3480, 3492, 3504, 3516, 3528, 3540, 3556, 3568, 3580, 3592, 3604, 3616, 3628, 3640, 3652, 3664, 3676, 3692, 3704, 3716, 3728, 3740, 3752, 3764, 3776, 3788, 3800, 3812, 3824, 3836, 3848, 3864, 3876, 3888, 3900, 3912, 3924, 3936, 3948, 3960, 3972, 3984, 3996, 4008, 4020, 4032, 4044, 4060, 4072, 4084, 4096, 4108, 4120, 4132, 4144, 4156, 4168, 4180, 4196, 4208, 4220, 4232, 4244, 4256, 4268, 4280, 4292, 4304, 4316, 4328, 4344, 4356, 4368, 4380, 4392, 4404, 4416, 4428, 4440, 4452, 4468, 4480, 4492, 4504, 4516, 4528, 4540, 4552, 4564, 4576, 4588, 4600, 4616, 4628, 4640, 4656, 4668, 4684, 4700, 4712, 4724, 4736, 4748, 4764, 4776, 4788, 4800, 4812, 4824, 4836, 4848, 4860, 4872, 4884, 4900, 4912, 4924, 4936, 4948, 4964, 4976, 4988]

def aoe2_keyvals()->dict:
	"""
	Dictionary used to translate action ids.
	key-value-strings-utf8.txt is sourced from:
	AoE2DE/resources/<lang>/strings/key-value/key-value-strings-utf8.txt
	"""
	with open("key-value-strings-utf8.txt","r",encoding="utf8") as f:
		lines=f.readlines()
		kv=[x.split(" ",maxsplit=1) for x in lines]
		kv=[x for x in kv if len(x)==2]
		kv={int(k):v[:-1] for k,v in kv if k.isdigit()}
		return kv

def hki_display(data:bytes)->str:
	""" Dump list of hotkeys from binary data. """
	keyvals=aoe2_keyvals()
	result=[]
	for i in HOTKEY_OFFSETS:
		key=data[i]
		action_id=int.from_bytes(data[i+4:i+8],"little")
		modifiers=data[i+8:i+12]
		result.append(f"{hex(i)}: {hotkey_string(key,modifiers)}: {keyvals[action_id]}")
	return "\n".join(result)

def hki_load(path:str)->bytes:
	""" Decompress .hki file. """
	with open(path,"rb") as f:
		return zlib.decompress(f.read(),wbits=-8)

def hki_save(path:str,data:bytes):
	""" Compress and save .hki file. """
	with open(path,"wb") as f:
		f.write(zlib.compress(data)[2:])

def hotkey_string(b:int,mods:bytes)->str:
	""" Convert hotkey from binary data into something readable. """
	ctrl=mods[0]==1
	alt=mods[1]==1
	shift=mods[2]==1
	modstring=f"{'Ctrl+' if ctrl else ''}{'Alt+' if alt else ''}{'Shift+' if shift else ''}"
	keycodes=key_codes()
	try:
		letter=keycodes[b].strip()
		if letter[:3]=="Oem":
			letter=letter[3:].capitalize()
	except KeyError:
		letter="???"
	return f"{modstring}{letter}"

def key_codes()->dict:
	"""
	Dictionary used to translate keycodes to english.
	keycodes.txt content is taken from:
	https://learn.microsoft.com/en-us/dotnet/api/system.windows.forms.keys
	"""
	with open("keycodes.txt","r") as f:
		lines=f.readlines()[::2]
		keys_dict=dict()
		for line in lines:
			kv=line.split(',')
			name=kv[0]
			value=int(kv[1])
			keys_dict[value]=name
		return keys_dict