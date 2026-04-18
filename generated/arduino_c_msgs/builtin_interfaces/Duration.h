/*
 * builtin_interfaces/Duration — Arduino-compatible LCM C encode/decode.
 * Wire format: int32_t + int32_t = 8 bytes.
 */
#ifndef DIMOS_ARDUINO_MSG_DURATION_H
#define DIMOS_ARDUINO_MSG_DURATION_H

#include "lcm_coretypes_arduino.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    int32_t sec;
    int32_t nanosec;
} dimos_msg__Duration;

static inline int dimos_msg__Duration__encoded_size(void) { return 8; }

static inline int dimos_msg__Duration__encode(void *buf, int offset, int maxlen,
    const dimos_msg__Duration *p)
{
    int pos = 0, thislen;
    thislen = __int32_t_encode_array(buf, offset + pos, maxlen - pos, &p->sec, 1);
    if (thislen < 0) return thislen; pos += thislen;
    thislen = __int32_t_encode_array(buf, offset + pos, maxlen - pos, &p->nanosec, 1);
    if (thislen < 0) return thislen; pos += thislen;
    return pos;
}

static inline int dimos_msg__Duration__decode(const void *buf, int offset,
    int maxlen, dimos_msg__Duration *p)
{
    int pos = 0, thislen;
    thislen = __int32_t_decode_array(buf, offset + pos, maxlen - pos, &p->sec, 1);
    if (thislen < 0) return thislen; pos += thislen;
    thislen = __int32_t_decode_array(buf, offset + pos, maxlen - pos, &p->nanosec, 1);
    if (thislen < 0) return thislen; pos += thislen;
    return pos;
}

#ifdef __cplusplus
}
#endif

#endif
