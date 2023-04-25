#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 2023

@author: iluzioDev

This script implements the elliptic curve Diffie-Hellman and ElGamal modes.
"""
import re
from modules.constants import ROW
import modules.functions as functions

def check_prime(number):
  """
  Check if a number is prime
  
  Args:
    n (int): Number to check.
    
  Returns:
    bool: True if the number is prime, False otherwise.
  """ 
  return all(number % i for i in range(2, number))

def main():
  """
  Main function
  """
  while True:
    print(ROW)
    print('■              WELCOME TO THE ECDH/ECEG MODE TOOL!                   ■')
    print(ROW)
    print('What do you want to do?')
    print('[1] Start the ECDH/ECEG mode.')
    print('[0] Exit.')
    print(ROW)
    option = input('Option  ->  ')
    print(ROW)

    if int(option) not in range(2):
      print('Invalid option!')

    if option == '0':
      print('See you soon!')
      print(ROW)
      break
      
    if option == '1':
      prime_number = input('Enter the prime number: ')
      print(ROW)
      if not check_prime(int(prime_number)):
        print('The number is not prime!')
        continue
      elliptic_curve = input('Enter the elliptic curve: ')
      print(ROW)
      if re.compile(r'y^2 = x^3 \+ (\d*)x \+ (\d*)').match(elliptic_curve):
        print('Invalid elliptic curve!')
        continue
      elliptic_curve = elliptic_curve.split(' ')
      if elliptic_curve[4] == 'x':
        a = 1
      else:
        a = int(elliptic_curve[4].replace('x', ''))
      b = int(elliptic_curve[6])
      elliptic_curve = (a, b)
      print('The points on the elliptic curve in Z' + str(prime_number) + ' are: ')
      print(ROW)
      points = functions.generate_points(elliptic_curve, int(prime_number))
      for i in range(0, len(points), 5):
        print(points[i:i+5])
      print(ROW)
      
      g_x = input('Enter the x coordinate of the base point: ')
      print(ROW)
      g_y = input('Enter the y coordinate of the base point: ')
      print(ROW)
      G_point = (int(g_x), int(g_y))
      if G_point not in points:
        print('The point is not on the elliptic curve!')
        continue
      print('The base point is:', G_point)
      print(ROW)
      
      dA = input('Enter the private key of Alice: ')
      print(ROW)
      if not dA.isnumeric():
        print('Invalid private key!')
        continue
      dB = input('Enter the private key of Bob: ')
      if not dB.isnumeric():
        print('Invalid private key!')
        continue
      print(ROW)
      dAG = functions.multiply_point_by_scalar(G_point, int(dA), elliptic_curve, int(prime_number))
      print('The public key of Alice is ' + dA + ' * ' + str(G_point) + ' = ' + str(dAG))
      print(ROW)
      dBG = functions.multiply_point_by_scalar(G_point, int(dB), elliptic_curve, int(prime_number))
      print('The public key of Bob is ' + dB + ' * ' + str(G_point) + ' = ' + str(dBG))
      print(ROW)
      
      shared_key_A = functions.multiply_point_by_scalar(dBG, int(dA), elliptic_curve, int(prime_number))
      shared_key_B = functions.multiply_point_by_scalar(dAG, int(dB), elliptic_curve, int(prime_number))
      if shared_key_A != shared_key_B:
        print('The shared keys are not equal!')
      print('The shared key is ' + dB + ' * ' + str(dAG) + ' = ' + str(shared_key_A))
      print(ROW)
      
      message = input('Enter the message: ')
      print(ROW)
      encoded_message, M, h = functions.encode(message, elliptic_curve, int(prime_number))
      print('M:', M)
      print(ROW)
      print('h:', h)
      print(ROW)
      print('Original message encoded to a point on the elliptic curve: ' + str(encoded_message))
      print(ROW)
      encripted_message = functions.encrypt(message, elliptic_curve, int(prime_number), G_point, int(dA), int(dB))
      print('Encripted message from Alice to Bob: ' + str(encripted_message))
      
  return

if __name__ == '__main__':
  main()
