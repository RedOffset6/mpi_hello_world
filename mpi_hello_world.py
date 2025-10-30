from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print(f"The mpi comm size is {size}")

# READ THE FOLLOWING FOR A BASIC EXPLINATION

# EVEYTHING IN THIS FILE WILL BE RAN SEPERATLY ON EACH AVAILABLE CPU (72 on one isambard ai node)

# comm.Get_size() will be equal to the total number of tasks (72)

# comm.Get_rank will be the id assigned to each task

# on the first cpu the code will execute with rank = 0
# then on the secodn cpu rank will equal 1 and so on

# this means if you have 250 tasks you can split the tasks into chunk = 250 // size
# if 10 cpus were available this would divide the tasks into 25 chunks

# you can then iterate where each cpu runs on tasks from (rank - 1)*chunk to rank*chunk


# so on the 9th cpu where rank == 8 the following would happen

# for i in range ((rank - 1)*chunks, rank*chunks):
#     print (i)

# the code will iterate over tasks from i values of (8-1)*25 to 8*25

# e.g iterate over values of 175 to 200

# this effectivly divides up tasks over 10 cpus on isambard the size value will always be for 72 cpus

# in my usage this could easily be used to parallelise computation over 250 parquet files numbered from 1 to 250



# Split up a task — for example, summing numbers 0..9999
n = 10000
chunk = n // size
start = rank * chunk
end = n if rank == size - 1 else start + chunk

# the following does a sum and a reduction this is a type of communication between threads where rank 0 is the master and teh calculation results are sent to thihs and combined
this kind of think is not nessecary in most of our workslows

local_sum = sum(range(start, end))
print(f"Rank {rank:02d}: handling range [{start}, {end}) -> partial sum = {local_sum}")

# Gather all partial results to rank 0
total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

if rank == 0:
    print(f"\nTotal sum = {total_sum}")