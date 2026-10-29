// macOS-only integration tests for the actual Objective-C queue and real pipes.
#import <Foundation/Foundation.h>
#import "WorkbenchInputDelivery.h"
#import <fcntl.h>
#import <unistd.h>
#include <assert.h>
#include <string.h>
static void tick(void) { [[NSRunLoop currentRunLoop] runUntilDate:[NSDate dateWithTimeIntervalSinceNow:0.002]]; }
static NSData *drain(int fd, WorkbenchInputDelivery *writer, NSUInteger expectedMinimum) {
  NSMutableData *result = [NSMutableData data];
  NSDate *deadline = [NSDate dateWithTimeIntervalSinceNow:8];
  while ([deadline timeIntervalSinceNow] > 0) {
    uint8_t bytes[32768]; ssize_t count;
    while ((count=read(fd,bytes,sizeof bytes))>0) [result appendBytes:bytes length:(NSUInteger)count];
    if (result.length >= expectedMinimum && writer.pendingBytes == 0) { tick(); break; }
    tick();
  }
  return result;
}
int main(void) { @autoreleasepool {
  int pipes[2]; assert(pipe(pipes)==0); fcntl(pipes[0],F_SETFL,O_NONBLOCK);
  __block BOOL failed=NO;
  WorkbenchInputDelivery *writer=[[WorkbenchInputDelivery alloc] initWithFD:pipes[1] status:^(NSUInteger pending,NSString *error){ assert(pending<=4*1024*1024); if(error) failed=YES; }];
  assert(writer); close(pipes[1]);
  NSMutableData *expected=[NSMutableData data];
  for(int i=0;i<100;i++) { NSData *part=[[NSString stringWithFormat:@"frame-%d-👩🏽‍💻\n",i] dataUsingEncoding:NSUTF8StringEncoding]; [expected appendData:part]; assert([writer enqueue:part]); }
  assert([[drain(pipes[0],writer,expected.length) copy] isEqual:expected]);assert(!failed);
  assert(![writer enqueue:[NSMutableData dataWithLength:5*1024*1024]]);
  // Cancel a stalled queue, then immediately enqueue new input. New-generation
  // bytes must survive cancellation and appear after any already-delivered prefix.
  NSMutableData *large=[NSMutableData dataWithLength:1024*1024];memset(large.mutableBytes,'x',large.length);
  assert([writer enqueue:large]); for(int i=0;i<20;i++)tick();
  [writer cancelPending];NSData *after=[@"AFTER-CANCEL" dataUsingEncoding:NSUTF8StringEncoding];assert([writer enqueue:after]);
  NSData *tail=drain(pipes[0],writer,after.length);assert(tail.length>=after.length);
  assert([[tail subdataWithRange:NSMakeRange(tail.length-after.length,after.length)] isEqual:after]);
  for(NSUInteger i=0;i<tail.length-after.length;i++) assert(((const uint8_t *)tail.bytes)[i]=='x');
  [writer invalidate];close(pipes[0]);for(int i=0;i<10;i++)tick();
  // A closed read end must be reported, never terminate the test with SIGPIPE.
  assert(pipe(pipes)==0); __block BOOL closedFailure=NO;
  writer=[[WorkbenchInputDelivery alloc] initWithFD:pipes[1] status:^(NSUInteger pending,NSString *error){ (void)pending;if(error)closedFailure=YES; }];
  assert(writer);close(pipes[1]);close(pipes[0]);assert([writer enqueue:after]);
  NSDate *deadline=[NSDate dateWithTimeIntervalSinceNow:2];while(!closedFailure&&[deadline timeIntervalSinceNow]>0)tick();assert(closedFailure);[writer invalidate];
  for(int i=0;i<10;i++)tick();
  puts("PASS: native input FIFO, UTF-8 frames, bounded queue, cancel/new-input race, owned descriptor lifetime and closed-pipe reporting");
} return 0; }
