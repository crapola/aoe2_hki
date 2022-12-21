from hki import hki_load


def hki_key_offsets()->list:
	""" Get key offsets using a file where they are all assigned to X. """
	data=hki_load("all_to_x.hki")
	search_bytes=b"X\0\0\0"
	lst=[]
	q=-1
	while True:
		q=data.find(search_bytes,q+1)
		if q!=-1:
			lst.append(q)
		else:
			break
	return lst

def main():
	print(hki_key_offsets())

if __name__=="__main__":
	main()