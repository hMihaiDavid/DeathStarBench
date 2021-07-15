#include <stdio.h>
#include <stdlib.h>

void foo() {
    int a = 1;
}
void bar() {
    int a = 2;
}
void baz() {
    int a = 3;
}

int loopy() {
    int sum = 0;
    for (int i = 0; i < 42; i++) {
        sum = sum + i*10;
    }

    int i = 0;
    while(i < 69) {
        sum += i*10;
        sum++;
    }

    return sum;
}

void (*fun_ptr)(void) = foo;
void *func_ptrs[] = {foo, bar, baz};

void setfp(int sel) {
    if (sel < 0) sel = 0;
    fun_ptr = func_ptrs[sel % 3];
}

void callfp() {
    loopy();
    fun_ptr();
    loopy();
}

int main() {
    int sel = -1;
    if (scanf("Select option: %d\n", &sel) < 1) return -1;

    // Switch statement
    switch (sel) {
        case 0: // dummy computations with loops
            printf("loopy() = %d\n", loopy());
            break;
        case 1: // call the function pointer
            callfp();
            break;
        case -1:
            exit(0);
        default: // set the function pointer
            setfp(sel);
    }
    return 0;
}
