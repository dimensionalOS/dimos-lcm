/*
 * vision_msgs/BoundingBox2D — Arduino-compatible LCM C encode/decode.
 * Wire format: Pose2D(24) + double + double = 40 bytes.
 */
#ifndef DIMOS_ARDUINO_MSG_BOUNDINGBOX2D_H
#define DIMOS_ARDUINO_MSG_BOUNDINGBOX2D_H

#include "vision_msgs/Pose2D.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    dimos_msg__Pose2D center;
    double size_x;
    double size_y;
} dimos_msg__BoundingBox2D;

static inline int dimos_msg__BoundingBox2D__encoded_size(void) { return 40; }

static inline int dimos_msg__BoundingBox2D__encode(void *buf, int offset, int maxlen,
    const dimos_msg__BoundingBox2D *p)
{
    int pos = 0, thislen;
    thislen = dimos_msg__Pose2D__encode(buf, offset + pos, maxlen - pos, &p->center);
    if (thislen < 0) return thislen; pos += thislen;
    thislen = __double_encode_array(buf, offset + pos, maxlen - pos, &p->size_x, 1);
    if (thislen < 0) return thislen; pos += thislen;
    thislen = __double_encode_array(buf, offset + pos, maxlen - pos, &p->size_y, 1);
    if (thislen < 0) return thislen; pos += thislen;
    return pos;
}

static inline int dimos_msg__BoundingBox2D__decode(const void *buf, int offset,
    int maxlen, dimos_msg__BoundingBox2D *p)
{
    int pos = 0, thislen;
    thislen = dimos_msg__Pose2D__decode(buf, offset + pos, maxlen - pos, &p->center);
    if (thislen < 0) return thislen; pos += thislen;
    thislen = __double_decode_array(buf, offset + pos, maxlen - pos, &p->size_x, 1);
    if (thislen < 0) return thislen; pos += thislen;
    thislen = __double_decode_array(buf, offset + pos, maxlen - pos, &p->size_y, 1);
    if (thislen < 0) return thislen; pos += thislen;
    return pos;
}

#ifdef __cplusplus
}
#endif

#endif
