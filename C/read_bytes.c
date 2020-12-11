#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>

int main(void){

	int fd;
	ssize_t ret;
	unsigned long word; 

	fd = open("./file", O_RDONLY);
	void* buf = &word;
	size_t len = sizeof(unsigned long); /* x86_64 : 8bytes */

	/* Keep reading until len n° bytes read or EOF reached */
	while (len != 0 && (ret = read(fd, buf, len)) != 0){
		if (ret == -1){
			if (errno == EINTR)
				continue;
			/* Serious error or EAGAIN (Non blocking mode) */
			perror("read");
			break;
		}

		len -= ret;
		buf += ret;
	}

	printf("%lx \n", word);

	if (ret == -1)
		/* error */

	return 0;
}