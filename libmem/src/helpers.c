#include "internal.h"

#if LM_OS != LM_OS_WIN
#include <fcntl.h>

LM_PRIVATE lm_size_t
_LM_OpenFileBuf(lm_tstring_t path, 
		lm_tchar_t **pfilebuf)
{
	int         fd;
	lm_size_t   total = 0;
	ssize_t     rdsize = 0;
	size_t      rdcount = 1024;
	lm_tchar_t *filebuf = (lm_tchar_t *)LM_NULLPTR;
	lm_size_t   allocsize = 1024 + sizeof(lm_tchar_t);

	fd = open(path, O_RDONLY);
	if (fd == -1)
		return total;

	do {
		/* Use 'realloc' to increase the buffer size and copy the old data */
		filebuf = (lm_tchar_t *)LM_REALLOC(filebuf, allocsize);

		if (!filebuf) {
			total = 0;
			break;
		}

		total += rdsize;
		allocsize += rdcount;
	} while ((rdsize = read(fd, &((char *)filebuf)[total], rdcount)) > 0);

	if (filebuf) {
		filebuf[total] = LM_STR('\x00');
		*pfilebuf = filebuf;
	}

	close(fd);
	return total;
}

LM_PRIVATE lm_void_t
_LM_CloseFileBuf(lm_tchar_t **pfilebuf)
{
	if (pfilebuf && *pfilebuf) {
		LM_FREE(*pfilebuf);
		*pfilebuf = (lm_tchar_t *)LM_NULL;
	}
}
#endif
