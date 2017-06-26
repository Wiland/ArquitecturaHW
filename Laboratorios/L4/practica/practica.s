@ ---------------------------------------
@       Data Section
@ ---------------------------------------

        .data
        .balign 4
prompt: .asciz  "\nIngrese un número: "
format: .asciz  "%d"
cbyte   .req    r4              @Contador de bytes para posiciòn del vector
count   .req    r5              @Contador
max     .req    r6              @Numero maximo de registros
ronal:  .int    0
datos:  times dw 50             @Vector de 50 posiciones de enteros

@ ---------------------------------------
@       Code Section
@ ---------------------------------------

        .text
        .global main
        .extern printf
        .extern scanf

main:   push    {ip, lr}        @ push return address + dummy register
                                @ for alignment
        ldr     cbyte, [=datos]
        mov     count, #0
        mov     max, #50

loop:   cmp     count, max          @ Si count es > que max?
        bgt     done            @ yes, va a la subrutina done
                                @ no, output string
        ldr     r0, =prompt
        bl      printf          @ print string and r1 as param

        ldr     r0, =format     @ call scanf, and pass address of format
        ldr     r1, =ronal      @ string and address of n in r0, and r1,
        bl      scanf           @ respectively.

        ldr     r3, [#cbyte]
        mov     r3, [#ronal]
        ldr     r0, =format     @ call scanf, and pass address of format

        add     count, #1       @ n++
        add     cbyte, #2
        b       loop

done:
        pop     {ip, pc}        @ pop return address into pc
