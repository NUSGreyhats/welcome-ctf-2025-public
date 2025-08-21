/* minimal.ld */
OUTPUT_FORMAT(elf64-x86-64) /* Specify output format for x86-64 ELF */
OUTPUT_ARCH(i386:x86-64)   /* Specify target architecture */
ENTRY(_start)              /* Define the entry point (your custom _start function) */

SECTIONS
{
    /* Set the base virtual address (VMA) for the executable.
     * This is a typical starting address for Linux executables. */
    . = 0x400000;

    /* .text section: Contains executable code */
    .text : {
        *(.text) /* Include all .text sections from input object files */
    }

    /* .rodata section: Contains read-only data (like your 'key' string) */
    .rodata : {
        *(.rodata) /* Include all .rodata sections */
    }

    /* .data section: Contains initialized writable data */
    .data : {
        *(.data) /* Include all .data sections */
    }

    /* .bss section: Contains uninitialized data.
     * This section does not take up space in the binary file itself,
     * but its size is recorded in the ELF header, and the OS zeroes it out at runtime. */
    .bss : {
        *(.bss) /* Include all .bss sections */
    }

    /* Discard sections that are commonly generated but not needed for a minimal binary.
     * These sections would otherwise add to the file size or complexity. */
    /DISCARD/ : {
        *(.note.GNU-stack) /* Standard stack information */
        *(.eh_frame)       /* Exception handling frames */
        *(.comment)        /* Compiler version comments */
        *(.dynsym)         /* Dynamic symbols */
        *(.dynstr)         /* Dynamic strings */
        *(.hash)           /* Symbol hash table */
        *(.gnu.version)    /* GNU versioning info */
        *(.gnu.version_d)
        *(.gnu.version_r)
        *(.interp)         /* Program interpreter path (for dynamic linking) */
        *(.dynamic)        /* Dynamic linking information */
        *(.got)            /* Global Offset Table */
        *(.got.plt)        /* Global Offset Table for Procedure Linkage Table */
        *(.plt)            /* Procedure Linkage Table */
        *(.rel.dyn)        /* Relocation info for dynamic sections */
        *(.rel.plt)        /* Relocation info for PLT */
        *(.rela.dyn)
        *(.rela.plt)
        *(.shstrtab)       /* Section header string table */
        *(.symtab)         /* Symbol table (stripped by -s, but good to discard) */
        *(.strtab)         /* String table for symbol names */
        *(.debug*)         /* Debugging sections */
        *(.buildid)        /* Build ID information */
    }
}