CC = gcc
CFLAGS = -Wall -O2

all: sendprobe usleep

sendprobe: sendprobe.c
	$(CC) $(CFLAGS) -o sendprobe sendprobe.c

usleep: usleep.c
	$(CC) $(CFLAGS) -o usleep usleep.c

clean:
	rm -f sendprobe usleep
