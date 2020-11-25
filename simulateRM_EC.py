"""
Title: CIS 452 Project 2: Resource Manager Single Instance Deadlock Detection
Author: Aron Sunuwar
Date: November 24, 2020

Description: This is program simulates and operating system functioning as a
             Resource Manager for Single Instance Deadlock Detection. This
             program takes in input files containing the details of processes
             and resources as well as the activity of processes.

             The format of input files follows:
             Processes: integer representing the total number of processes in
                        the system
             Resources: integer representing the total number of resources in
                        the system
             Resource request: char r followed by process number followed by
                        the resource number it is requesting (r 0 1)
             Resource release: char f followed by process number followed by
                        the resource number it is releasing (f 0 1)
"""

from os import error
import sys
from ResourceManager import ResourceManager
from GraphGUI import GraphGUI

filename = "scenario-2.txt"


def readFile(filepath):
    """ Reads file and saves to array of lines """
    fileIn = open(filepath, 'r')
    lines = fileIn.readlines()
    lineList = []

    for line in lines:
        lineList.append(line.strip('\n'))

    return lineList


if __name__ == "__main__":

    """ Read file and gets list of lines """
    lines = readFile(filename)

    """ Initialize Resource Manager and create resource allocation graph """
    resourceManager = ResourceManager(int(lines[0]), int(lines[1]))
    resourceManager.initialize()

    """ Initialize Graph GUI and initialize """
    gui = GraphGUI(resourceManager.rag)
    gui.initialize(filename)
    gui.display(filename)

    """ Run through rest of the lines, execute actions and check for deadlock """
    for line in lines[2:]:

        # read line and save action, process number and resource number
        action = line[0]
        process = "P" + line[2]
        resource = "R" + line[4]
        message = ""

        # Handle requests: P# requests R#
        if (action == 'r'):
            message = resourceManager.handleRequests(process, resource)

        # Handle frees: P# releases R#
        if (action == 'f'):
            message = resourceManager.handleFrees(process, resource)

        # Check and handle deadlock
        if resourceManager.detectDeadlock(resource):
            error = f"\nERROR: System is deadlocked with processes: {resourceManager.deadlocked}"
            message += error
            print(error)

            gui.display(message)

            message = resourceManager.recoverFromDeadlock(resource)

        gui.display(message)

        print("")
        for node in resourceManager.rag:
            print(f"{node}: {resourceManager.rag.nodes[node]}")
        print("")

    gui.close()
