import sys
import random
from llvmcpy.llvm import *

bb_names = {}

def instr_is_call(instr):
    return Opcode[instr.instruction_opcode] == "Call"

def instr_is_branch(instr):
    return Opcode[instr.instruction_opcode] == "Br"

# XXX: confirm that the  pointers are always the same....
def bb_getname(bb):
    if bb in bb_names:
        return bb_names[bb]
    return "bb_unnamed_"+random.randint(10, 999999)

def bb_setname(bb, name):
    bb_names[bb] = name

def out_block(bb, color, out):
    out.write("Node%d" % hash(bb))
    out.write(" [shape=record")
    if color:
        out.write(",color=%s" % color)
    out.write(",label=\"%s\"]" % bb_names[bb])
    out.write(";\n")

def out_edge(bba, bbb, color, out):
    out.write("Node%s -> Node%s" % (hash(bba), hash(bbb)))
    if color:
        out.write((" [color=%s]" % color))
    out.write(";\n")

def process_function(mod, f, out):
    print("In function", f.name.decode("utf-8"), ":")

    #bbs = list(f.iter_basic_blocks())
    # labeling the blocks
    for i, bb in enumerate(f.iter_basic_blocks()):
        bb_setname(bb, ("b%d" % i))

    for bb in f.iter_basic_blocks():
        ti = bb.get_terminator() #bb.get_last_instruction()
        if not ti: # sanity check
            continue
        # Iterate over the instruction of the bb to color it if it has any
        # calls and set  its label to the name of the called functions
        color = None # default
        new_bb_label = ""
        for ins in bb.iter_instructions():
            if instr_is_call(ins):
                fname = ins.get_called().name.decode("utf-8")
                if fname == "llvm.dbg.declare":
                    continue # skip weird llvm intrinsic
                if fname == "":
                    fname = "*"
                color = "blue"
                new_bb_label += ", " + fname
        if new_bb_label != "":
            new_bb_label = new_bb_label[2:]
            bb_setname(bb, new_bb_label)

        out_block(bb, color, out)

        nsuc = ti.get_num_successors()
        for isuc in range(nsuc):
            suc = ti.get_successor(isuc)
            # write an edge from bb to each successor bb
            # but first determine its color:
            # if terminator is conditional branch: green (true) or red (false),
            # otherwise leave default color (Nil)
            color = None
            if instr_is_branch(ti) and ti.is_conditional():
                assert (nsuc == 2), "Conditional Branch should have 2 successors exactly"
                color = "green" if isuc == 0 else "red"
            #if suc.is_basic_block(): TODO
            out_edge(bb, suc, color, out)

        print()
if __name__ == "__main__":
    with open(sys.argv[1]) as asm:
        mod = create_memory_buffer_with_contents_of_file(sys.argv[1]).parse_bitcode2()

    for f in mod.iter_functions():
        if f.is_declaration():
            continue
        with open(f.name.decode("utf-8") + ".dot", "w") as out:
            out.write("digraph G {\n")
            out.write("label=\"CFG for '%s' function\";\n" % f.name.decode("utf-8"))
            process_function(mod, f, out)
            out.write("}")

