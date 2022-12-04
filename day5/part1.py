counter = 0
for line in open('input.txt', 'r').readlines():
  l = line.strip()
  counter += 1

print(counter)
