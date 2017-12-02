import multiprocessing as mp

output = mp.Queue()

def scrape():
    output.put("hello world")

processes = [mp.Process(target=scrape, args=()) for x in range(2)]

for p in processes:
    p.start()

for p in processes:
    p.join()

results = [output.get() for p in processes]

print(results)
