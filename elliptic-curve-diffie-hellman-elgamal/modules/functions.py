#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 2023

@author: iluzioDev

This document contains the functions used in the elliptic curve Diffie-Hellman and ElGamal modes.
"""
def nearest_power_of_2(n):
  """
  Calculate the nearest power of 2 greater than n.

  Args:
      n (int): Number.

  Returns:
      int: Nearest power of 2 greater than n.
  """
  power = 1
  while power < n:
    power *= 2
  return power

def euclid_extended(a, b):
  """
  Euclid's extended algorithm.

  Args:
    a (int): First number.
    b (int): Second number.

  Returns:
    tuple: Tuple containing the GCD, the x coefficient and the y coefficient.
  """
  if a == 0:
    return (b, 0, 1)
  else:
    g, y, x = euclid_extended(b % a, a)
    s = 1 if a > 0 else -1
    t = 1 if b > 0 else -1
    return (g, x - ((b // a) * y) * s, y * t)

def generate_points(curve, p):
  """
  Generate all the points on the elliptic curve.

  Args:
      curve (tuple): Elliptic curve, only a and b values are needed.
      p (int): Prime number.

  Returns:
      list: List of all the points on the elliptic curve.
  """
  if not isinstance(curve, tuple) or not isinstance(p, int):
    return 'Invalid arguments!'
  
  points = []
  for x in range(p):
    y2 = (x ** 3 + curve[0] * x + curve[1]) % p
    for y in range(p):
      if y ** 2 % p == y2:
        points.append((x, y))
  return points

def add_points(point1, point2, curve, p):
  """
  Add two points on the elliptic curve
  
  Args:
    point1 (tuple): First point.
    point2 (tuple): Second point.
    curve (tuple): Elliptic curve, only a and b values are needed.
    p (int): Prime number.
    
  Returns:
    tuple: The result of the addition.
  """
  if not isinstance(point1, tuple) or not isinstance(point2, tuple) or not isinstance(curve, tuple) or not isinstance(p, int):
    return 'Invalid arguments!'
  
  x1, y1 = point1
  x2, y2 = point2
  a, *_ = curve
  
  if point1 == (0, 0):
    return point2
  if point2 == (0, 0):
    return point1
  if x1 == x2 and y1 == -y2:
    return (0, 0)
  
  if point1 == point2:
    lamb = ((3 * x1 ** 2 + a) * euclid_extended(2 * y1, p)[1]) % p
  else:
    lamb = ((y2 - y1) * euclid_extended(x2 - x1, p)[1]) % p
    
  x3 = (lamb ** 2 - x1 - x2) % p
  y3 = (lamb * (x1 - x3) - y1) % p
  
  return  x3, y3

def multiply_point_by_scalar(point, scalar, curve, p):
  """
  Multiply a point on the elliptic curve by a scalar.

  Args:
      point (tuple): Point on the elliptic curve.
      scalar (int): Scalar.
      curve (tuple): Elliptic curve, only a and b values are needed.
      p (int): Prime number.

  Returns:
      tuple: The result of the multiplication.
  """
  if scalar == 0 or point == (0, 0):
    return (0, 0)

  result = (0, 0)
  current = point

  while scalar > 0:
    if scalar & 1:
      result = add_points(result, current, curve, p)
    current = add_points(current, current, curve, p)
    scalar >>= 1

  return result

def encode(message, curve, p):
  """
  Encode a message using the elliptic curve Diffie-Hellman and ElGamal modes.

  Args:
    message (str): Message to encode.
    curve (tuple): Elliptic curve, only a and b values are needed.
    p (int): Prime number.

  Returns:
    tuple: Point on the elliptic curve.
  """
  if not isinstance(message, str) or not isinstance(curve, tuple) or not isinstance(p, int):
    return 'Invalid arguments!'
  if not message.isnumeric():
    return 'Invalid message!'
  m = int(message)
  M = nearest_power_of_2(m)
  h = p // M
  
  points = generate_points(curve, p)
  
  j = 0
  while True:
    x = (m * h + j) % p
    if x in [point[0] for point in points]:
      y = [point[1] for point in points if point[0] == x][0]
      break
  return (x, y), M, h
  

def encrypt(message, curve, p, G, dA, dB):
  """
  Encode a message using the elliptic curve Diffie-Hellman and ElGamal modes.

  Args:
      message (str): Message to encrypt.
      curve (tuple): Elliptic curve, only a and b values are needed.
      p (int): Prime number.
      G (tuple): Generator point.
      dA (int): Private key of Alice.
      dB (int): Private key of Bob.

  Returns:
      tuple: Tuple containing the encrypted message and the public key of Alice.
  """
  if not isinstance(message, str) or not isinstance(curve, tuple) or not isinstance(p, int):
    return 'Invalid arguments!'
 
  Qm = encode(message, curve, p)[0]
  dAG = multiply_point_by_scalar(G, dA, curve, p)
  dBG = multiply_point_by_scalar(G, dB, curve, p)
  
  return (add_points(Qm, multiply_point_by_scalar(dBG, dA, curve, p), curve, p), dAG)
