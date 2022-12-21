def hex_dump(data:bytes,bytes_per_line=16)->str:
	off_pad=len(hex(len(data))[2:])
	data=[data[i:i+bytes_per_line] for i in range(0,len(data),bytes_per_line)]
	result=[]
	for i,v in enumerate(data):
		hx=["{0:02x}".format(x) for x in v]
		asc=[chr(x)  if x>=32 and x<=127 else "." for x in v]
		line=f"{i*bytes_per_line:0{off_pad}x}: "+" ".join(hx)+" "+"".join(asc)
		result.append(line)
	return "\n".join(result)

def main():
	data=bytes([i%256 for i in range(100)])
	print(hex_dump(data,32))

if __name__=="__main__":
	main()