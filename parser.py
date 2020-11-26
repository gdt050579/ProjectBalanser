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
	res["req_a"] = len(res["type_a"])
	res["req_b"] = len(res["type_b"])
	res["req_c"] = len(res["type_c"])
	return res
	
def DebugPrintBalanceList(lst):
	for id in range(0,len(lst)):
		print("ID:%2d, Scor:%5d, No_Students:%3d"%(id,lst[id]["scor"],len(lst[id]["no_students"])))

def SortFunction(scor,no_students_count):
	if no_students_count==0:
		return 10000000 # a very large number
	else:
		return scor
		
def BalanceID(type_name,max_count,students):
	cnt = []
	for i in range(0,max_count):
		cnt += [{"id":i+1, "scor":0,"students":{},"no_students":[]}]	
	for stud_id in students:
		scor = 100
		stud = students[stud_id]
		for ids in stud[type_name]:
			cnt[ids-1]["scor"] += scor
			cnt[ids-1]["students"][stud_id] = 1
			scor-=1
	#Create a list with students that do not appear for every ID
	for i in range(0,max_count):
		for stud_id in students:
			if stud_id not in cnt[i-1]["students"]:
				cnt[i-1]["no_students"]+=[stud_id]
	
	#balansez
	iter = 0
	while True:
		cnt.sort(key = lambda x: SortFunction(x["scor"],len(x["no_students"])))
		if len(cnt[0]["no_students"])==0:
			break
		obj = cnt[0]
		stud_id = obj["no_students"].pop()
		stud = students[stud_id]
		stud[type_name]+=[obj["id"]]
		obj["scor"] += 101-len(stud[type_name])
		iter+=1
	#DebugPrintBalanceList(cnt)	
	
def ListToString(students,student_id,type_name):
	s = ""
	list = students[student_id][type_name]
	for i in list:
		s += str(i)+","
	s = s[:-1]
	return s
def CreatePreferenceList(students):
	res = ""
	for stud_id in students:
		res += stud_id+"|"+ListToString(students,stud_id,"type_a")+"|"+ListToString(students,stud_id,"type_b")+"|"+ListToString(students,stud_id,"type_c")+"\n"
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
	BalanceID("type_a",30,d)	
	BalanceID("type_b",39,d)
	BalanceID("type_c",25,d)	
	
	try:
		res = json.dumps(d,indent=4)
		open("students.json","wt").write(res)
		open("students.txt","wt").write(CreatePreferenceList(d))
	except Exception as e:
		Error("Fail to create json or txt file ")
		Error(str(e))
		return

if __name__ == "__main__":
	main()
	
