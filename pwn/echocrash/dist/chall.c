#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>

#define BUF_SIZE 0x200
#define START_CHUNK 1
#define CONT_CHUNK 2
#define HEADER_SIZE 5

uint8_t global_buffer[BUF_SIZE];

void win() {
	FILE *f = fopen("./flag.txt", "r");
	fseek(f, 0, SEEK_END);
	size_t sz = ftell(f);
	fseek(f, 0, SEEK_SET);
	char* flag = malloc(sz);
	fread(flag, sz, 1, f);
	fclose(f);
	puts(flag);
}

void send_checksum(uint8_t *data, size_t len) {
    uint64_t checksum = 0;
    for (size_t i = 0; i < len; ++i)
        checksum += data[i];
    write(1, &checksum, sizeof(checksum));
}

void handle_packet(int fd) {
    uint8_t header[HEADER_SIZE];
    uint8_t packet_data[BUF_SIZE];
    int start_seen = 0;

    while (1) {
        if (read(fd, header, HEADER_SIZE) != HEADER_SIZE) break;

        int8_t type = header[0];
        int16_t size = *(int16_t*)(header + 1);
        int16_t buffer_offset = *(int16_t*)(header + 3);

        if (size > BUF_SIZE - HEADER_SIZE) continue; // basic sanity

        if (read(fd, packet_data, size) != size) break;

        if (type == START_CHUNK) {
            memset(global_buffer, 0, BUF_SIZE);
            buffer_offset = 0;
            start_seen = 1;
        }

        if (!start_seen) continue;

        memcpy(global_buffer + buffer_offset, packet_data, size);

        if (buffer_offset > 0x180) {
            send_checksum(global_buffer, buffer_offset);
            break;
        }
    }
}

int main() {

	setbuf(stdin, 0);
	setbuf(stdout, 0);

    puts("EchoCrash v1.0");
    puts("Send fragmented payloads. Type=1 to start, 2 to continue.");
    puts("Checksum will be returned once buffer crosses 0x180 bytes.");
    handle_packet(0);
    return 0;
}

