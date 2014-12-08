"""
Check the buffer size for TCP  
"""
#pragma repy restrictions.tcpbuffertest

myip = "127.0.0.1"
localport = 12345
targetport = 12346
timeout = 1.0
mycontext['maxlag'] = 0
connfd = 0
mycontext['count'] = 0
mycontext['sum'] = 0

def foreversend():
  sockfd = openconnection("127.0.0.1", 12346, "127.0.0.1", 12345, 2.0)
  while True:
    amount = sockfd.send("%9f "%getruntime())
    sleep(0.01)
    
def handleconnection():
  while True:
    sendtime = float(connfd.recv(10).split()[0])
    lag = getruntime() - sendtime
    mycontext['count'] += 1
    mycontext['sum'] += lag
#    log(lag)
    if mycontext['maxlag'] < lag:
      mycontext['maxlag'] = lag
    sleep(0.01)

def time_set():
  sleep(10)
  if mycontext['maxlag'] > 4:
    log("TCP packets has lagged too long in the buffer: ", mycontext['maxlag'])
  if mycontext['maxlag'] == 0:
    log("0 lag detected")
  log("Average lag time: ", mycontext['sum']/mycontext['count'])
  exitall()

createthread(time_set)
sock_s = listenforconnection(myip, targetport)

createthread(foreversend)
#waiting for the connection
sleep(0.1)
(ip, port, connfd) = sock_s.getconnection()
handleconnection() 
