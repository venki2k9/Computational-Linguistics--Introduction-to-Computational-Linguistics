import os

target_file = "/Users/tumuluri/DNA_targets/targets"
dna_sequence_location = "/Users/tumuluri/DNA"

class Node:
    childnodes = None
    endofsequenceflag = None
    TerminalNode = None

    def __init__(self):
        self.childnodes = {"A":None,"T":None,"C":None,"G":None}
        self.endofsequenceflag = False
        self.TerminalNode = True

    def getChildNode(self,incoming_chr):
        child_node = None
        if self.childnodes.has_key(incoming_chr):
            if self.childnodes[incoming_chr]:
                child_node = self.childnodes[incoming_chr]
        return child_node

    def FlagNonTerminalNode(self):
        self.TerminalNode = False

    def FlagEndOfSequence(self):
        self.endofsequenceflag = True

    def CreateChild(self,incoming_chr,node):
        self.childnodes[incoming_chr] =  node
        self.FlagNonTerminalNode()

class TargetPatternTree:
    root = None
    creation_pointer = None
    search_pointer = None
    def __init__(self):
        self.root = Node()
        self.creation_pointer = self.root
        self.search_pointer = self.root

    def ArrangeItemsInTree(self,chr,end_of_sequence):
        pointer = self.creation_pointer
        if end_of_sequence:
            pointer.FlagEndOfSequence()
        child = pointer.getChildNode(chr)
        if not child:
            child = Node()
            pointer.CreateChild(chr,child)
        self.creation_pointer = child

    def InsertIntoTree(self,target):
        for idx,chr in enumerate(target):
            if idx == len(target)-1:
                self.ArrangeItemsInTree(chr, end_of_sequence=True)
            else:
                self.ArrangeItemsInTree(chr,end_of_sequence=False)
        self.creation_pointer = self.root

    def SearchTree(self,dna_seq):
        last_sequence_idx =0
        for idx,seq_chr in enumerate(dna_seq):
            #print(seq_chr)
            if self.search_pointer.getChildNode(seq_chr):
                if self.search_pointer.endofsequenceflag:
                    print(str(hex(idx)) + '\t' + dna_seq[last_sequence_idx:idx+1])
                    if self.search_pointer.getChildNode(seq_chr).TerminalNode:
                        self.search_pointer = self.root
                        last_sequence_idx = idx + 1
                    else:
                        child_node = self.search_pointer.getChildNode(seq_chr)
                        self.search_pointer = child_node
                else:
                    child_node = self.search_pointer.getChildNode(seq_chr)
                    self.search_pointer = child_node
            else:
                self.search_pointer = self.root
                last_sequence_idx = idx +1



    def getChildNodes(self,node):
        print(node.childnodes.keys)
        print(node.childnodes.values)


    def DescribeTree(self):
        collection_of_nodes = []
        process_nodes = []
        process_nodes.append(self.root)
        while len(process_nodes) >0:
            process_node =  process_nodes.pop()
            if process_node:
                process_nodes.append(process_node.childnodes["G"])
                process_nodes.append(process_node.childnodes["T"])
                process_nodes.append(process_node.childnodes["C"])
                process_nodes.append(process_node.childnodes["A"])

            collection_of_nodes.append(process_node)
        print("# Node in Tree: "+ str(len(collection_of_nodes)))
        for ele in collection_of_nodes:
            if ele:
                print(ele.childnodes)





def GetTargets(target_file):
    target_tree = TargetPatternTree()
    fl = open(target_file,'r')
    for line in fl.readlines():
        line = line.strip()
        line = line.upper()
        target_tree.InsertIntoTree(line)
    return target_tree


def TestTargets():
    target_tree = TargetPatternTree()
    target_tree.InsertIntoTree('TG')
    #target_tree.DescribeTree()
    target_tree.InsertIntoTree('TGC')
    #target_tree.DescribeTree()
    target_tree.InsertIntoTree('TGCA')
    #target_tree.DescribeTree()
    target_tree.InsertIntoTree('GCA')
    #target_tree.DescribeTree()
    target_tree.SearchTree('GCAGCAGCATGCATGCAGCAGCAGCATGCATGCAGCAGCAGCATGCATGCAGCAGCAGCATGCATGCAGCAGCAGCATGCATGCAGCAGCAGCATGCATGCAGCAGCAGCATGCATGCAGCAGCAGCATGCATGCAGCAGCAGCATGCATGCAGCAGCAGCATGCATGCAGCAGCAGCATGCATGCAGCAGCAGCATGCATGCANNGATGCA')

def GetDNASequences(DNA_Sequence_loc,target_tree):
    for fl in os.listdir(DNA_Sequence_loc):
        fl = os.path.join(DNA_Sequence_loc,fl)
        fobj = open(fl,'r')
        dna_seq_str = fobj.read()
        dna_seq_str = dna_seq_str.strip()
        dna_seq_str = dna_seq_str.upper()
        target_tree.SearchTree(dna_seq_str)
        return dna_seq_str


#TestTargets()
target_tree = GetTargets(target_file=target_file)
#target_tree.DescribeTree()
GetDNASequences(dna_sequence_location,target_tree=target_tree)
