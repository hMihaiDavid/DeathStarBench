import sys
import random
from cxxfilt import demangle
from llvmcpy.llvm import *

bb_labels = {}

def escape_str(s):
    return s.replace("&", "&amp;").replace("\"", "&quot;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|")

def instr_is_call(instr):
    return Opcode[instr.instruction_opcode] == "Call"
def instr_is_invoke(instr):
    return Opcode[instr.instruction_opcode] == "Invoke"
def instr_is_branch(instr):
    return Opcode[instr.instruction_opcode] == "Br"

# XXX: confirm that the  pointers are always the same....
def bb_getlabel(bb):
    if bb in bb_labels:
        return bb_labels[bb]
    return "bb_unnamed_"+random.randint(10, 999999)

def bb_setlabel(bb, name):
    bb_labels[bb] = name

def out_block(bb, color, out):
    out.write("Node%d" % hash(bb))
    out.write(" [shape=record")
    if color:
        out.write(",color=%s" % color)
    out.write(",label=<%s>]" % bb_getlabel(bb))
    out.write(";\n")

def out_edge(bba, bbb, color, out):
    out.write("Node%s -> Node%s" % (hash(bba), hash(bbb)))
    if color:
        out.write((" [color=%s]" % color))
    out.write(";\n")

def process_function(mod, f, out):
    #print("In function", f.name.decode("utf-8"), ":")

    #bbs = list(f.iter_basic_blocks())
    # labeling the blocks
    for i, bb in enumerate(f.iter_basic_blocks()):
        bb_setlabel(bb, ("b%d" % i))

    for bb in f.iter_basic_blocks():
        ti = bb.get_terminator() #bb.get_last_instruction()
        if not ti: # sanity check
            continue
        bb_label = "<font color='gray'>"+Opcode[bb.get_first_instruction().instruction_opcode]+"</font><br />"
        for ins in bb.iter_instructions():
            if instr_is_call(ins) or instr_is_invoke(ins):
                color = "blue" if instr_is_call(ins) else "orange"
                fname = ins.get_called().name.decode("utf-8")
                if fname == "llvm.dbg.declare":
                    continue # skip weird llvm intrinsic
                if fname == "":
                    fname = "*"
                try:
                    fname = demangle(fname, external_only=False)
                except:
                    pass
                s = fname.replace("std::__cxx11::","").replace("std::", "").replace("apache::thrift::", "")
                print(s)
                s = escape_str((s[:60]+"...") if len(s) > 62 else s)
                print(s)
                bb_label += ("<font color='%s'>" % color)+s+"</font><br align='center'/>"
        bb_label += "<br /><font color='gray'>"+Opcode[ti.instruction_opcode]+"</font>"
        bb_setlabel(bb, bb_label)

        out_block(bb, None, out)

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

#class Dummy:
#    def write(self, nothin):
#        pass

if __name__ == "__main__":
    with open(sys.argv[1]) as asm:
        mod = create_memory_buffer_with_contents_of_file(sys.argv[1]).parse_bitcode2()
    mangle_map_file = open("mangle_map.txt", "w")
    i=0
    for f in mod.iter_functions():
        if f.is_declaration():
            continue
        #if i != 743:
        #    i = i + 1
        #    continue

        fname = f.name.decode("utf-8")
        fname_deman = fname
        try:
            fname_deman = demangle(fname)
        except:
            fname_deman = fname
            pass

        with open(("res/f%d.dot") % i, "w") as out:
            out.write("digraph G {\n")
            print(fname_deman)
            out.write("label=<CFG for '%s' function>;\n" % escape_str(fname_deman))
            #out = Dummy()
            process_function(mod, f, out)
            out.write("}")
        mangle_map_file.write("%d %s %s\n" % (i, fname, fname_deman))
        i = i + 1

