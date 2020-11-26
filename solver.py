import random,json

MAX_PROJECTS = {"type_a":30, "type_b": 39 , "type_c": 25}

def Error(s):
	print("[ERROR] - "+s)
	
def Info(s):
	print("[INFO ] - "+s)

def LoadStudenti():
	try:
		res = json.loads(open("students.json","rt").read())
		return res
	except Exception as e:
		Error("Fail to load studenti JSON file")
		Error(str(e))
		return None		

def Solve(studentsList, students, type_name, req_in_type, max_projects):
	max_per_student = int(len(students)/max_projects)+1
	count = [0]* (max_projects+1)
	random.shuffle(studentsList)
	scor = 0
	solution = {}
	for stud_id in studentsList:
		stud = students[stud_id]
		lst_opt = stud[type_name]
		found_solution = False
		for i in range(0,len(lst_opt)):
			if count[lst_opt[i]]<max_per_student:
				count[lst_opt[i]]+=1				
				#if interested in a project --> get a lower score, otherwise use a generic 100
				if i<stud[req_in_type]:					
					solution[stud_id] = (lst_opt[i],i)
					scor += i
				else:
					solution[stud_id] = (lst_opt[i],100)
					scor += 100
				found_solution = True
				break
		if not found_solution:
			Error("Unable to find a solution for ID: '"+stud_id+"' !!!")
			return None
	return (solution,scor)

def Solver(studentsList, students, prjType, maxTimes):
	global MAX_PROJECTS
	best = ({},0)
	type_name = "type_"+prjType.lower()
	req_in_type = "req_"+prjType.lower()
	prjCount = MAX_PROJECTS[type_name]
	for i in range(0,maxTimes):
		result = Solve(studentsList, students, type_name, req_in_type, prjCount)
		if result == None: return None
		if (i==0) or (result[1]<best[1]):
			best = result
			Info("Iteration: %d -> Score for '%s' = %d "%(i+1,type_name,best[1]))
	return best
	
def main():
	students = LoadStudenti()
	if students == None: return
	lst_students = []
	for stud_id in students:
		lst_students += [stud_id]
	Info("Number of students: "+str(len(students)))
	max_attempts = 5000
	res_A = Solver(lst_students,students,"A",max_attempts)
	res_B = Solver(lst_students,students,"B",max_attempts)
	res_C = Solver(lst_students,students,"C",max_attempts)
	
	#build the result 
	s = ""
	order_a = 0
	order_b = 0
	order_c = 0
	interested_in_a = 0
	interested_in_b = 0
	interested_in_c = 0
	for stud_id in students:
		s += "%s|A:%2d|B:%2d|C:%2d\n"%(stud_id,res_A[0][stud_id][0],res_B[0][stud_id][0],res_C[0][stud_id][0])
		if res_A[0][stud_id][1]<3:
			order_a+=1
		if res_B[0][stud_id][1]<3:
			order_b+=1
		if res_C[0][stud_id][1]<3:
			order_c+=1
		if students[stud_id]["req_a"]>0:
			interested_in_a+=1
		if students[stud_id]["req_b"]>0:
			interested_in_b+=1
		if students[stud_id]["req_c"]>0:
			interested_in_c+=1			
	print("Received top 3 projects for A: %d / %d [%3.2f%%]"%(order_a, interested_in_a, order_a*100.0/interested_in_a))
	print("Received top 3 projects for B: %d / %d [%3.2f%%]"%(order_b, interested_in_b, order_b*100.0/interested_in_b))
	print("Received top 3 projects for C: %d / %d [%3.2f%%]"%(order_c, interested_in_c, order_c*100.0/interested_in_c))
	#save the results
	try:
		open("students.projects","wt").write(s)
	except Exception as e:
		Error("Fail to create students.projects file ")
		Error(str(e))
		return	
	
if __name__ == "__main__":
	main()