"""
Check the buffer size for UDP  
"""
#pragma repy restrictions.udpbuffertest

myip = "127.0.0.1"
localport = 12345
targetport = 12346
timeout = 1.0
mycontext['maxlag'] = 0
#fp = openfile("test1.log", True)
#mycontext['count'] = 0

def foreversend():
  while True:
    sendmessage("127.0.0.1", 12346, str(getruntime()) + ' ' + 'X'*92, "127.0.0.1", 12345)
    sleep(0.01)
    
def handleconnection(sock_s):
  while True:
    (ip, port, message) = sock_s.getmessage()
    lag = getruntime() - float(message.split()[0])
#    fp.writeat(str(lag) + '              ', mycontext['count'])
#    mycontext['count'] = mycontext['count'] + 15
#    log(lag)
    if mycontext['maxlag'] < lag:
      mycontext['maxlag'] = lag
    sleep(0.01)

def time_set():
  sleep(5)
  if mycontext['maxlag'] > 2:
    log("TCP packets has lagged too long in the buffer: ", mycontext['maxlag'])
  if mycontext['maxlag'] == 0:
    log("0 lag detected")
  exitall()

createthread(time_set)
sock_s = listenformessage(myip, targetport)

createthread(foreversend)
sleep(0.1)
handleconnection(sock_s) 
