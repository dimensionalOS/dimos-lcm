/*
 * std_msgs/UInt8 — Arduino-compatible LCM C encode/decode.
 * Wire format: byte = 1 bytes.
 */
#ifndef DIMOS_ARDUINO_MSG_UINT8_H
#define DIMOS_ARDUINO_MSG_UINT8_H

#include "lcm_coretypes_arduino.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint8_t data;
} dimos_msg__UInt8;

static inline int dimos_msg__UInt8__encoded_size(void) { return 1; }

static inline int dimos_msg__UInt8__encode(void *buf, int offset, int maxlen,
    const dimos_msg__UInt8 *p)
{
    return __byte_encode_array(buf, offset, maxlen, &p->data, 1);
}

static inline int dimos_msg__UInt8__decode(const void *buf, int offset,
    int maxlen, dimos_msg__UInt8 *p)
{
    return __byte_decode_array(buf, offset, maxlen, &p->data, 1);
}

#ifdef __cplusplus
}
#endif

#endif
