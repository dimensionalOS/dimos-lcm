/*
 * std_msgs/UInt16 — Arduino-compatible LCM C encode/decode.
 * Wire format: int16_t = 2 bytes.
 */
#ifndef DIMOS_ARDUINO_MSG_UINT16_H
#define DIMOS_ARDUINO_MSG_UINT16_H

#include "lcm_coretypes_arduino.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    int16_t data;
} dimos_msg__UInt16;

static inline int dimos_msg__UInt16__encoded_size(void) { return 2; }

static inline int dimos_msg__UInt16__encode(void *buf, int offset, int maxlen,
    const dimos_msg__UInt16 *p)
{
    return __int16_t_encode_array(buf, offset, maxlen, &p->data, 1);
}

static inline int dimos_msg__UInt16__decode(const void *buf, int offset,
    int maxlen, dimos_msg__UInt16 *p)
{
    return __int16_t_decode_array(buf, offset, maxlen, &p->data, 1);
}

#ifdef __cplusplus
}
#endif

#endif
