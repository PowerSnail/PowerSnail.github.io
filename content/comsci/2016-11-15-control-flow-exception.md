---
layout: page
title: "Exceptional Control Flow"
description: "Reading Notes on CSAPP"
tags:
    - computer science
    - notes
    - study
    - csapp
    - reading notes
mathjax: true
date: "2016-11-15"
---

## Overview

A processor accesses a sequence of instructions when it operates. The transition from one to the next, is called *control transfer*. The sequence of transfers is called *control flow*. The control flow is smooth when the transitions are always to the adjacent address. Operations such as `jump`, `call`, etc. will cause the control flow to be abrupt. 

There are other situations where the control flow is abruptly changed. For example, hardware timer, network packet arrival, etc. are events that have to be dealt with but not necessarily a part of the execution of the program. The system will likely deal with such situations with *exceptional control flow* (ECF), a disruption to the control flow. 

- Application Level ECF: inter-process *signal*
- OS kernel Level ECF: context switches

## Exceptions

### Definition

An *exception* is an abrupt change in the control flow in response to some change in the processor's state. 

An *event* is a change in the processor's state.

### Exception Happening

When the application is executing instruction $I_{curr}$, there is an event occurred.

The event could be either caused by the instruction just occurred, or completely unrelated to the application. The processor will look up the *exception table*, and make a procedure call to the *exception handler*, which will process the particular kind of event. Then, depending on the event, three things can occur:

1. The handler returns, to $I_{curr}$
2. The handler returns, to $I_{next}$
3. The handler aborts the program

### Exception Handling

The handling of exception involves both hardware and software.

Each type of exception is assigned an integer *exception number*, assigned by:

- The designer of the processor
    + divide by zero
    + page faults
    + memory access violations
    + break-points
    + arithmetic overflows
- The OS kernal
    + system calls
    + signals from external I/O devices

At **Boot time**, the OS creates the exception table, mapping each exception number to the address of the exception handler for the particular type of exception.

The table's base address is contained in a CPU register, *exception table base register*. 

At **Run time**, the processor detects the event, and determines the exception number $k$. Then it makes an indirect procedure call through the address in table[$k$]. 

The procedure call is accompanied by a few operations:

- the processor pushes the address of $I_{curr}$ or $I_{next}$ on to the **kernal stack**
- the control is transferred to the kernal, which means the exception handlers run in **kernal mode**, that they have access to all system resources.

The return is a special operation `return from interrupt`, which restores kernal mode to user mode. 

### Class of Exceptions

| Class | Cause | Async/Sync | Return behavior |
| ----- | ----- | ---------- | --------------- |
| Interrupt | Signal from I/O device | Async | Aways returns to next instruction |
| Trap | Intentional exception | Sync | Always returns to next instruction |
| Fault | Potentially recoverable error | Sync | Might return to current instruction |
| Abort | Nonrecoverable error | Sync | Never returns |

Table 1: Classes of Exceptions [^1]


*Async*: means that the event (IO Interrupt) is not caused by execution of any instruction, but rather an asynchronous signal that an external IO device sends to the processor. 

#### Interrupt Handling

The handling of interrupt runs independent from the program. It is not caused by, has no impact on the current program. The processor notices the interrupt pin is set, and jumps to the interrupt handler. The handler will return to $I_{next}$, as though nothing has happened.

#### Traps and System Calls

Traps are intentional exceptions, likely to help interface between user program and the kernal, which is a *system call*. Trap handlers also return to $I_{next}$ like interrupt handlers. 

System Calls:

- `read`: file reading
- `fork`: create a new process
- `execve`: loading a new program
- `exit`: terminating the current process

Remember that syscall runs in kernal mode and is thus different from normal procedure calls. 

#### Faults

Faults are error conditions tha a handler might be able to correct. If the error is corrected, the handler will return to $I_{curr}$ (the faulting instruction), so it is re-executed. Otherwise, the handler will returns to an abort routine to terminate the program

#### Aborts

Aborts result from unrecoverable fatal errors, for example, DRAM bits corruption. 

### Example Exceptions in Linux/x86-64 Systems

- **Divide error**: divide by zero, usually ends up in `abort`. (Floating exceptions)
- **General protection fault**: usually because the program references an undefined area of virtual memory, or tries to write to read-only text segment. Usually ends up in `abort`. (Segmentation Fault)
- **Page Fault**: Page of virtual memory is not resident in memory, needs to be retrieved from disk. The exception is `fault`, and the handler will re-execute the faulting instruction after loading the page. 
- **Machine check**: Fatal hardware error is detected during execution of the faulting instruction. It directly goes to `abort`.

Syscalls:

| Number | Name | Description |
| ------ | ---- | ----------- |
| 0 | `read` | Read file |
| 1 | `write` | write file |
| 2 | `open` | open file |
| 3 | `close` | close file |
| 4 | `stat` | Get info about file |
| 9 | `mmap` | map memory page to file |
| 12 | `brk` | Reset the top the heap |
| 32 | `dup2` | copy file descriptor |
| 33 | `pause` | suspend process until signal arrives |
| 37 | `alarm` | schedule delivery of alarm signal |
| 39 | `getpid` | get process id |
| 57 | `fork` | create process |
| 59 | `execve` | execute a program |
| 60 | `_exit` | terminate process |
| 61 | `wait4` | wait for a process to terminate |
| 62 | `kill` | send a signal to a process

### C and Syscalls

C/C++ programs can call syscall directly. For example,

```c
int main()
{
    write(1, "hello, world\n", 13);
    _exit(0);
}
```

In syscall, the syscall id is passed in `%rax`, and arguments are passed through `%rdi`, `%rsi`, `%rdi`, `%r10`, `%r8`, `%r9`, in order. 

Equivalent Assembly Program

```nasm
.section .data
string:
    .ascii "hello, world\n"
string_end:
    .equ len, string_end - string
.section .text
.global main
main:
    movq $1, %rax           # syscall code: write = 1
    movq $1, %rdi           # Arg1: stdout
    movq $string, %rsi      # Arg2: string
    movq $len, %rdx         # Arg3: length
    syscall

    movq $60, %rax          # syscall code: _exit = 60
    movq $0, %rdi           # Arg1: exist status = 0
    syscall
```

## Processes

The concept of *process* provides the illusion of 

- our program has exclusive use of CPU and memory
- the processor executes the instructions of our program without interuption
- the code and data of the program appeas to be the only objects in memory

A process is an instance of a program in execution. This means it includes:

- the code in memory,
- the data in memory,
- the stack of the program
- the general-purpose registers
- the program counters
- environmnet variables
- the set of open file descriptors

These states are the *context* of the program.

### Logical Control Flow

We perceive the illusionary control flow, that registers, memory, etc. are changed step by step completely according to the instruction set of our program. This control flow is called **Logical Control Flow**.

In reality, processes take turns to use the processor. Each process runs for a short period of time and is preempted (temporarily suspended), until the next turn. 

This short time period is called *time slice*.

### Concurrent Flows

A logical flow whose execution overlaps in time with another flow is called a concurrent flow. Two flows run *concurrently*.

### Parallel Flows

The concurrent flows that run on different processor cores or computers are called *parallel flows*.

### Private Address Space

The illusion that the program has exclusive use of address space is provided by *private address space*. This "space" of addresses cannot be read/written by other programs, and therefore is exclusive to the program. 

### User Mode vs Kernel Mode

The OS restricts each process what instructions can be executed and what memory space can be accessed. The processor provides the capability with a `mode bit`. 

`mode bit` | Mode | Instruction | Memory Space
---------- | ---- | ----------- | ------------
1 | Kernel Mode | Any Instruction | Any Memory
0 | User Mode | No Priviledged Instruction | No reference to code/data in kernel area 

Priviledged Instruction: `syscall` functions, including halt, change mode, I/O op, etc.

#### /proc

`/proc` is a linux filesystem mount of the kernal data structure. It allows the user to access general system attributes. 

### Context Switch

The kernel maintains a context for each process. The context is the state that the kernel needs to restart a preempted process. 

- values of general-purpose registers,
- floating-point registers
- program counter
- user's stack
- status registers
- kernel's stack
- various kernel data structure
    + page table
    + process table
    + file table

**Scheduling**, deciding to preempt a process and restart a preempted process. This is handled by **scheduler**, a code in the kernel.  

The kernel can decide to switch when the process is waiting for a read. The IO device can take care of the work, so the kernel will switch to another process, until the IO device sends an interrupt signalling successful transfer of data into the memory. 

## System Call Error Handling

When a systemlevel function encounter an error, they return $-1$, and set the global integer variable `errno` to indicate what went wrong. 

An error checking fork function:

```c
void unix_error(char *msg)
{
    fprintf(stderr, "%s: %s\n", msg, strerror(errno));
    exit(0);
}

pid_t Fork(void)
{
    pid_t pid;
    if ((pid = fork()) < 0) // <- check for error return value
        unix_error("Fork error");
    return pid;
}
```

## Signals

A signal is a small message that notifies a process that an event of some type has occurred in the system. 

### Sending Signal

The kernel sends a signal because:

- the kernel detects a system event 
- a process invoked `kill` function

#### Process Group

Each process belongs to exactly one process group. By default, a child process belongs to the same group as its parent.

The Process Group ID can be read/write using `getpgrp` and `setpgid`.

#### `/bin/kill`

`/bin/kill -9 15213` sends a signal 9 (SIGKILL) to process 15213. 

`/bin/kill -9 -15213` sends a signal 9 to ever process in group 15213

#### from Keyboard

A unix shell has at most 1 foreground job and zero or more background jobs. Typing <kbd>ctrl</kbd> + <kbd>c</kbd> causes the kernel to send SIGINT to every process in the foreground process group. <kbd>ctrl</kbd> + <kbd>z</kbd> sends SIGTSTP signal to every process in the foreground process group, which pauses them. 

#### Calling `kill` function

```c
#include <sys/types.h>
#include <signal.h>

int kill(pid_t pid, int sig)
```


If :

- `pid` > 0, send `sig` to process[`pid`]
- `pid` = 0, send `sig` to process group that currnt process belongs
- `pid` < 0, send `sig` to process group [|`pid`|]


#### Calling `alarm` function

```c
#include <unistd.h>

unsigned int alarm (unsigned int secs);
```

Arranges the kernel to send SIGALRM signal to the calling process in `secs` seconds. If secs == 0, then no new alarm is scheduled. 

It returns the remaining secondsd of previous alarm.

A call of `alarm` cancels all previous `alarm`s.

### Receiving Signal

The kernel checks for any *pending and not blocked* signals, when switching a process from kernel mode to user mode, i.e. from an Interrupt, syscall, or context switching. 

If there is no such signals, then it will proceed to $I_{next}$. Otherwise, the kernel will choose a signal and force the process to receive it. The receipt will trigger some action, and once the action is completed, the kernel proceeds to $I_{next}$.

There is a default action associated with each signal; the user program can change it by using a `signal` function

```c
#include <signal.h>

typedef void(*sighandler_t)(int);

sighandler_t signal(int signum, sighandler_t handler);
```

Then `handler` can be SIG_IGN (ignore), SIG_DFL (default), or the address of a user-defined function, a *signal handler.


[^1]: Figure 8.5, CSAPP