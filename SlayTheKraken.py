#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys
print(sys.path)


from dashboard import plot_prices_continuously


def main():
    plot_prices_continuously()

if __name__ == '__main__':
    main()