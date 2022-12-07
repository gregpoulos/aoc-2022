#!/usr/local/bin/python3

f = open('input.txt', 'r')
signal = f.read().strip()
f.close()
for i in range(14, len(signal)):
  if(len(set(signal[i-14:i])) == 14):
    print(i)
    break

