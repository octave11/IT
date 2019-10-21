import socket 
import threading               
  
s = socket.socket()          
print("Socket successfully created !!!")
port = 12340                
  
s.bind(('', port))         
print("socket binded to : "+str(port)) 
  
s.listen(5)      
print("Socket is listening...")            


num_clients = input("Enter Number of Clients : ")
count=0

client = {}
addr = {}
client_pairs = {}
managers = set()

def receive(client_id):

	client_pairs[client_id]={}
	
	while True:

		mesg = client[client_id].recv(1024).decode()
			
		mesg = mesg.split(" ")
		i=0
		print("Update : ",mesg)
		result = '>>> '
		if((mesg[0] not in ["put","get","upgrade","close"]) or ("put" in mesg[1:] or "get" in mesg[1:])):
			result = result + "Invalid Command !!!"
		else:
			while(i<len(mesg)):
				if(mesg[i] == 'put'):
					if(len(mesg)<3):
						print('Key or Value is Missing!!!')
						result='Key or Value is Missing!!!'
						i+=3
					else:					
						if(len(mesg)==4):
							client_pairs[ client_id ][ mesg[i+1] ] = mesg[i+2]+" "+mesg[i+3]
							i+=4
						else:
							client_pairs[ client_id ][ mesg[i+1] ] = mesg[i+2]
							i+=3
						result=result+"PUT Successfully !!!"
	
	
				elif mesg[i] == 'get':
					if(len(mesg)<2):
						print("Key or Value Missing!!!")
						result='Key or Value Missing!!!'
						i+=2
					else:
						key = mesg[i+1]
	
						if(client_id in managers):
	
							for client_name, pairs in client_pairs.items():
								if key in pairs:
									result = result+" "+pairs[key]
	
						else:
							if(key in client_pairs[client_id].keys()):
								result = result + client_pairs[client_id][key]
							else:
								result = result + "Key Not Found !!!"		
					
						i+=2
	
				elif mesg[i]=='upgrade':
					managers.add(client_id)
					result="Upgraded"	
					i+=1
	
				elif mesg[i]=='close':
					client[client_id].close()	
					result = 'Closed'
					i+=1
			
		
		client[client_id].send(result.encode())		
	
	
while count<int(num_clients) : 
	  
	# Establish connection with client. 
	client[count], addr[count] = s.accept()      
	print('Got connection from'+str(addr[count])) 

	# send a thank you message to the client.  
	client[count].send(('Thank you for connecting!!! ').encode()) 
	print(client[count].recv(1024).decode()) 
	# Close the connection with the client 

	thread = threading.Thread(target=receive, args=(count,))
	thread.start()

	count+=1 


