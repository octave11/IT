import socket                
  
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 12340               
  
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
  
# receive data from the server 
print(s.recv(1024).decode())
s.send(('connected').encode()) 
# close the connection 


while True:

	result=''
	input_str = input('Enter query: ')
	s.send(input_str.encode()) 
	result = s.recv(1024).decode()
	#print('result'+' out')

	if(result == 'close'):
		print('closing client connection')
		s.close()
		exit()

	else:
		#print('in')
		print(result)	

