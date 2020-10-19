# simulation-model-for-M-M-K-server-queue-system

Lambda (λ) = Interarrival rate

Mu (μ) = Service rate

Ro (ρ) = λ / μ

Average Queue Length (L)

Average Delay in Queue (D)

Server Utilization Factor (U)

Number of servers (k)

## Experiment 1
This is a basic M/M/1 implementation

## Experiment 2
It is a variant of M/M/1 system. The following figures are drawn using experimental
results.
1. L vs ρ
2. D vs ρ
3. U vs ρ

## Experiment 3 - M/M/K implementation
Here there are K servers but only 1 queue.

## Experiment 4 - M/M/K implementation
There are K servers and K queues in this experiment i.e each server has it own queue.There will be some changes in the arrival and departure subroutine.

### Arrival
Upon arrival if a customer finds all the servers busy, he will move in the leftmost shortest queue. Everything else is same as single queue system.

### Departure
When a customer leaves a server, the next person standing in corresponding server’s queue will be served. Now assume after departure length of this server’s
queue is L. Also assume length of the left and right queues are LF and LR respectively.If either (LF – L) or (LR – L)>= 2 then one or more customers from the tail of the longer queue will join the current server’s queue. If one of them finds the server idle, he/she will be served immediately.
