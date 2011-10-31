#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

if __name__ == "__main__":
    for ccolor in range(1024):
        r = ccolor % 0xFF
        g = (ccolor / 0xFF) % 0xFF
        b = (ccolor / 0xFF / 0xFF) % 0xFF
        print r,g,b
        assert r + g*0xFF + b*0xFF*0xFF == ccolor