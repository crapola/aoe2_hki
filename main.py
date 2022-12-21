from hex_dump import hex_dump
from hotkeys import Hotkeys


def main():
	hk=Hotkeys("default.hki")
	hk.swap(ord('A'),ord('Q'))
	hk.swap(ord('W'),ord('Z'))
	print(hk)
	hk.save("azerty.hki")

if __name__=="__main__":
	main()