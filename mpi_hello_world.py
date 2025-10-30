from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print(f"The mpi comm size is {size}")


# Split up a task — for example, summing numbers 0..9999
n = 10000
chunk = n // size
start = rank * chunk
end = n if rank == size - 1 else start + chunk

local_sum = sum(range(start, end))
print(f"Rank {rank:02d}: handling range [{start}, {end}) -> partial sum = {local_sum}")

# Gather all partial results to rank 0
total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

if rank == 0:
    print(f"\n✅ Total sum = {total_sum}")