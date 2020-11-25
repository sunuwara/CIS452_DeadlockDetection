"""
Title: CIS 452 Project 2: Resource Manager Single Instance Deadlock Detection
Author: Aron Sunuwar
Date: November 24, 2020

Description: This is the class that holds Resource Managers internal logic
"""

import networkx as nx


class ResourceManager:
    """ Class for the Resource Manager that simulates Single instance Deadlock Detection"""

    def __init__(self, numProcesses, numResources):
        self.rag = nx.DiGraph()
        self.numProcesses = numProcesses
        self.numResources = numResources
        self.deadlocked = list()

    def initialize(self):
        """ Initialize the Resource Managers resource allocation graph and add nodes"""
        print(
            f"Number of processes = {self.numProcesses}, Number of Resources = {self.numResources}")

        # Add process nodes to resource allocation graph
        for x in range(self.numProcesses):
            node = "P" + str(x)
            self.rag.add_node(node, holds=[], requests=[])

        # Add resource nodes to resource allocation graph
        for x in range(self.numResources):
            node = "R" + str(x)
            self.rag.add_node(node, heldBy="", requestedBy=[])

    def handleRequests(self, process, resource):
        """ Handles requests from process to resource and updates resource allocation graph """

        pNode = self.rag.nodes[process]
        rNode = self.rag.nodes[resource]
        message = f"Request: {process} requests {resource}"

        if not rNode['heldBy']:
            # Handle case where requested resource isn't held by any process
            pNode['holds'].append(resource)
            rNode['heldBy'] = process
            self.rag.add_edge(resource, process)
            message += f", {process} now holds {resource}"

        else:
            # Handle case where requested resource belongs to another process
            pNode['requests'].append(resource)
            rNode['requestedBy'].append(process)
            self.rag.add_edge(process, resource)
            message += f", {resource} is taken, {process} will wait"

        print(message)

        return message

    def handleFrees(self, process, resource):
        """ Handles frees from process to resource, updates resource allocation graph """

        pNode = self.rag.nodes[process]
        rNode = self.rag.nodes[resource]
        message = ""

        # Frees resource held by process
        pNode['holds'].remove(resource)
        rNode['heldBy'] = ""
        self.rag.remove_edge(resource, process)
        message = f"FREE: {process} releases {resource}"

        if rNode['requestedBy']:
            # Handle case where resource is requested by another process
            nextProcess = rNode['requestedBy'].pop(0)
            npNode = self.rag.nodes[nextProcess]

            npNode['holds'].append(resource)
            npNode['requests'].remove(resource)
            rNode['heldBy'] = nextProcess

            self.rag.remove_edge(nextProcess, resource)
            self.rag.add_edge(resource, nextProcess)
            message += f", {nextProcess} now holds {resource}"

        print(message)

        return message

    def detectDeadlock(self, startNode):
        """
            Detect any deadlocks in the Resource Allocation Graph.

            In the case of Single Instance Resource Allocation Graph if there is any
            cycle then there is sufficient condition for deadlock:
            https://www.geeksforgeeks.org/resource-allocation-graph-rag-in-operating-system/
        """
        visited = list()
        self.deadlocked.clear()

        if self.hasCycle(self.rag, startNode, visited):
            for node in visited:
                if node[0] == "P":
                    self.deadlocked.append(node)
            return True

        return False

    def hasCycle(self, graph, node, visited):
        """
            Checks recursively if directed graph has cycle

            To detect cycle in a directed graph Depth First Search can be used:
            https://www.geeksforgeeks.org/detect-cycle-in-a-graph/
        """

        print(f"\n{visited}")

        # Repeat for each neighbor nodes
        for neighbor in graph.neighbors(node):
            # Add current node to visited
            visited.append(node)

            print(f"Current node: {node}, neighbor: {neighbor}")
            if neighbor in visited:
                # If neighbor node is in visited then cycle exists
                return True
            else:
                # Otherwise recusively check neighbor's nodes
                if self.hasCycle(graph, neighbor, visited):
                    return True

        # If node has no neighbors then return false

        return False

    def recoverFromDeadlock(self, preemptionResource):
        """
            Recovers from deadlock by forcing the process holding the resource
            that caused the deadlock to let go. Since this is a Single Instance
            Resource preempting the resource that caused deadlock wont lead to
            starvation because eventually some process will get hold of this
            resource
        """
        message = f"Recover: {preemptionResource} disconnects from {self.rag.nodes[preemptionResource]['heldBy']}\n"

        message += self.handleFrees(
            self.rag.nodes[preemptionResource]['heldBy'], preemptionResource)

        print(message)
        return message
