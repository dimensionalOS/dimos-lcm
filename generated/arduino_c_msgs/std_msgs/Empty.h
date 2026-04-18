/*
 * std_msgs/Empty — Arduino-compatible LCM C encode/decode.
 * Wire format:  = 0 bytes.
 */
#ifndef DIMOS_ARDUINO_MSG_EMPTY_H
#define DIMOS_ARDUINO_MSG_EMPTY_H

#include "lcm_coretypes_arduino.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
} dimos_msg__Empty;

static inline int dimos_msg__Empty__encoded_size(void) { return 0; }

static inline int dimos_msg__Empty__encode(void *buf, int offset, int maxlen,
    const dimos_msg__Empty *p)
{
    int pos = 0, thislen;
    return pos;
}

static inline int dimos_msg__Empty__decode(const void *buf, int offset,
    int maxlen, dimos_msg__Empty *p)
{
    int pos = 0, thislen;
    return pos;
}

#ifdef __cplusplus
}
#endif

#endif
