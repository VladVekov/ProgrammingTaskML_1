"""
name: Investments
author: vladvekov
"""
import csv
import os
from datetime import datetime


class pair(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second


class Date_Time_Price(object):
    def __init__(self, Date, Time, Price):
        self.Date = Date
        self.Time = Time
        self.Price = Price


def read_mode():
    DATA = []
    with open("/home/vlad/Документы/NewTable.csv", "r", encoding='utf-8') as ReadingFile:
        CSVreader = csv.reader(ReadingFile)
        for index, line in enumerate(CSVreader):
            if index == 1:
                ParseLine = list(map(float, line))
                CurrentStablePrice = ParseLine[3]
                TempData = Date_Time_Price(ParseLine[1], ParseLine[2], CurrentStablePrice)
                DATA.append(TempData)
            elif index > 1:
                ParseLine = list(map(float, line))
                if CurrentStablePrice != ParseLine[3]:
                    CurrentStablePrice = ParseLine[3]
                    TempData = Date_Time_Price(ParseLine[1], ParseLine[2], CurrentStablePrice)
                    DATA.append(TempData)
    return DATA


def Segmentation(DATA):
    MaxSegmentValue = []
    MinSegmentValue = []
    CurentSegmentIndex = 0;
    for Index, CurData in enumerate(DATA):
        if Index == 0:
            MaxSegmentPrice = pair(Index, CurData.Price)
            MinSegmentPrice = pair(Index, CurData.Price)
            CurentSegmentIndex += 1
        else:
            if CurentSegmentIndex == 100:
                MaxSegmentValue.append(MaxSegmentPrice)
                MinSegmentValue.append(MinSegmentPrice)
                CurentSegmentIndex = 0
                MaxSegmentPrice = pair(Index, CurData.Price)
                MinSegmentPrice = pair(Index, CurData.Price)
            else:
                if MaxSegmentPrice.second < CurData.Price:
                    MaxSegmentPrice = pair(Index, CurData.Price)
                if MinSegmentPrice.second > CurData.Price:
                    MinSegmentPrice = pair(Index, CurData.Price)
                CurentSegmentIndex += 1
    return MaxSegmentValue, MinSegmentValue


DATA = read_mode()
MaxSegmentValue, MinSegmentValue = Segmentation(DATA)
SetTransactions = []

def FindMaxProfit(Begin, End, K):
    if End >= len(MaxSegmentValue) or Begin >= End:
        return 0

    LeftPointer = RightPointer = Begin
    MaxDiffer = 0
    for I in range(Begin, End + 1):
        for J in range(I + 1, End + 1):
            CurrDiffer = MaxSegmentValue[J].second - MinSegmentValue[I].second
            if CurrDiffer > MaxDiffer and CurrDiffer > 0:
                LeftPointer = I
                RightPointer = J
                MaxDiffer = CurrDiffer

    if MaxDiffer <= 0:
        return 0
    else:
        SetTransactions.append(pair(LeftPointer, RightPointer))
        FindMaxProfit(Begin, LeftPointer - 1, K)
        FindMaxProfit(RightPointer, End, K)


def merge1(Arr1, Arr2, Сapital):
    Result = []
    i = 0
    j = 0
    while i < len(Arr1) and j < len(Arr2):
        PurchasedNumber = Сapital // MinSegmentValue[Arr1[i].first].second
        CurProfit_1 = MaxSegmentValue[Arr1[i].second].second * PurchasedNumber -\
                      MinSegmentValue[Arr1[i].first].second * PurchasedNumber

        PurchasedNumber = Сapital // MinSegmentValue[Arr2[j].first].second
        CurProfit_2 = MaxSegmentValue[Arr2[j].second].second * PurchasedNumber - \
                      MinSegmentValue[Arr2[j].first].second * PurchasedNumber
        if CurProfit_1 >= CurProfit_2:
            Result.append(Arr1[i])
            i += 1
        else:
            Result.append(Arr2[j])
            j += 1
    Result += Arr1[i:] + Arr2[j:]
    return Result


def merge_sort1(Arr, Сapital):
    if len(Arr) > 1:
        m = len(Arr) // 2
        return merge1(merge_sort1(Arr[0:m], Сapital), merge_sort1(Arr[m:], Сapital), Сapital)
    else:
        return Arr


def merge(Arr1, Arr2):
    Result = []
    i = 0
    j = 0
    while i < len(Arr1) and j < len(Arr2):
        if Arr1[i].first <= Arr2[j].first:
            Result.append(Arr1[i])
            i += 1
        else:
            Result.append(Arr2[j])
            j += 1
    Result += Arr1[i:] + Arr2[j:]
    return Result


def merge_sort(Arr):
    if len(Arr) > 1:
        m = len(Arr) // 2
        return merge(merge_sort(Arr[0:m]), merge_sort(Arr[m:]))
    else:
        return Arr


if __name__ == "__main__":
    FindMaxProfit(0, len(MaxSegmentValue)-1, 10)
    print("enter the maximum number of transactions", end=" ")
    K = int(input())
    print("enter capital", end=" ")
    Capital = int(input())
    SortedTransact = merge_sort1(SetTransactions, Capital)
    SortedTransact = SortedTransact[:K]
    SortedTransact = merge_sort(SortedTransact)
    ResultProfit = 0
    for CurIndex, CurElem in enumerate(SortedTransact):
        PurchasedNumber = Capital // MinSegmentValue[CurElem.first].second
        Profit = MaxSegmentValue[CurElem.second].second * PurchasedNumber - \
                 MinSegmentValue[CurElem.first].second * PurchasedNumber
        print("Transaction :", CurIndex+1)
        print("Purchase date :", DATA[MinSegmentValue[CurElem.first].first].Date,
                      "Purchase time :", DATA[MinSegmentValue[CurElem.first].first].Time,
                      "Share price upon purchase :", DATA[MinSegmentValue[CurElem.first].first].Price,
                      "Share price on sale :", DATA[MaxSegmentValue[CurElem.first].first].Price,
                      "Date of sale :", DATA[MaxSegmentValue[CurElem.first].first].Date,
                      "Sale time :", DATA[MaxSegmentValue[CurElem.first].first].Time,
                      "Purchase price :", PurchasedNumber * DATA[MinSegmentValue[CurElem.first].first].Price,
                      "Selling price", PurchasedNumber * DATA[MaxSegmentValue[CurElem.first].first].Price,
                      "Profit :", Profit)
        Capital += Profit
        for IndexDATA in range(MinSegmentValue[CurElem.first].first, MaxSegmentValue[CurElem.first].first):
            print("current share price", PurchasedNumber * DATA[IndexDATA].Price)
        print()
    print("final capital : ", Capital)