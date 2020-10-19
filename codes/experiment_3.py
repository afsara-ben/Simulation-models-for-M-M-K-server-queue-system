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

# Write more functions if required


# States and statistical counters
class States:
    def __init__(self):
        # States
        self.server_status = []
        self.total_delays = 0.0
        self.no_of_delay =0.0
        self.num_custs_delayed = 0.0


        self.time_arrival = []
        self.time_arrival.append([])

        #  intermediate variables
        self.arrival_event_count = 0
        self.departure_event_count = 0

        self.time_of_last_event = 0.0
        
        self.Total_time_served = 0.0
        self.Area_under_queue = 0.0
        self.num_in_q = 0
       

        # Statistics
        self.util = 0.0
        self.avgQdelay = 0.0
        self.avgQlength = 0.0
        self.served = 0.0


    def set_initial_server_status(self,sim):
        print("in set_initial_server_status, k = ", sim.params.k)
        for k in range(sim.params.k):
            sim.states.server_status.append(0)

    def return_free_server(self, sim):

        # print("ini return server")
        serverNo=0
        k = sim.params.k
        # self.see_server_status(sim)
        while serverNo < k :
            if self.server_status[serverNo] == IDLE:
                return serverNo
            serverNo+=1
        return -1 #means all servers are busy

    def see_server_status(self,sim):
        for i in range(sim.params.k):
            print(sim.states.server_status[i], ' - ', end = '')
        print('Queue length - ', len(sim.states.time_arrival[0]))


    def update(self, sim, event):
        # Complete this function

        
        print("\nin update of States")
        print()
        # print(' event ', event)
        
        time_since_last_event = event.eventTime - sim.states.time_of_last_event # time_since_last_event = duita event er modhekar time
                                                                                #event.eventTime = oi event er time
        
        sim.states.time_of_last_event = event.eventTime


        no_of_busy_servers = 0

        for i in range(sim.params.k):
            if(sim.states.server_status[i] == BUSY): 
                no_of_busy_servers +=1

        print("No of busy servers - ", no_of_busy_servers)
        mult = (no_of_busy_servers/sim.params.k)
        sim.states.Total_time_served +=  mult * time_since_last_event
        sim.states.Area_under_queue += sim.states.num_in_q * time_since_last_event
        print('Total_time_served - ', sim.states.Total_time_served)
        # print('Area_under_queue - ', sim.states.Area_under_queue)
        print('Number of customers served - ', sim.states.served)
       
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
        # print ('All arrival times  - ', sim.states.time_arrival)
        # DO NOT CHANGE THESE LINES
        print('MMk Results: lambda = %lf, mu = %lf, k = %d' % (sim.params.lambd, sim.params.mu, sim.params.k))
        print('MMk Total delay: %d' % (sim.states.total_delays))
        print('MMk Total customer served: %d' % (sim.states.served))
        print('MMk Average queue length: %lf' % (self.avgQlength))
        print('MMk Average customer delay in queue: %lf' % (self.avgQdelay))
        print('MMk Time-average server utility: %lf' % (self.util))


    def getResults(self, sim):
        return (self.avgQlength, self.avgQdelay, self.util)


def analytical(sim):
        
        lambd = sim.params.lambd
        mu = sim.params.mu


        analytical_L = lambd**2/(mu*(mu-lambd))
        analytical_D = lambd/(mu*(mu-lambd))
        analytical_U = lambd/mu

        print('\nAnalytical results')
        print('MMk Average queue length: %lf' % (analytical_L))
        print('MMk Average customer delay in queue: %lf' % (analytical_D))
        print('MMk Time-average server utility: %lf' % (analytical_U))



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
        print (" in StartEvent's process")

        
        sim.states.see_server_status(sim)

        sim.scheduleEvent(ArrivalEvent(random.expovariate(sim.params.lambd), sim))
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

        # put TOA of i+1 th customer in array
        # time_arrival = [num_in_q - 1] as it is 0 index based
        # self.sim.states.time_arrival [ sim.states.num_in_q-1 ] = sim.states.timeOfNextArrival

        
        # Schedule next (n+1) arrival 
        sim.scheduleEvent(ArrivalEvent(timeOfNextArrival,sim))

        

        # Check to see whether server is busy
        server = sim.states.return_free_server(sim) #server = the server which is free
        # print('server returned was ', server)
        if (server == -1): #means all servers are busy
            
            #insert in q
            print("\n~~~~~~~~~~~~~~~~~~~~~~~ ALL servers are now busy ~~~~~~~~~~~~~~~~~~~~`")
           
            self.sim.states.num_in_q += 1 
            print("inserted in queue")
            
            # There is still room in the queue, so store the time of arrival of the arriving customer at the (new) end of time_arrival. */
            # self.sim.states.time_arrival[sim.states.num_in_q-1] = sim.simclock;
            # self.sim.states.time_arrival[] = sim.simclock
            #put next arrival time in array
            self.sim.states.time_arrival[0].append(sim.simclock)
            sim.states.see_server_status(sim)

        else:

            sim.states.see_server_status(sim)
            # Server is idle, so arriving customer has a delay of zero. */
            print("server[",server,"] status : ", 'IDLE' if self.sim.states.server_status[server] == 0 else 'BUSY')
            
            # delay = 0.0
            # sim.states.total_delays += delay

            # Increment the number of customers delayed, and make server busy. */
            # sim.states.num_custs_delayed +=1
            sim.states.served +=1
            print('Customer is now being served')
            sim.states.server_status[server] = BUSY

            
            # Schedule a departure (service completion)
            print('service completed\n')
            sim.states.departure_event_count += 1 
            departure_time = sim.simclock + random.expovariate(sim.params.mu)
            sim.scheduleEvent(DepartureEvent(departure_time, sim, server))
           


class DepartureEvent(Event):
    def __init__(self,eventTime, sim, curr_server):
        print("Initializing DepartureEvent")
        self.eventType = 'DEPARTURE'
        self.eventTime = eventTime
        self.sim = sim
        self.curr_server = curr_server
        


    def process(self, sim):
        print("in process() of DepartureEvent")

        sim.states.see_server_status(sim)
        
        # print(' Number in q - ', sim.states.num_in_q)
        #  Check to see whether the queue is empty
        if(sim.states.num_in_q == 0):
            print('Q is empty, so make server idle')
            self.sim.states.server_status[self.curr_server] = IDLE


        else:
            sim.states.num_in_q -=1

            # delay = sim.simclock - sim.states.time_arrival[num_in_q-1]
            
            # print('~~~~~~~~~  customer ', sim.states.served, ' was just served ~~~~~~~~~~~~~~')
            #  service done for customer at head, move on to next one
            sim.states.served += 1

            #calculate delay
            sim.states.no_of_delay +=1
            delay = sim.simclock - sim.states.time_arrival[0][0] #curr time - time of arrival of this customer who is now being served
            sim.states.total_delays += delay

            # Increment the number of customers delayed, and schedule departure. 
            # self.sim.states.num_custs_delayed +=1;

            time_departure_next_event = sim.simclock + random.expovariate(sim.params.mu)
            sim.states.departure_event_count +=1
            sim.scheduleEvent(DepartureEvent(time_departure_next_event, sim, self.curr_server))

            #move next person to head of queue
            sim.states.time_arrival[0] = sim.states.time_arrival[0][1:]





class Simulator:
    def __init__(self, seed):
        print(" in init of Simulator")
        self.eventQ = []
        self.simclock = 0
        self.seed = seed
        self.params = None
        self.states = None

    def initialize(self):
        print("Initializing Simulator")
        self.simclock = 0
        self.states.set_initial_server_status(self)  #-- changed here

        self.scheduleEvent(StartEvent(0, self))

    def configure(self, params, states):
        print("in configure of Simulator")
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



def experiment3():
    # Similar to experiment2 but for different values of k; 1, 2, 3, 4
    # Generate the same plots
    # Fix lambd = (5.0/60), mu = (8.0/60) and change value of k


    print("starting experiment3")
    seed = 101
    k = 4
    avglength = []
    avgdelay = []
    util = []

    k_servers = [1,2,3,4]
    
    for k in k_servers:    
        sim = Simulator(seed)
        sim.configure(Params(5.0 / 60, 8.0/60, k), States())
        sim.run()
        sim.printResults()

        len_,delay,util_ =  sim.getResults()
        avglength.append(len_)
        avgdelay.append(delay)
        util.append(util_)

    plt.figure(1)
    plt.subplot(311)
    plt.plot(k_servers, avglength)
    plt.title('Experiment 3')
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
    
    experiment3()
    

if __name__ == "__main__":
    main()
