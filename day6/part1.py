#!/usr/local/bin/python3

f = open('input.txt', 'r')
signal = f.read().strip()
f.close()
for i in range(4, len(signal)):
  if(len(set(signal[i-4:i])) == 4):
    print(i)
    break

