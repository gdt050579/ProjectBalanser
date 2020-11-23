import os,sys,json

HIDE_PERSONAL_INFORMATION = False

def Error(s):
	print("[ERROR] - "+s)

def ProcessIDList(lst, maxID):
	w = lst.replace(" ",",").replace("\t",",").strip().split(",")
	l = []
	already_added = {}
	for strN in w:
		try:
			value = int(strN)
			if (value>=1) and (value<=maxID) and (value not in already_added):
				l+=[value]
				already_added[value] = 1
		except:
			pass
	return l

def ParseOneLine(line):
	global HIDE_PERSONAL_INFORMATION
	#format: TimeStamp,Email,Name,ID,TypeA,TypeB,TypeC
	res = {}
	data = line.split(",",4)
	if HIDE_PERSONAL_INFORMATION:
		res["email"] = "*"
		res["name"] = "*"
	else:
		res["email"] = data[1].strip()
		res["name"] = data[2].strip()
	res["id"] = data[3].strip().upper()
	l = []
	state = 1
	content = ""
	for ch in data[4]:
		if ch=='"':			
			state = 3-state
			continue
		if (ch==',') and (state==1):
			l += [content]
			content = ""
			continue		
		content+=ch
	l += [content]
	if len(l)!=3:
		Error("Invalid format --> expecting 3 preferences")
		return None
	
	res["type_a"] = ProcessIDList(l[0],30)
	res["type_b"] = ProcessIDList(l[1],39)
	res["type_c"] = ProcessIDList(l[2],25)
	
	return res
	
def LoadStudents(fname):
	d = {}
	try:
		for line in open(fname,"rt"):
			line = line.strip()
			if len(line) == 0: continue
			if line.startswith("Timestamp,Email Address,"): continue
			res = ParseOneLine(line)
			if res==None:
				Error("Invalid line: "+line)
				return None
			if res["id"] in d:
				Error("ID '"+res["id"]+"' has been used twice")
				return None
			d[res["id"]] = res
		return d
	except Exception as e:
		Error("Fail to read file: "+fname)
		Error(str(e))
		return None


def main():
	if len(sys.argv)!=2:
		Error("Missing cvs file with students options")
		return
	d = LoadStudents(sys.argv[1])
	if d==None:
		return
	try:
		res = json.dumps(d,indent=4)
		open("students.json","wt").write(res)
	except Exception as e:
		Error("Fail to create json file ")
		Error(str(e))
		return

if __name__ == "__main__":
	main()
