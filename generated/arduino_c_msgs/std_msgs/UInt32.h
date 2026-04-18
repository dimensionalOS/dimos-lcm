/*
 * std_msgs/UInt32 — Arduino-compatible LCM C encode/decode.
 * Wire format: int32_t = 4 bytes.
 */
#ifndef DIMOS_ARDUINO_MSG_UINT32_H
#define DIMOS_ARDUINO_MSG_UINT32_H

#include "lcm_coretypes_arduino.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    int32_t data;
} dimos_msg__UInt32;

static inline int dimos_msg__UInt32__encoded_size(void) { return 4; }

static inline int dimos_msg__UInt32__encode(void *buf, int offset, int maxlen,
    const dimos_msg__UInt32 *p)
{
    return __int32_t_encode_array(buf, offset, maxlen, &p->data, 1);
}

static inline int dimos_msg__UInt32__decode(const void *buf, int offset,
    int maxlen, dimos_msg__UInt32 *p)
{
    return __int32_t_decode_array(buf, offset, maxlen, &p->data, 1);
}

#ifdef __cplusplus
}
#endif

#endif
