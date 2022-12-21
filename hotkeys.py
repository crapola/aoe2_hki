import hki


class Hotkeys:
	def __init__(self,path:str):
		self.data=hki.hki_load(path)

	def __str__(self)->str:
		return hki.hki_display(self.data)

	def export(self,path:str):
		with open(path,"wb") as f:
			f.write(self.data)

	def find_key(self,keycode:int)->list:
		return [i for i in hki.HOTKEY_OFFSETS if self.data[i]==keycode]

	def save(self,path:str):
		hki.hki_save(path,self.data)

	def swap(self,a:int,b:int):
		""" a and b are keycodes. """
		lst_a=self.find_key(a)
		lst_b=self.find_key(b)
		ba=bytearray(self.data)
		for i in lst_a:
			ba[i]=b
		for i in lst_b:
			ba[i]=a
		self.data=bytes(ba)