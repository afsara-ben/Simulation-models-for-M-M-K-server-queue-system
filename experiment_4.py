"""
The task is to simulate an M/M/k system with a single queue.
Complete the skeleton code and produce results for three experiments.
The study is mainly to show various results of a queue against its ro parameter.
ro is defined as the ratio of arrival rate vs service rate.
For the sake of comparison, while plotting results from simulation, also produce the analytical results.
"""

import heapq
import random
import matplotlib.pyplot as plt

Q_LIMIT = 10
IDLE = 0
BUSY = 1



# Parameters
class Params:
    def __init__(self, lambd, mu, k):
        self.lambd = lambd  # interarrival rate
        self.mu = mu  # service rate
        self.k = k
    # Note lambd and mu are not mean value, they are rates i.e. (1/mean)


# States and statistical counters
class States:
    def __init__(self):
        # States
        self.server_status = [] #list state of k servers
        self.total_delays = 0.0
        self.no_of_delay =0.0
        self.num_custs_delayed = 0.0
        self.queue = [] #stores the arrival times
        # self.queue.append([]) #2d array row = server #, queue[i][] = customers in server row[i] 


        #  intermediate variables
        self.arrival_event_count = 0
        self.departure_event_count = 0
        self.time_of_last_event = 0.0
        self.Total_time_served = 0.0
        self.Area_under_queue = 0.0
       
        # Statistics
        self.util = 0.0
        self.avgQdelay = 0.0
        self.avgQlength = 0.0
        self.served = 0.0


    def set_server_and_queue_status(self,sim):
        print("Initializing ", sim.params.k, " servers and ", sim.params.k, " queues")
        for k in range(sim.params.k):
            sim.states.server_status.append(IDLE) #server[i] = IDLE initially
            sim.states.queue.append([]) #list of list

        self.see_server_status(sim)





    def return_free_server(self, sim):

        
        serverNo=0
        k = sim.params.k
        # self.see_server_status(sim)
        while serverNo < k :
            if self.server_status[serverNo] == IDLE:
                print('Server ', serverNo, ' is free')
                return serverNo
            serverNo+=1

        # print ('All servers are busy')
        return -1 #means all servers are busy

    def see_server_status(self,sim):
        for i in range(sim.params.k):
            print(sim.states.server_status[i], ' - ', len(sim.states.queue[i]))

    def get_shortest_Q(self,sim):
        lst = []
        for k in range(sim.params.k):
            lst.append(len(sim.states.queue[k]))
        min_ = min(lst)
        
        return lst.index(min_)

    def print_queue_status(self, sim):
        for i in range(sim.params.k):
            # print( 'queue ',i, ' - ', sim.states.queue_status[i])
            print( 'queue ',i, ' - ', len(sim.states.queue[i]))

    def count_busy_servers(self,sim):
        no_of_busy_servers=0
        
        for i in range(sim.params.k):
            if(sim.states.server_status[i] == BUSY): 
                no_of_busy_servers +=1

        print("No of busy servers - ", no_of_busy_servers)
        return no_of_busy_servers

    def get_avg_len_of_queues(self,sim):
        k = sim.params.k
        len_ = 0

        for i in range(k):
            len_ += len(sim.states.queue[i])

        return len_/k

    def update(self, sim, event):
        # Complete this function

        
        # print("\nin update() of States\n")
        print('\nUpdated stats\n')
        
        
        time_since_last_event = event.eventTime - sim.states.time_of_last_event # time_since_last_event = duita event er modhekar time
                                                                                #event.eventTime = oi event er time
        
        sim.states.time_of_last_event = event.eventTime


        no_of_busy_servers = self.count_busy_servers(sim)

        
        mult = (no_of_busy_servers/sim.params.k)
        sim.states.Total_time_served +=  mult * time_since_last_event

        avg_lenQ = self.get_avg_len_of_queues(sim)
        sim.states.Area_under_queue += avg_lenQ * time_since_last_event

        print('Total_time_served - ', sim.states.Total_time_served)
        print('Area_under_queue - ', sim.states.Area_under_queue)
        print('Total customers served - ', sim.states.served)
       
        print()
       
        # event.process(sim) -- ei line er jonne double event call hochilo
        


    def finish(self, sim):
        

        self.util = self.Total_time_served/sim.simclock
        self.avgQlength= self.Area_under_queue/sim.simclock
        # self.avgQdelay = self.total_delays/sim.states.num_custs_delayed
        self.avgQdelay = self.total_delays/sim.states.served

       

    def printResults(self, sim):
        print()


        print(' arrival_event_count- ', sim.states.arrival_event_count)
        print( ' departure_event_count- ', sim.states.departure_event_count)
        # print ('All arrival times  - ', sim.states.queue)
        # DO NOT CHANGE THESE LINES
        print('MMk Results: lambda = %lf, mu = %lf, k = %d' % (sim.params.lambd, sim.params.mu, sim.params.k))
        print('MMk Total delay: %d' % (sim.states.total_delays))
        print('MMk Total customer served: %d' % (sim.states.served))
        print('MMk Average queue length: %lf' % (self.avgQlength))
        print('MMk Average customer delay in queue: %lf' % (self.avgQdelay))
        print('MMk Time-average server utility: %lf' % (self.util))


    def getResults(self, sim):
        return (self.avgQlength, self.avgQdelay, self.util)



class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.eventTime = None

    def process(self, sim):
        raise Exception('Unimplemented process method for the event!')

    def __repr__(self):
        return self.eventType


    #this class decorater needed because of this comparison
    def __lt__(self, other):
        return self.eventTime < other.eventTime


class StartEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'START'
        self.sim = sim

    def process(self, sim):
        print ("in StartEvent's process()")

        
        # sim.states.see_server_status(sim)

        sim.scheduleEvent(ArrivalEvent(random.expovariate(sim.params.lambd), sim)) #initially start at 0th server
        sim.scheduleEvent(ExitEvent(int(100000), sim))
        

class ExitEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'EXIT'
        self.sim = sim

    def process(self, sim):
        None

class ArrivalEvent(Event):
    def __init__(self,eventTime, sim):
        print("Initializing ArrivalEvent")
        self.eventType = 'ARRIVAL'
        self.eventTime = eventTime
        self.sim = sim
    

        

    def process(self, sim):
        print("in process() of ArrivalEvent")
        
        
        #increase arrival count 
        sim.states.arrival_event_count +=1

        timeOfNextArrival = sim.simclock + random.expovariate(sim.params.lambd)
        # print(' timeOfNextArrival ', timeOfNextArrival)
        
        # Schedule next (n+1) arrival 
        sim.scheduleEvent(ArrivalEvent(timeOfNextArrival,sim)) 
            

        # process n_th customer
        # Check to see whether server is busy
        server = sim.states.return_free_server(sim) #server = the server which is free
    
        if (server == -1): #means all servers are busy
            
            
            print("\n~~~~~~~~~~~~~~~~~~~~~~~ ALL servers are now busy ~~~~~~~~~~~~~~~~~~~~`")
           
            # move customer to leftmost shortest queue
            # find shortest queue
            shortestQ = sim.states.get_shortest_Q(sim)
            print('After inserting customer at server ', shortestQ, 'having shortest q length ', len(sim.states.queue[shortestQ]))

            
           
           

            # self.sim.states.queue_status[shortestQ] += 1 
            
            
            #put arrival time of this customer in its server's queue
            self.sim.states.queue[shortestQ].append(sim.simclock)
            
            sim.states.see_server_status(sim)




        else:

            sim.states.see_server_status(sim)
            # this server is idle, so arriving customer has a delay of zero. */
            print("server[",server,"] status : ", 'IDLE' if self.sim.states.server_status[server] == 0 else 'BUSY')
            # delay = 0.0
            # sim.states.total_delays += delay

            # Increment the number of customers delayed, and make server busy. */
            # sim.states.num_custs_delayed +=1
            sim.states.served +=1
            print('Customer now being served at server ', server)
            sim.states.server_status[server] = BUSY

            
            # Schedule a departure (service completion)
            print('service completed\n')
            sim.states.departure_event_count += 1 
            departure_time = sim.simclock + random.expovariate(sim.params.mu)
            sim.scheduleEvent(DepartureEvent(departure_time, sim, curr_server=server))

           


class DepartureEvent(Event):
    def __init__(self,eventTime, sim, curr_server):
        print("Initializing DepartureEvent")
        self.eventType = 'DEPARTURE'
        self.eventTime = eventTime
        self.sim = sim
        self.curr_server = curr_server
        


    def process(self, sim):
        print("in process() of DepartureEvent")
        # sim.states.print_queue_status(sim)
        sim.states.see_server_status(sim)

        
        #  Check to see whether the queue of current server is empty
        # if empty then make the server idle
        # if(sim.states.num_in_q == 0):
        # if(sim.states.queue_status[self.curr_server] == 0):
        if(len(sim.states.queue[self.curr_server]) == 0):
            print('Q is empty, so make server', self.curr_server ,'idle')
            self.sim.states.server_status[self.curr_server] = IDLE


        else:
            # sim.states.num_in_q -=1
            # sim.states.queue_status[self.curr_server] -= 1

            sim.states.served += 1


            #calculate delay
            sim.states.no_of_delay +=1
            # delay = sim.simclock - sim.states.queue[0][0] #curr time - time of arrival of this customer who is now being served
            delay = sim.simclock - sim.states.queue[self.curr_server][0]
            sim.states.total_delays += delay

            # Increment the number of customers delayed, and schedule departure. 
            # self.sim.states.num_custs_delayed +=1;

            time_departure_next_event = sim.simclock + random.expovariate(sim.params.mu)
            sim.states.departure_event_count +=1
            sim.scheduleEvent(DepartureEvent(time_departure_next_event, sim, self.curr_server))

            #move next person to head of queue
            sim.states.queue[self.curr_server] = sim.states.queue[self.curr_server][1:]


            print('\nPerforming SWITCHING operation\n')
            # DO THE SWITCHING part
            # When a customer leaves a server, the next person standing in corresponding
            # server’s queue will be served. Now assume after departure length of this server’s
            # queue is L. Also assume length of the left and right queues are LF and
            # LR respectively.If either (LF – L) or (LR – L)>= 2 then one or more customers from
            # the tail of the longer queue will join the current server’s queue. If one of them
            # finds the server idle, s/he will be served immediately

            # L = sim.states.queue_status[self.curr_server]


            L = len(sim.states.queue[self.curr_server])
            
            print('length of current server', self.curr_server  ,' = ', L)
            LF = L #initially dhorlam if L = server 0
            LR = L #initially dhorlam if L = server 3
            
            if(self.curr_server != 0) :
                LF = len(sim.states.queue[self.curr_server - 1])
            if(self.curr_server != sim.params.k-1):
                LR = len(sim.states.queue[self.curr_server + 1])

            if LF > LR:
                longerQ = self.curr_server - 1 #len of left queue is longer
            else:
                longerQ = self.curr_server + 1 #len of right queue is longer

            #schedule an arrival event? - NO
            if((    (LF - L) or (LR-L)  ) >= 2  ):

                # increase n decrease count
                # sim.states.queue_status[longerQ] -= 1
                # sim.states.queue_status[self.curr_server] += 1

                # append last person from longer queue to end of current queue
                sim.states.queue[self.curr_server].append(sim.states.queue[longerQ][-1]) 

                # remove that person from longer queue
                sim.states.queue[longerQ]=sim.states.queue[longerQ][:-1]

                    


class Simulator:
    def __init__(self, seed):
        print("in init of Simulator")
        self.eventQ = []
        self.simclock = 0
        self.seed = seed
        self.params = None
        self.states = None

    def initialize(self):
        print("Initializing Simulator")
        self.simclock = 0
        self.states.set_server_and_queue_status(self)  #-- changed here

        self.scheduleEvent(StartEvent(0, self))

    def configure(self, params, states):
        print("Configuring Simulator")
        self.params = params
        self.states = states

    def now(self):
        print("in now of Simulator")
        return self.simclock

    def scheduleEvent(self, event):
        # print("in scheduleEvent of Simulator")
        heapq.heappush(self.eventQ, (event.eventTime, event))

    def run(self):
        print("Running Simulator")
        random.seed(self.seed)
        self.initialize()

        

        while len(self.eventQ) > 0:
            # print('len of eventQ ' ,len(self.eventQ))
            time, event = heapq.heappop(self.eventQ)
            # print('popping ', event, ' at ', time)

            if event.eventType == 'EXIT':
                print ("\nEXITING")
                break

            if self.states != None:
                self.states.update(self, event) #sim instance er states attr contains a States() instance which calls the update of States class

            print('\n-------------------------------------------------------------------------------')
            print('              At %lf' % event.eventTime, 'Event', event, 'k = ', self.params.k,'\n')
            
            self.simclock = event.eventTime
            event.process(self)

        self.states.finish(self)

    def printResults(self):
        self.states.printResults(self)

    def getResults(self):
        print("in getResults of Simulator")
        return self.states.getResults(self)


def experiment4():

    print("starting experiment4")
    seed = 101
    k=2
    sim = Simulator(seed)
    sim.configure(Params(5.0 / 60, 8.0 / 60, k), States())
    sim.run()
    sim.printResults()

def experiment4_with_graph():


    print("starting experiment4")
    seed = 101
    avglength = []
    avgdelay = []
    util = []

    k_servers = [1,2,3,4]
    
    
    for k in k_servers:    
        sim = Simulator(seed)
        sim.configure(Params(5.0 / 60, 8.0 / 60, k), States())
        sim.run()
        sim.printResults()

        len_,delay,util_ =  sim.getResults()
        avglength.append(len_)
        avgdelay.append(delay)
        util.append(util_)


    plt.figure(1)

    plt.subplot(311)
    plt.plot(k_servers, avglength)
    plt.title('Simulating a MMK server with K queues')
    plt.xlabel('Number of servers (k)')
    plt.ylabel('Avg Q length')

    plt.subplot(312)
    plt.plot(k_servers, avgdelay)
    plt.xlabel('Number of servers (k)')
    plt.ylabel('Avg Q delay (sec)')

    plt.subplot(313)
    plt.plot(k_servers, util)
    plt.xlabel('Number of servers (k)')
    plt.ylabel('Util')

    plt.show()

    


def main():
    
    # experiment4()
    experiment4_with_graph();
    

if __name__ == "__main__":
    main()
