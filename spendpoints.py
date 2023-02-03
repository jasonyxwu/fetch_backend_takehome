import csv
import sys
import heapq
import logging

class Transaction(object):
  def __init__(self, payer: str, points: int, timestamp: str):
    self.payer = payer
    self.points = points
    self.timestamp = timestamp

  def __str__(self) -> str:
    return "payer: {0}, points: {1}, timestamp: {2}".format(self.payer, self.points, self.timestamp)
  
  def __lt__(self, other):
    # defined for comparision in the heap
    return self.timestamp < other.timestamp


class Account(object):
  def __init__(self):
    self._history_heap = []   # all transactions, the oldest stay on top
    self._total_points = 0    # use to determine whether spending given points is possible
    self._payer_dict = {}     # for output

  def read_data(self):
    with open("./transaction.csv") as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=",")
      for index, row in enumerate(csv_reader):
        if index != 0: 
          assert len(row) == 3
          payer, points, time = row
          points = int(points)

          self._total_points += points

          if payer not in self._payer_dict:
            self._payer_dict[payer] = points
          else:
            self._payer_dict[payer] += points
          
          new_transaction = Transaction(payer, points, time)
          self._history_heap.append(new_transaction)
    # done read, make heap
    heapq.heapify(self._history_heap)
  
  def print_by_payers(self):
    print(str(self._payer_dict))

  def print_history(self):
    print([str(i) for i in self._history_heap])

  def spend_points(self, points: int):
    if not isinstance(points, int) or points < 0: 
      print("invalid input: {0}".format(points))
      return None
    if points > self._total_points: # check if points are enough
      print("points not enough!")
      return None

    self._total_points -= points
    while(points > 0):
      top = self._history_heap[0]
      if top.points > points:
        self._payer_dict[top.payer] -= points
        top.points -= points
        points = 0
      else:
        self._payer_dict[top.payer] -= top.points
        points -= top.points
        heapq.heappop(self._history_heap)
    self.print_by_payers()
  


if __name__ == '__main__':
  assert len(sys.argv) == 2
  account = Account()
  account.read_data()
  account.spend_points(int(sys.argv[1]))
