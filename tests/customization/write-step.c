#include <assert.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include "WorkbenchWriteStep.h"
static char received[100000];
static size_t used, calls;
static ssize_t partial(int fd, const void *data, size_t length) {
  (void)fd; assert(length <= 16384); calls++;
  if (calls % 5 == 0) { errno = EAGAIN; return -1; }
  if (calls % 7 == 0) { errno = EINTR; return -1; }
  size_t count = length > 113 ? 113 : length;
  memcpy(received + used, data, count); used += count;
  return (ssize_t)count;
}
static ssize_t zero(int f, const void *p, size_t l) { (void)f;(void)p;(void)l;return 0; }
int main(void) {
  char expected[70000]; for (size_t i=0;i<sizeof expected;i++) expected[i]=(char)(i%251);
  size_t offset=0;
  for (int turns=0; offset<sizeof expected && turns<2000; turns++) {
    WBWriteResult result=WBWriteStep(0, expected+offset, sizeof expected-offset, partial);
    assert(!result.error); offset+=result.advanced;
  }
  assert(offset==sizeof expected && used==sizeof expected && !memcmp(expected,received,used));
  assert(WBWriteStep(0, expected, 1, zero).error==EIO);
  assert(WBWriteStep(0, expected, 0, zero).error==0);
  int pipes[2]; assert(pipe(pipes)==0);
  assert(fcntl(pipes[1], F_SETFL, fcntl(pipes[1], F_GETFL)|O_NONBLOCK)==0);
  while(write(pipes[1],expected,4096)>0) {}
  WBWriteResult wait=WBWriteStep(pipes[1],expected,4096,write); assert(wait.wait && !wait.advanced);
  assert(read(pipes[0],received,sizeof received)>0);
  assert(WBWriteStep(pipes[1],expected,4096,write).advanced>0);
  signal(SIGPIPE,SIG_IGN); close(pipes[0]);
  assert(WBWriteStep(pipes[1],expected,4096,write).error==EPIPE);close(pipes[1]);
  puts("PASS: exact byte ordering across partial writes/EINTR/EAGAIN, chunk cap, zero progress, real full pipe and closed-pipe failure");
}
