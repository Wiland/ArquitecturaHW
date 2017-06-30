/* print-array.s */
/* ************************************** DECLARACIÓN DE VARIABLES **************************************** */
.data

/* declare an array of 10 integers called my_array */
.align 4
my_array: .word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
          .word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
          .word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
          .word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
          .word 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

.align 4
integer_printf: .asciz "%d " /* format string that prints an integer plus a space */

.align 4
newline_printf: .asciz "\n" /* format string that simply prints a newline */

.align 4
prompt: .asciz  "\nIngrese un número: " /* Texto para mostrar antes de ingresar el número */
format: .asciz  "%d" /* Formato en el que el usuario ingresa el número */
txt_orden: .asciz  "\nVector ordenado ascendentemente: "
txt_menor: .asciz  "\nNúmero menor: %d"
txt_moda: .asciz  "\n\nModa: %d con %d repeticiones"
txt_prome: .asciz  "\n\nPromedio aproximado: %d"

num: .word 0 /* Número ingresado por el usuaro */


/* ********************************************* CUERPO *************************************************** */
.text
/* Asignación de variables (apuntadores a datos que se requieren más adelante) */
addr_of_integer_printf: .word integer_printf
addr_of_newline_printf: .word newline_printf
addr_of_my_array: .word my_array
addr_of_integer_comparison : .word integer_comparison


/* --------------------------------- FUNCIONES --------------------------------------- */

/* Función para Imprimir el arreglo*/
print_array:
    /* r0 will be the address of the integer array */
    /* r1 will be the number of items in the array */
    push {r4, r5, r6, lr}  /* keep r4, r5, r6 and lr in the stack */

    mov r4, r0             /* r4 ← r0. keep the address of the array */
    mov r5, r1             /* r5 ← r1. keep the number of items */
    mov r6, #0             /* r6 ← 0.  current item to print */

    b .Lprint_array_check_loop /* go to the condition check of the loop */

    .Lprint_array_loop: /* prepare the call to printf */
      ldr r0, addr_of_integer_printf  /* r0 ← &integer_printf */
      /* load the item r6 in the array in address r4. Elements are of size 4 bytes so we need to multiply r6 by 4 */
      ldr r1, [r4, +r6, LSL #2]       /* r1 ← *(r4 + r6 << 2)
                                         this is the same as
                                         r1 ← *(r4 + r6 * 4) */
      bl printf                       /* call printf */

      add r6, r6, #1                  /* r6 ← r6 + 1 */

    .Lprint_array_check_loop:
      cmp r6, r5               /* perform r6 - r5 and update cpsr */
      bne .Lprint_array_loop   /* if cpsr states that r6 is not equal to r5
                                  branch to the body of the loop */

    /* prepare call to printf */
    ldr r0, addr_of_newline_printf /* r0 ← &newline_printf */
    bl printf

    pop {r4, r5, r6, lr}   /* restore r4, r5, r6 and lr from the stack */
    bx lr                  /* return */

/* Función para Llenar arreglo */
fill_array:
    /* r0 will be the address of the integer array */
    /* r1 will be the number of items in the array */
    push {r4, r5, r6, lr}  /* keep r4, r5, r6 and lr in the stack */

    mov r4, r0             /* r4 ← r0. keep the address of the array */
    mov r5, r1             /* r5 ← r1. keep the number of items */
    mov r6, #0             /* r6 ← 0.  current item to print */

    .Lfill_array_loop: /* prepare the call to printf */
      ldr r0, addr_of_integer_printf  /* r0 ← &integer_printf */

      ldr     r0, =prompt     @ print the prompt
      bl      printf

      ldr     r0, =format     @ call scanf, and pass address of format
      ldr     r1, =num        @ string and address of num in r0, and r1,
      bl      scanf           @ respectively.

      ldr     r1, =num        @ print num formatted by output string.
      ldr     r1, [r1]        @ print num formatted by output string.
      str     r1, [r4, +r6, LSL #2]

      add r6, r6, #1                  /* r6 ← r6 + 1 */
      add r11, r11, r1

    .Lfill_array_check_loop:
      mov r8, r6
      cmp r6, r5               /* perform r6 - r5 and update cpsr */
      bne .Lfill_array_check_user_input   /* if cpsr states that r6 is not equal to r5 branch to the user input validation */
      b .Lend_array_fill

    .Lfill_array_check_user_input:
      cmp r1, #0               /* perform r1 - 0 and update cpsr */
      bne .Lfill_array_loop   /* if cpsr states that r7 is not equal to 0 branch to the body of the loop */
      sub r8, r6, #1

    .Lend_array_fill:
      /* prepare call to printf */
      ldr r0, addr_of_newline_printf /* r0 ← &newline_printf */
      bl printf

    pop {r4, r5, r6, lr}   /* restore r4, r5, r6 and lr from the stack */
    bx lr                  /* return */

/* Función para Calcular promedio */
calculate_average:
    /* r0 contains N */
    /* r1 contains D */
    mov r0, r11
    mov r1, r8

    mov r2, r1             /* r2 ← r0. We keep D in r2 */
    mov r1, r0             /* r1 ← r0. We keep N in r1 */

    mov r0, #0             /* r0 ← 0. Set Q = 0 initially */

    b .Lloop_check
    .Lloop:
       add r0, r0, #1      /* r0 ← r0 + 1. Q = Q + 1 */
       sub r1, r1, r2      /* r1 ← r1 - r2 */
    .Lloop_check:
       cmp r1, r2          /* compute r1 - r2 */
       bhs .Lloop            /* branch if r1 >= r2 (C=0 or Z=1) */

    /* r0 already contains Q */
    /* r1 already contains R */
    bx lr

/* Función para calcular promedio */ /**** NO SE USA ****/
calculate_average_binary:
    /* r0 contains N and Ni */
    /* r1 contains D */
    /* r2 contains Q */
    /* r3 will contain Di */

    mov r0, r11
    mov r1, r8

    mov r3, r1                   /* r3 ← r1 */
    cmp r3, r0, LSR #1           /* update cpsr with r3 - r0/2 */
    .Lloop2:
      movls r3, r3, LSL #1       /* if r3 <= 2*r0 (C=0 or Z=1) then r3 ← r3*2 */
      cmp r3, r0, LSR #1         /* update cpsr with r3 - (r0/2) */
      bls .Lloop2                /* branch to .Lloop2 if r3 <= 2*r0 (C=0 or Z=1) */

    mov r2, #0                   /* r2 ← 0 */

    .Lloop3:
      cmp r0, r3                 /* update cpsr with r0 - r3 */
      subhs r0, r0, r3           /* if r0 >= r3 (C=1) then r0 ← r0 - r3 */
      adc r2, r2, r2             /* r2 ← r2 + r2 + C.
                                    Note that if r0 >= r3 then C=1, C=0 otherwise */

      mov r3, r3, LSR #1         /* r3 ← r3/2 */
      cmp r3, r1                 /* update cpsr with r3 - r1 */
      bhs .Lloop3                /* if r3 >= r1 branch to .Lloop3 */

    bx lr

/* Función para Calcular moda */
calculate_trend:
    /* r0 will be the address of the integer array */
    /* r1 will be the number of items in the array */
    push {r4, r5, r6, lr}  /* keep r4, r5, r6 and lr in the stack */

    mov r2, #0   /* Número repetido */
    mov r3, #0   /* Cantidad de repeticiones */
    mov r9, #0   /* Número repetido (Temporal) */
    mov r12, #0  /* Cantidad de repeticiones (Temporal) */

    mov r4, r0             /* r4 ← r0. keep the address of the array */
    mov r5, r1             /* r5 ← r1. keep the number of items */
    mov r6, #0             /* r6 ← 0.  current item to print */

    b .Ltrend_check_loop /* go to the condition check of the loop */

    .Ltrend_loop: /* prepare the call to printf */
      ldr r0, addr_of_integer_printf  /* r0 ← &integer_printf */
      /* load the item r6 in the array in address r4. Elements are of size 4 bytes so we need to multiply r6 by 4 */
      ldr r1, [r4, +r6, LSL #2]       /* r1 ← *(r4 + r6 << 2)
                                         this is the same as
                                         r1 ← *(r4 + r6 * 4) */

      cmp r12, #0
      beq .Lfirst_line
      bne .Lcontinue_loop

      .Lfirst_line:
        mov r9, r1

      .Lcontinue_loop:
        add r6, r6, #1                  /* r6 ← r6 + 1 */

      cmp r1, r9            /* Número actual = Número repetido */
      beq .Ltrend_add

      cmp r12, r3           /* Cantidad de rep actual > Cantidad rep almacenado */
      bgt .Lnew_trend
      b .Ltrend_check_loop

    .Ltrend_add:
      add r12, r12, #1  /* r12 ← r12 + 1 */
      b .Ltrend_check_loop

    .Lnew_trend:
      mov r2, r9
      mov r9, r1
      mov r3, r12
      mov r12, #1

    .Ltrend_check_loop:
      cmp r6, r5               /* perform r6 - r5 and update cpsr */
      bne .Ltrend_loop   /* if cpsr states that r6 is not equal to r5
                                  branch to the body of the loop */
    mov r1, r2
    mov r2, r3
    ldr r0, =txt_moda
    bl  printf

    /* prepare call to printf */
    ldr r0, addr_of_newline_printf /* r0 ← &newline_printf */
    bl printf

    pop {r4, r5, r6, lr}   /* restore r4, r5, r6 and lr from the stack */
    bx lr                  /* return */

/* Función para comparar dos números (devuelve 1, 0 ó -1) */
integer_comparison:
    /* r0 will be the address to the first integer */
    /* r1 will be the address to the second integer */
    ldr r0, [r0]    /* r0 ← *r0
                       load the integer pointed by r0 in r0 */
    ldr r1, [r1]    /* r1 ← *r1
                       load the integer pointed by r1 in r1 */

    cmp r0, r1      /* compute r0 - r1 and update cpsr */
    moveq r0, #0    /* if cpsr means that r0 == r1 then r0 ←  0 */
    movlt r0, #-1   /* if cpsr means that r0 <  r1 then r0 ← -1 */
    movgt r0, #1    /* if cpsr means that r0 >  r1 then r0 ←  1 */
    bx lr           /* return */


/* ********************************************* MAIN *************************************************** */
.globl main
main:
    push {r4, lr}             /* keep r4 and lr in the stack */

    /* prepare call to print_array */
    ldr r0, addr_of_my_array  /* r0 ← &my_array */
    mov r1, #50               /* r1 ← 50 our array is of length 50 */
    bl fill_array            /* call fill_array */

    /* prepare call to qsort */
    /*
    void qsort(void *base,
         size_t nmemb,
         size_t size,
         int (*compar)(const void *, const void *));
    */

    ldr r0, addr_of_my_array  /* r0 ← &my_array
                                 base */
    mov r1, r8               /* r1 ← r8
                                 nmemb = number of members
                                 our array is 50 elements long */
    mov r2, #4                /* r2 ← 4
                                 size of each member is 4 bytes */
    ldr r3, addr_of_integer_comparison
                              /* r3 ← &integer_comparison
                                 compar */
    bl qsort                  /* call qsort */

    /* Imprimir vector ordenado */
    ldr r0, =txt_orden
    bl  printf

    /* now print sorted array */
    /* prepare call to print_array */
    ldr r0, addr_of_my_array  /* r0 ← &my_array */
    mov r1, r8               /* r1 ← r8
                                 our array is of length 50 */
    bl print_array            /* call print_array */

    /* Imprimir número menor */
    ldr r0, =txt_menor
    ldr r1, addr_of_my_array
    ldr r1, [r1]
    bl  printf

    /* Imprimir promedio */
    bl calculate_average
    mov r1, r0
    ldr r0, =txt_prome
    bl  printf

    /* Calcular moda */
    ldr r0, addr_of_my_array  /* r0 ← &my_array base */
    mov r1, r8                /* r1 ← r8 */
    bl  calculate_trend

    mov r0, #0                /* r0 ← 0 set errorcode to 0 prior returning from main */
    pop {r4, lr}              /* restore r4 and lr in the stack */
    bx lr                     /* return */
