/*
 * sensor_msgs/JoyFeedback — Arduino-compatible LCM C encode/decode.
 * Wire format: byte + byte + float = 6 bytes.
 */
#ifndef DIMOS_ARDUINO_MSG_JOYFEEDBACK_H
#define DIMOS_ARDUINO_MSG_JOYFEEDBACK_H

#include "lcm_coretypes_arduino.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint8_t type;
    uint8_t id;
    float intensity;
} dimos_msg__JoyFeedback;

static inline int dimos_msg__JoyFeedback__encoded_size(void) { return 6; }

static inline int dimos_msg__JoyFeedback__encode(void *buf, int offset, int maxlen,
    const dimos_msg__JoyFeedback *p)
{
    int pos = 0, thislen;
    thislen = __byte_encode_array(buf, offset + pos, maxlen - pos, &p->type, 1);
    if (thislen < 0) return thislen; pos += thislen;
    thislen = __byte_encode_array(buf, offset + pos, maxlen - pos, &p->id, 1);
    if (thislen < 0) return thislen; pos += thislen;
    thislen = __float_encode_array(buf, offset + pos, maxlen - pos, &p->intensity, 1);
    if (thislen < 0) return thislen; pos += thislen;
    return pos;
}

static inline int dimos_msg__JoyFeedback__decode(const void *buf, int offset,
    int maxlen, dimos_msg__JoyFeedback *p)
{
    int pos = 0, thislen;
    thislen = __byte_decode_array(buf, offset + pos, maxlen - pos, &p->type, 1);
    if (thislen < 0) return thislen; pos += thislen;
    thislen = __byte_decode_array(buf, offset + pos, maxlen - pos, &p->id, 1);
    if (thislen < 0) return thislen; pos += thislen;
    thislen = __float_decode_array(buf, offset + pos, maxlen - pos, &p->intensity, 1);
    if (thislen < 0) return thislen; pos += thislen;
    return pos;
}

#ifdef __cplusplus
}
#endif

#endif
